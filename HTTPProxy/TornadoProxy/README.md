# Tornado Proxy

## 应用场景

第一个是爬虫代理，我可以在N个公网vps上，部署toproxy http 代理，然后我的主调度器只需要加入proxy server就可以实现同步调用了。

第二个场景是翻墙上网，我可以翻墙去浏览国内无法访问的页面，比如xxx，你懂的. 

## 原理
你通过http client附加proxy地址访问页面，我通常会解析你的访问，然后我自己再去访问你刚才提交的页面，然后返回你结果。
当然在协议上来说，这虽然不是最高性能的方法，但是最简单有效的方法....  如果是底层的socket来写，我首先需要解析你的各种各样的header请求，然后还要考虑多任务的模块，或 prefork 或 异步模式， 这都是开发的成本。    我这里是用tornado这异步框架，本身解决了各个流程的堵塞问题，然又用异步的 httpclient,避免了我请求url时的堵塞。 

## New Future

1. 加入了白名单功能

2. 当访问的地址连接失败的时候，会做重试机制

3. support 301 redirect

4. 加入了基本认证

5. 简单防御

## 直接使用
    ```python
    python toproxy/proxy.py -h

    usage: proxy.py [-h] [-p PORT] [-w WHITE] [-u USER]
    
    python -m toproxy/proxy -p 8888 -w 127.0.0.1,8.8.8.8 -u xiaorui:fengyun
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PORT, --port PORT  tonado proxy listen port
      -w WHITE, --white WHITE
                            white ip list ---> 127.0.0.1,215.8.1.3
      -u USER, --user USER  Base Auth , xiaoming:123123
    ```

    第一个参数是端口，第二个参数是白名单ip地址。 
    方法1:
    python  -m toproxy/proxy -p 8888 -w 127.0.0.1 -u xiaorui:123
    python  -m toproxy/proxy
    ::::Starting HTTP proxy on port 8888

### test

    curl -vvv -x xiaorui.cc:8888 http://www.google.com

    ab -X xiaorui.cc:8888 -c 200 -n 1000 http://www.hao123.com/ 
    
    ```
    his is ApacheBench, Version 2.3 <$Revision: 655654 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/
    
    Benchmarking www.hao123.com (be patient)
    Completed 100 requests
    Completed 200 requests
    Completed 300 requests
    Completed 400 requests
    Completed 500 requests
    Completed 600 requests
    Completed 700 requests
    Completed 800 requests
    Completed 900 requests
    Completed 1000 requests
    Finished 1000 requests
    
    
    Server Software:        BWS/1.0
    Server Hostname:        www.hao123.com
    Server Port:            80
    
    Document Path:          /
    Document Length:        750380 bytes
    
    Concurrency Level:      200
    Time taken for tests:   7.967 seconds
    Complete requests:      1000
    Failed requests:        10
       (Connect: 0, Receive: 0, Length: 10, Exceptions: 0)
    Write errors:           0
    Total transferred:      752184936 bytes
    HTML transferred:       751671400 bytes
    Requests per second:    125.52 [#/sec] (mean)
    Time per request:       1593.406 [ms] (mean)
    Time per request:       7.967 [ms] (mean, across all concurrent requests)
    Transfer rate:          92199.44 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:       24   40  94.6     31    1034
    Processing:   289 1371 786.8   1223    4028
    Waiting:       46   57  27.8     55     663
    Total:        317 1411 791.2   1276    4059
    
    Percentage of the requests served within a certain time (ms)
      50%   1276
      66%   1751
      75%   2030
      80%   2208
      90%   2510
      95%   2768
      98%   3187
      99%   3389
     100%   4059 (longest request)
    ```
