## 整体架构

![](https://note.youdao.com/yws/api/personal/file/WEB2ca58ff7376054e8db44ecd3ac376a69?method=download&shareKey=7dbc7fa322c3b14c7483c6f8730ee9df)

## 存储设计

选用mysql作为数据存储服务。

### 用户信息存储

用户信息表字段：

```sql
+------------------+---------------------+------+-----+---------+-------+
| Field            | Type                | Null | Key | Default | Extra |
+------------------+---------------------+------+-----+---------+-------+
| id               | bigint(20) unsigned | NO   | PRI | NULL    |       |
| name             | varchar(32)         | NO   | UNI | NULL    |       |
| password         | varchar(50)         | NO   |     | NULL    |       |
| create_timestamp | int(10) unsigned    | YES  |     | NULL    |       |
| avatar           | varchar(128)        | YES  |     | NULL    |       |
| session          | varchar(32)         | YES  |     | NULL    |       |
| login_timestamp  | int(10) unsigned    | YES  |     | NULL    |       |
+------------------+---------------------+------+-----+---------+-------+
```

索引：

```sql
+------------+------------+----------+--------------+-------------+------------+
| Table      | Non_unique | Key_name | Seq_in_index | Column_name | Index_type |
+------------+------------+----------+--------------+-------------+------------+
| user_tab_0 |          0 | PRIMARY  |            1 | id          | BTREE      |
| user_tab_0 |          0 | name     |            1 | name        | BTREE      |
+------------+------------+----------+--------------+-------------+------------+
```

用户量级为1000w，对用户表进行分表操作，分为10张表。

```sql
+------------------------------+
| Tables_in_minimarket_user_db |
+------------------------------+
| user_tab_0                   |
| user_tab_1                   |
| user_tab_2                   |
| user_tab_3                   |
| user_tab_4                   |
| user_tab_5                   |
| user_tab_6                   |
| user_tab_7                   |
| user_tab_8                   |
| user_tab_9                   |
+------------------------------+
```

#### 表id路由方式

分表之后需要通过username和userid同时查询用户数据，即可以通过username或userid获取表id。

用户登录时需要通过username获取用户信息，可以通过对username进行hash取模的方式。

这里使用go语言自带的fnv hash算法。

```go
fnv(username) % 10
```

同时也要保证userid可以获取到同样的表id，可以把表id信息包含在userid的信息里。

```sh
|-1bit-|---41bit mstime---|---15bit random num---|---7bit tableid---|
|---------------------------- 64 bit -------------------------------|
```

用户在

