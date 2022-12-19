use minimarket_product_db;

drop table comment_tab_0;
drop table comment_tab_1;
drop table comment_tab_2;
drop table comment_tab_3;
drop table comment_tab_4;

create table if not exists comment_tab_0(
    id bigint primary key,
    product_id bigint not null,
    user_id bigint not null,
    resp_comment_id bigint not null default 0,  -- 非0表示是回复
    content varchar(512) not null,
    create_time bigint not null,
    update_time bigint,
    img varchar(128)
);

create index product_id_resp_comment_id_index on comment_tab_0 (product_id, resp_comment_id);

create index resp_comment_id_index on comment_tab_0 (resp_comment_id);

ALTER TABLE `comment_tab_0` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

create table comment_tab_1 like comment_tab_0;
create table comment_tab_2 like comment_tab_0;
create table comment_tab_3 like comment_tab_0;
create table comment_tab_4 like comment_tab_0;

-- 查询商品下的评论
explain select * from comment_tab_0 where product_id=100 and resp_comment_id=0 order by create_time limit 5;

-- 查询评论下的回复
explain select * from comment_tab_0 where resp_comment_id=100 order by create_time limit 5;

-- 查询商品评论和回复
explain select * from comment_tab_0 where product_id=100 order by create_time limit 5;