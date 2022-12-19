ulimit -n 65535
wrk -t16 -c64 -d50s --script=login.lua --latency http://127.0.0.1:8080/auth/login/