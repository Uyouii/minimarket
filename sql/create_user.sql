use minimarket_user_db;

drop table user_tab_0;
drop table user_tab_1;
drop table user_tab_2;
drop table user_tab_3;
drop table user_tab_4;
drop table user_tab_5;
drop table user_tab_6;
drop table user_tab_7;
drop table user_tab_8;
drop table user_tab_9;

create table if not exists user_tab_0(
    id bigint(20) unsigned primary key,
    name varchar(32) unique not null,
    password varchar(50) not null,
    create_timestamp int unsigned,
    avatar varchar(128),
    session varchar(32),
    login_timestamp int unsigned
);

create table user_tab_1 like user_tab_0;
create table user_tab_2 like user_tab_0;
create table user_tab_3 like user_tab_0;
create table user_tab_4 like user_tab_0;
create table user_tab_5 like user_tab_0;
create table user_tab_6 like user_tab_0;
create table user_tab_7 like user_tab_0;
create table user_tab_8 like user_tab_0;
create table user_tab_9 like user_tab_0;


explain select * from user_tab_0 where name = 'testuser2';
explain select * from user_tab_0 where id = 1514332880696832;
