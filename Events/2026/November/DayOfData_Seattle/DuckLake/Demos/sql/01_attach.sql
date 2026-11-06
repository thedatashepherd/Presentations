-- Run from your extracted Demos directory. Local demo credentials only.
INSTALL ducklake;
INSTALL postgres;
LOAD ducklake;
LOAD postgres;
ATTACH 'ducklake:postgres:dbname=ducklake_catalog host=127.0.0.1 port=55432 user=ducklake_demo password=local_demo_only' AS lake
  (DATA_PATH '/ABSOLUTE/PATH/TO/Demos/data/', DATA_INLINING_ROW_LIMIT 0);
USE lake;
