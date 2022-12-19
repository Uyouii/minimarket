use minimarket_product_db;

ALTER DATABASE `product_tab` CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci; 

drop table product_tab;

create table if not exists product_tab(
    id bigint primary key, 
    name varchar(128) not null,
    cate varchar(32) not null,
    create_time bigint,
    update_time bigint,
    descript varchar(2048),
    photo varchar(128) not null,
    fulltext key name_full_text(name),
    fulltext key cate_full_text(cate)
);

ALTER TABLE `product_tab` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

explain select * from product_tab where match name against ('app*' IN BOOLEAN MODE) limit 3;

select id,name,cate from product_tab where match name against ('app*' IN BOOLEAN MODE) limit 20;

explain select * from product_tab where match cate against ('phone*' IN BOOLEAN MODE) limit 3;

select id,name,cate from product_tab where match cate against ('phone*' IN BOOLEAN MODE) limit 20;