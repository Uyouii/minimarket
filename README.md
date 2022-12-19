## MiniMarketTask

### 项目依赖

- mysql 5.7
- django 1.16.11
- gunicorn 19.9.0
- python 2.7
- go 1.18
- nginx 1.21.6
- redis 6.2.6

### 项目结构

- [**`authserver`**](https://git.garena.com/taiyou.dong/minimarkettask/-/tree/master/authserver): go tcp server, 授权服务器
- [**`crawler`**](https://git.garena.com/taiyou.dong/minimarkettask/-/tree/master/crawler): 爬虫项目，爬取https://shopee.sg 商品和评论
  - [数据文件位置](https://git.garena.com/taiyou.dong/markettaskshopeedata)  
- [**`marketserver`**](https://git.garena.com/taiyou.dong/minimarkettask/-/tree/master/marketserver): Django 服务器
- [**`sql`**](https://git.garena.com/taiyou.dong/minimarkettask/-/tree/master/sql): 数据库创建sql文件
- [**`test`**](https://git.garena.com/taiyou.dong/minimarkettask/-/tree/master/test): 测试及压测文件
- [**`doc`**](https://git.garena.com/taiyou.dong/minimarkettask/-/tree/master/doc): 项目文档
  - [api.md](https://git.garena.com/taiyou.dong/minimarkettask/-/blob/master/doc/api.md): 接口文档
  - [perforamcetesting.md](https://git.garena.com/taiyou.dong/minimarkettask/-/blob/master/doc/perforamcetesting.md): 性能测试文档

### 运行

[依赖安装记录](https://git.garena.com/taiyou.dong/minimarkettask/-/blob/master/doc/projectrecord.md)

#### 开启nginx

[nginx 配置](https://git.garena.com/taiyou.dong/minimarkettask/-/blob/master/marketserver/nginx.conf)

```sh
ulimit -n 65535
nginx -s stop
nginx
```

#### 开启TcpServer

```sh
cd minimarkettask/authserver
ulimit -n 65535
go build 
./authserver [release/debug]
```

#### 开启gunicorn

[gunicorn配置](https://git.garena.com/taiyou.dong/minimarkettask/-/blob/master/marketserver/gunicorn.conf.py)

```sh
cd minimarkettask/marketserver
ulimit -n 65535
gunicorn -c gunicorn.conf.py marketserver.wsgi:application
```

#### 接口测试

[接口文档](https://git.garena.com/taiyou.dong/minimarkettask/-/blob/master/doc/api.md)

```sh
cd minimarkettask/test
python testclient.py

login [username] [password]
register [username] [password] [avatar]
getproduct [username] [productid]
getallproduct [username] [pagesize=20] [curpage=0]
searchproductname [username] [searchname] [pagesize=20] [curpage=0]
searchproductcate [username] [cate] [pagesize=20] [curpage=0]
getcomment [username] [commentid]
addcomment [username] [productid] [content]
responsecomment [username] [commentid] [content]
randomaddcomment [username] [productid] [count]
getproductcomment [username] [productid] [pagesize=20] [curpage=0]
getcommentresponses [username] [commentid] [pagesize=20] [curpage=0]
```

#### 性能测试

[性能测试文档](https://git.garena.com/taiyou.dong/minimarkettask/-/blob/master/doc/perforamcetesting.md)

```sh
cd minimarkettask/test/wrk_test
ulimit -n 65535
./wrk_login_test.sh
or
wrk -t16 -c64 -d10s --script=login.lua --latency http://127.0.0.1:8080/auth/login/
```

