CREATE TABLE sentiment_data
(
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name   TEXT    NOT NULL,
    positive_count INTEGER NOT NULL,
    neutral_count  INTEGER NOT NULL,
    negative_count INTEGER NOT NULL,
    timestamp      DATETIME DEFAULT CURRENT_TIMESTAMP
);