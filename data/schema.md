## Schema

E-commerce database with the following tables:

### Table: products
- product_id: int, PRIMARY KEY, unique product identifier
- product_brand: str, brand name
- product_name: str, product name
- product_description: str, product description
- product_price: float, product price
- product_category: str, main category
- product_subcategory: str, subcategory

### Table: customers
- customer_id: int, PRIMARY KEY, unique customer identifier
- customer_city: str, customer's city
- customer_state: str, customer's state/province
- customer_zip: str, customer's zip code
- customer_country: str, customer's country
- customer_gender: str, customer's gender
- customer_age: int, customer's age
- customer_class_quartile: str, customer's class quartile
- customer_description: str, customer's description

### Table: orders
- order_id: int, part of COMPOSITE PRIMARY KEY, unique order identifier
- order_seq_nbr: int, part of COMPOSITE PRIMARY KEY, sequence number for the order
- customer_id: int, FOREIGN KEY to customers.customer_id
- product_id: int, FOREIGN KEY to products.product_id
- order_date: date, date of the order
- COMPOSITE PRIMARY KEY: (order_id, order_seq_nbr)