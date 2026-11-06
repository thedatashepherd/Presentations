CREATE TABLE orders AS
SELECT i AS order_id, (i % 100) + 1 AS customer_id,
       DATE '2026-01-01' + CAST(i % 90 AS INTEGER) AS order_date,
       CAST((i % 200) + 10 AS DECIMAL(12,2)) AS amount
FROM range(1, 5001) t(i);
SELECT count(*) AS orders, sum(amount) AS sales FROM orders;
SELECT * FROM lake.snapshots();
