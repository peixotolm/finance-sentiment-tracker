CREATE TABLE products (
    id INTEGER,
    title VARCHAR NOT NULL,
    PRIMARY KEY (title)
);

CREATE TABLE sentiments (
    id INTEGER PRIMARY KEY,
    product_name VARCHAR NOT NULL,
    positive_count INTEGER DEFAULT 0,
    neutral_count INTEGER DEFAULT 0,
    negative_count INTEGER DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_name) REFERENCES products (title)
);

CREATE TABLE stock_data (
    id INTEGER PRIMARY KEY,
    product_name VARCHAR NOT NULL,
    price FLOAT,
    open_price FLOAT,
    close_price FLOAT,
    high FLOAT,
    low FLOAT,
    volume FLOAT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_name) REFERENCES products (title)
);