"""add created_by to products

Revision ID: add_created_by_to_products
Revises: bff7941a8037
Create Date: 2024-04-21 17:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'add_created_by_to_products'
down_revision = 'bff7941a8037'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add created_by column as nullable first
    op.add_column('products', sa.Column('created_by', sa.Integer(), nullable=True))
    
    # Get the first superuser's ID
    connection = op.get_bind()
    result = connection.execute(text("SELECT id FROM users WHERE is_superuser = true ORDER BY id LIMIT 1"))
    superuser_id = result.scalar()
    
    if not superuser_id:
        # If no superuser exists, create one
        result = connection.execute(
            text("INSERT INTO users (email, full_name, hashed_password, is_superuser, is_active) "
                 "VALUES ('admin@example.com', 'Admin', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', true, true) "
                 "RETURNING id")
        )
        superuser_id = result.scalar()
    
    # Update existing products to use the superuser as created_by
    connection.execute(text(f"UPDATE products SET created_by = {superuser_id} WHERE created_by IS NULL"))
    
    # Now make the column not nullable
    op.alter_column('products', 'created_by', nullable=False)
    
    # Add foreign key constraint
    op.create_foreign_key(
        'fk_products_created_by_users',
        'products', 'users',
        ['created_by'], ['id']
    )


def downgrade() -> None:
    # Remove foreign key constraint
    op.drop_constraint('fk_products_created_by_users', 'products', type_='foreignkey')
    # Remove created_by column
    op.drop_column('products', 'created_by') 