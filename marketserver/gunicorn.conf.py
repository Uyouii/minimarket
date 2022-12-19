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