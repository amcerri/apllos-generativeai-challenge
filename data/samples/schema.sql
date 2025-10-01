-- Olist Analytics Schema (PostgreSQL)
--
-- Normalized tables derived from Olist CSV datasets.

BEGIN;

CREATE SCHEMA IF NOT EXISTS analytics;
SET search_path = analytics, public;

-- Product category translation ---------------------------------------------
-- CSV: product_category_name_translation.csv
-- Columns: product_category_name, product_category_name_english
CREATE TABLE IF NOT EXISTS product_category_translation (
    product_category_name          TEXT PRIMARY KEY,
    product_category_name_english  TEXT NOT NULL
);

-- Customers -----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customers (
    customer_id                TEXT PRIMARY KEY,
    customer_unique_id         TEXT NOT NULL,
    customer_zip_code_prefix   INTEGER NOT NULL,
    customer_city              TEXT NOT NULL,
    customer_state             TEXT NOT NULL
);

-- Geolocation ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS geolocation (
    geolocation_zip_code_prefix INTEGER NOT NULL,
    geolocation_lat             DOUBLE PRECISION NOT NULL,
    geolocation_lng             DOUBLE PRECISION NOT NULL,
    geolocation_city            TEXT NOT NULL,
    geolocation_state           TEXT NOT NULL
);

-- Orders --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS orders (
    order_id                        TEXT PRIMARY KEY,
    customer_id                     TEXT NOT NULL,
    order_status                    TEXT NOT NULL,
    order_purchase_timestamp        TIMESTAMP,
    order_approved_at               TIMESTAMP,
    order_delivered_carrier_date    TIMESTAMP,
    order_delivered_customer_date   TIMESTAMP,
    order_estimated_delivery_date   TIMESTAMP,
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Products ------------------------------------------------------------------
-- CSV: olist_products_dataset.csv
CREATE TABLE IF NOT EXISTS products (
    product_id                   TEXT PRIMARY KEY,
    product_category_name        TEXT,
    product_name_lenght          INTEGER,
    product_description_lenght   INTEGER,
    product_photos_qty           INTEGER,
    product_weight_g             INTEGER,
    product_length_cm            INTEGER,
    product_height_cm            INTEGER,
    product_width_cm             INTEGER,
    CONSTRAINT fk_products_category
        FOREIGN KEY (product_category_name)
        REFERENCES product_category_translation(product_category_name)
);

-- Sellers -------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sellers (
    seller_id                TEXT PRIMARY KEY,
    seller_zip_code_prefix   INTEGER NOT NULL,
    seller_city              TEXT NOT NULL,
    seller_state             TEXT NOT NULL
);

-- Order items ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS order_items (
    order_id             TEXT NOT NULL,
    order_item_id        INTEGER NOT NULL,
    product_id           TEXT NOT NULL,
    seller_id            TEXT NOT NULL,
    shipping_limit_date  TIMESTAMP,
    price                NUMERIC(10,2),
    freight_value        NUMERIC(10,2),
    PRIMARY KEY (order_id, order_item_id),
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)  REFERENCES orders(order_id),
    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT fk_order_items_seller
        FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

-- Order payments ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS order_payments (
    order_id              TEXT NOT NULL,
    payment_sequential    INTEGER NOT NULL,
    payment_type          TEXT NOT NULL,
    payment_installments  INTEGER NOT NULL,
    payment_value         NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (order_id, payment_sequential),
    CONSTRAINT fk_order_payments_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Order reviews -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS order_reviews (
    review_id                TEXT PRIMARY KEY,
    order_id                 TEXT NOT NULL,
    review_score             INTEGER NOT NULL,
    review_comment_title     TEXT,
    review_comment_message   TEXT,
    review_creation_date     TIMESTAMP,
    review_answer_timestamp  TIMESTAMP,
    CONSTRAINT fk_order_reviews_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Indexes for common joins --------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_orders_customer_id        ON orders (customer_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id      ON order_items (order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id    ON order_items (product_id);
CREATE INDEX IF NOT EXISTS idx_order_items_seller_id     ON order_items (seller_id);
CREATE INDEX IF NOT EXISTS idx_order_payments_order_id   ON order_payments (order_id);
CREATE INDEX IF NOT EXISTS idx_order_reviews_order_id    ON order_reviews (order_id);
CREATE INDEX IF NOT EXISTS idx_products_category         ON products (product_category_name);
CREATE INDEX IF NOT EXISTS idx_customers_zip_prefix      ON customers (customer_zip_code_prefix);
CREATE INDEX IF NOT EXISTS idx_sellers_zip_prefix        ON sellers (seller_zip_code_prefix);
CREATE INDEX IF NOT EXISTS idx_geolocation_zip_prefix    ON geolocation (geolocation_zip_code_prefix);

COMMIT;