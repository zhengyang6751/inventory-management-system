# UML Diagrams Documentation

This document contains the UML diagrams for the Inventory Management System, including use case, class, state, and sequence diagrams.

## 1. Use Case Diagram

The use case diagram shows the main functionalities of the system and their relationships with different actors.

### Actors

- Admin User
- Regular User
- System

### Main Use Cases

1. User Management

   - Login
   - Register
   - Manage User Permissions

2. Product Management

   - Add Product
   - Edit Product
   - Delete Product
   - View Product List
   - Track Stock Levels

3. Category Management

   - Add Category
   - Edit Category
   - Delete Category
   - View Categories

4. Supplier Management

   - Add Supplier
   - Edit Supplier
   - Delete Supplier
   - View Suppliers

5. Sales Management

   - Create Sale
   - View Sales History
   - Process Returns
   - Generate Sales Reports

6. Inventory Management
   - Track Stock
   - Set Low Stock Alerts
   - View Stock History
   - Manage Stock Adjustments

## 2. Class Diagram

The class diagram shows the main classes in the system and their relationships.

### Main Classes

1. User

   - Attributes: id, email, full_name, hashed_password, is_active, is_superuser
   - Methods: authenticate(), is_active(), is_superuser()

2. Product

   - Attributes: id, name, description, sku, barcode, price, cost, stock, min_quantity
   - Methods: update_stock(), check_low_stock()

3. Category

   - Attributes: id, name, description
   - Methods: get_products()

4. Supplier

   - Attributes: id, name, contact_name, email, phone, address
   - Methods: get_products()

5. Sale

   - Attributes: id, product_id, customer_id, quantity, unit_price, total_amount, notes
   - Methods: calculate_total(), process_sale()

6. Customer

   - Attributes: id, full_name, email, phone, address
   - Methods: get_sales_history()

7. InventoryTransaction
   - Attributes: id, product_id, quantity, transaction_type, notes
   - Methods: record_transaction()

## 3. State Diagram

The state diagram shows the lifecycle of a Product in the system.

### States

1. New
2. Active
3. Low Stock
4. Out of Stock
5. Discontinued

### Transitions

- New -> Active: When product is added to inventory
- Active -> Low Stock: When stock falls below minimum quantity
- Low Stock -> Active: When stock is replenished
- Active -> Out of Stock: When stock reaches zero
- Out of Stock -> Active: When stock is replenished
- Active -> Discontinued: When product is marked as discontinued

## 4. Sequence Diagram

The sequence diagram shows the process of creating a new sale.

### Objects Involved

1. User Interface
2. SaleController
3. ProductService
4. CustomerService
5. Database

### Flow

1. User selects product and enters quantity
2. System checks product availability
3. System retrieves customer information
4. System calculates total amount
5. System creates sale record
6. System updates product stock
7. System returns confirmation

## 5. Association Analysis

### Is-A Relationships

- None in the current system (no inheritance relationships)

### Has-A Relationships

1. Product has Category (Composition)

   - Cardinality: Many-to-One (Many products can belong to one category)
   - Justification: Products must belong to a category, and categories can contain multiple products

2. Product has Supplier (Composition)

   - Cardinality: Many-to-One (Many products can be supplied by one supplier)
   - Justification: Products must have a supplier, and suppliers can supply multiple products

3. Sale has Product (Aggregation)

   - Cardinality: Many-to-One (Many sales can reference one product)
   - Justification: Sales reference products but products can exist without sales

4. Sale has Customer (Aggregation)

   - Cardinality: Many-to-One (Many sales can be made to one customer)
   - Justification: Sales reference customers but customers can exist without sales

5. InventoryTransaction has Product (Composition)
   - Cardinality: Many-to-One (Many transactions can be recorded for one product)
   - Justification: Transactions must reference a product, and products can have multiple transactions
