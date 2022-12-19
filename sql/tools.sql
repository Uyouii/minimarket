-- 查询用户数据库中表的行数
SELECT  table_name,table_rows FROM information_schema.tables
WHERE table_schema = 'minimarket_user_db' ORDER BY table_rows desc;

-- 查询商品数据库中表的行数
SELECT  table_name,table_rows FROM information_schema.tables
WHERE table_schema = 'minimarket_product_db' ORDER BY table_rows desc;