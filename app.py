USE smart_business_db;

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    cost_price DECIMAL(10,2) NOT NULL,
    stock_quantity INT NOT NULL
);

CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity_sold INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    sale_date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO products (product_name, price, cost_price, stock_quantity) 
VALUES ('Tea', 50.00, 30.00, 100),
       ('Biscuit', 30.00, 20.00, 200);

INSERT INTO sales (product_id, quantity_sold, total_amount, sale_date) 
VALUES (1, 5, 250.00, '2026-11-01'),
       (2, 10, 300.00, '2026-11-01'),
       (1, 8, 400.00, '2026-11-02');
