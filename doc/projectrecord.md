## 项目配置记录

### python

m1芯片的mac自带的python2.7访问mysql会有问题，建议不使用系统自带的python，自行下载个python2.7使用

### MySql

mysq 5.7.30 下载地址：https://downloads.mysql.com/archives/community/

m1芯片也可以运行x86的版本

需要自己添加下系统路径：

```sh
export PATH=$PATH:/usr/local/mysql/bin
export PATH=$PATH:/usr/local/mysql/support-files
```

### django

看一下入门教程：https://django-chinese-docs-16.readthedocs.io/en/latest/intro/index.html

配置下环境变量:

```sh
export PATH=$PATH:/Users/taiyou.dong/Library/Python/2.7/bin
```

创建项目：

```sh
django-admin.py startproject [project_name]
```

运行项目：
```sh
python manage.py runserver 8000
```

配置mysql：

```py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "minimarket_product_db",
        "USER": "root",
        "PASSWORD": "asdfgh",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        'OPTIONS': {'charset':'utf8mb4'},  
    },
}
```

同步django数据库设置：

```sh
 python manage.py syncdb
```

创建app：

```sh
 python manage.py startapp [appname]
```

创建超级用户：

```sh
python manage.py createsuperuser --username=joe --email=joe@example.com
```

settings.py里配置gunicorn:

```python
INSTALLED_APPS = (
		'...',
    'gunicorn',
)
```

运行测试用例：

```sh
python manage.py test [appname]
```

### Gunicorn

gunicorn.conf.py

```python
import multiprocessing

worker_class = "gevent"
# worker_class = "eventlet"
bind = "127.0.0.1:8000"
workers = 20
proc_name = 'marketserver'
backlog=8192 * 2
loglevel = 'release'
keepalive = 10
timeout= 10
worker_connections=2000
```

运行：
```
gunicorn -c gunicorn.conf.py marketserver.wsgi:application
```

### nginx 

直接用homebrew 安装 nginx，比较方便：

```sh
brew install nginx
```

server配置：

```sh

# user  nobody;
worker_processes  20;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

# pid        logs/nginx.pid;


events {
    worker_connections  4096;    
    use kqueue;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    tcp_nopush     on;

    tcp_nodelay on;

    # keepalive_timeout  0;
    keepalive_timeout  65;
    keepalive_requests 10000;



    #gzip  on;

    upstream market{
        server 127.0.0.1:8000;
        keepalive_timeout  60s;
        keepalive 500;
        keepalive_requests 10000;
    }

    server {
        listen       8080 so_keepalive=on;
        server_name  127.0.0.1;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            proxy_http_version 1.1;
            proxy_pass http://market;
            proxy_set_header Connection "";
            proxy_set_header Host $host;
        }
    }

    include servers/*;
}

```

nginx查看配置文件：

```sh
nginx -t
```

nginx自定义配置文件运行：

```sh
nginx -c xxx.conf
```

nginx停止：

```sh
nginx -s stop
```

### go

go下载地址：https://go.dev/dl/

### redis

```sh
brew install redis
brew services restart redis
```

### 查询 tempwait

```sh
netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'
```

