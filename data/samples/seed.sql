-- Olist Analytics Sample Seed (PostgreSQL)
--
-- Overview
-- --------
-- Minimal, consistent dataset to smoke‑test queries and end‑to‑end flows
-- without requiring full CSV ingestion. Safe to run multiple times.

BEGIN;

SET search_path = analytics, public;

-- Clean current sample data (keeps other environments/data intact)
TRUNCATE TABLE
    order_items,
    order_payments,
    order_reviews,
    orders,
    products,
    sellers,
    customers,
    product_category_translation,
    geolocation
RESTART IDENTITY CASCADE;

-- Category translations ------------------------------------------------------
INSERT INTO product_category_translation (product_category_name, product_category_name_english) VALUES
    ('informatica_acessorios', 'computers_accessories'),
    ('moveis_decoracao',       'furniture_decor'),
    ('beleza_saude',           'health_beauty')
ON CONFLICT (product_category_name) DO NOTHING;

-- Customers -----------------------------------------------------------------
INSERT INTO customers (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state) VALUES
    ('c_001', 'u_001', 12345, 'Sao Paulo',       'SP'),
    ('c_002', 'u_002', 22222, 'Rio de Janeiro',  'RJ')
ON CONFLICT (customer_id) DO NOTHING;

-- Sellers -------------------------------------------------------------------
INSERT INTO sellers (seller_id, seller_zip_code_prefix, seller_city, seller_state) VALUES
    ('s_001', 13000, 'Campinas', 'SP'),
    ('s_002', 29000, 'Vitoria',  'ES')
ON CONFLICT (seller_id) DO NOTHING;

-- Products ------------------------------------------------------------------
INSERT INTO products (
    product_id, product_category_name, product_name_lenght, product_description_lenght,
    product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm
) VALUES
    ('p_001', 'informatica_acessorios', 12,  80, 1,  500, 20, 10, 15),
    ('p_002', 'moveis_decoracao',       14, 120, 2, 3000, 60, 40, 50)
ON CONFLICT (product_id) DO NOTHING;

-- Orders --------------------------------------------------------------------
INSERT INTO orders (
    order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at,
    order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date
) VALUES
    ('o_001', 'c_001', 'delivered', '2024-12-01 10:00:00', '2024-12-01 10:05:00',
     '2024-12-02 08:00:00', '2024-12-05 18:30:00', '2024-12-10 00:00:00'),
    ('o_002', 'c_002', 'shipped',   '2025-01-15 09:12:00', '2025-01-15 09:20:00',
     '2025-01-16 11:00:00', NULL, '2025-01-22 00:00:00')
ON CONFLICT (order_id) DO NOTHING;

-- Order items ---------------------------------------------------------------
INSERT INTO order_items (
    order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value
) VALUES
    ('o_001', 1, 'p_001', 's_001', '2024-12-03 00:00:00', 100.00, 15.00),
    ('o_001', 2, 'p_002', 's_002', '2024-12-03 00:00:00',  50.00, 10.00),
    ('o_002', 1, 'p_002', 's_002', '2025-01-17 00:00:00', 320.00, 25.00)
ON CONFLICT (order_id, order_item_id) DO NOTHING;

-- Order payments ------------------------------------------------------------
INSERT INTO order_payments (
    order_id, payment_sequential, payment_type, payment_installments, payment_value
) VALUES
    ('o_001', 1, 'credit_card', 2, 175.00),
    ('o_002', 1, 'boleto',      1, 345.00)
ON CONFLICT (order_id, payment_sequential) DO NOTHING;

-- Order reviews -------------------------------------------------------------
INSERT INTO order_reviews (
    review_id, order_id, review_score, review_comment_title, review_comment_message,
    review_creation_date, review_answer_timestamp
) VALUES
    ('r_001', 'o_001', 5, 'Entrega rápida', 'Tudo certo.', '2024-12-06 10:00:00', '2024-12-06 12:00:00')
ON CONFLICT (review_id) DO NOTHING;

-- Geolocation ---------------------------------------------------------------
INSERT INTO geolocation (
    geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state
) VALUES
    (12345, -23.5505, -46.6333, 'Sao Paulo',      'SP'),
    (22222, -22.9068, -43.1729, 'Rio de Janeiro', 'RJ'),
    (13000, -22.9099, -47.0626, 'Campinas',       'SP'),
    (29000, -20.3155, -40.3128, 'Vitoria',        'ES');

COMMIT;