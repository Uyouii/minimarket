### login 压测数据

```sh
$ ./wrk_login_test.sh
Running 50s test @ http://127.0.0.1:8080/auth/login/
  16 threads and 64 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    15.74ms   10.94ms 312.23ms   90.71%
    Req/Sec   269.04     36.42   646.00     75.34%
  Latency Distribution
     50%   13.68ms
     75%   18.14ms
     90%   24.48ms
     99%   52.32ms
  214578 requests in 50.08s, 64.86MB read
Requests/sec:   4284.61
Transfer/sec:      1.30MB
```

- **压测工具** : wrk
- **压测脚本**: [login.lua](https://github.com/Uyouii/minimarket/blob/master/test/wrk_test/login.lua)

- **随机用户数量**：400
- **压测时间**：10.08s
- **成功请求总量**：38432
- **平均速度**：4284.61/ s
- **平均带宽**：1.30MB / s
- **CPU占用**：Apple M1 Pro 10核 97.94%
- **内存占用**：15G （PC 内存16G）

- **性能记录**：

```sh
Processes: 517 total, 13 running, 504 sleeping, 3740 threads                  11:33:03
Load Avg: 13.11, 8.75, 7.09  CPU usage: 56.79% user, 41.15% sys, 2.4% idle
SharedLibs: 388M resident, 86M data, 25M linkedit.
MemRegions: 329045 total, 2428M resident, 106M private, 1416M shared.
PhysMem: 15G used (2242M wired), 69M unused.
VM: 192T vsize, 3778M framework vsize, 27958148(0) swapins, 28527277(0) swapouts.
Networks: packets: 737366265/115G in, 722299053/101G out.
Disks: 19768232/703G read, 26549949/929G written.

PID    COMMAND      %CPU  TIME     #TH    #WQ  #PORT MEM    PURG   CMPRS  PGRP  PPID
1042   com.crowdstr 161.2 02:48:17 28/3   8/2  257   368M   0B     283M+  1042  1
355    mysqld       99.5  06:36:44 92/14  0    118   403M   0B     351M-  355   1
63432  Python       82.6  00:12.61 2/1    0    31    45M+   0B     9940K- 63418 63419
63435  Python       78.9  00:06.59 2/1    0    31    42M+   0B     11M    63418 63419
63440  Python       70.9  00:15.95 2/1    0    31    47M    0B     13M-   63418 63419
0      kernel_task  64.5  18:10:49 591/11 0    0     240M   0B     0B     0     0
63447  authserver   54.7  00:18.64 20/2   0    40    43M    0B     6848K  63447 59875
648    iTerm2       53.7  08:15:00 11     8    472   468M-  64K+   93M    648   1
63431  Python       47.9  00:15.03 2      0    31    43M    0B     11M-   63418 63419
370    WindowServer 43.1  16:18:28 24/2   6    3662  1329M+ 1632K- 401M   370   1
63425  Python       28.1  00:10.23 2      0    31    48M    0B     10M-   63418 63419
63427  Python       20.6  00:09.36 2/1    0    31    41M    0B     12M    63418 63419
63436  Python       19.9  00:05.20 2      0    31    39M+   0B     25M-   63418 63419
23112  SeaTalk Help 16.9  10:38:52 23     1    251   1360M  0B     1284M- 23063 23063
63433  Python       12.2  00:08.11 2      0    31    41M    0B     27M-   63418 63419
651    NeteaseMusic 10.8  24:17.13 28     11   598   137M+  96K    93M    651   1
```

