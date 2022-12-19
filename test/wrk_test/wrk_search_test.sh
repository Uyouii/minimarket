ulimit -n 65535
wrk -t4 -c12 -d10s --script=searchname.lua --latency http://127.0.0.1:8080/product/searchname/