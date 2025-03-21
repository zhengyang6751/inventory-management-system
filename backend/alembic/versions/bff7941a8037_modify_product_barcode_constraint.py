"""modify_product_barcode_constraint

Revision ID: bff7941a8037
Revises: f00a24e0de95
Create Date: 2024-03-21 13:22:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bff7941a8037'
down_revision: Union[str, None] = 'f00a24e0de95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Drop the existing index
    op.drop_index('ix_products_barcode', table_name='products')
    
    # 2. Modify the column to allow NULL values
    op.alter_column('products', 'barcode',
                    existing_type=sa.String(),
                    nullable=True)
    
    # 3. Create a new unique index that excludes NULL values
    op.create_index('ix_products_barcode', 'products', ['barcode'],
                    unique=True,
                    postgresql_where=sa.text("barcode IS NOT NULL AND barcode != ''"))


def downgrade() -> None:
    # 1. Drop the conditional unique index
    op.drop_index('ix_products_barcode', table_name='products')
    
    # 2. Modify the column to not allow NULL values
    op.alter_column('products', 'barcode',
                    existing_type=sa.String(),
                    nullable=False)
    
    # 3. Create the original unique index
    op.create_index('ix_products_barcode', 'products', ['barcode'], unique=True) 