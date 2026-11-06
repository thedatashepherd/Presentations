ALTER TABLE orders ADD COLUMN channel VARCHAR DEFAULT 'web';
SELECT order_id, channel FROM orders ORDER BY order_id LIMIT 5;
SELECT * FROM lake.snapshots();
