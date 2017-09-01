# EpollfdTimer

Python基于linux timerfd实现的定时器模块. 使用Epoll来监听调度timerfd.

## timerstack.c
参照[linux timerfd api](http://man7.org/linux/man-pages/man2/timerfd_create.2.html)，用PyObject封装了timerfd的c api, 因为python标准库里不存在timerfd定时接口

## Examples

timerstack.create():   创建一个相对时间的定时器fd
timerstack.settime():  设置新旧时间，可以简单理解为间隔时间和次数.
timerstack.gettime():  查看模式

```python
import timerstack,os
f = timerstack.create(timerfd.CLOCK_REALTIME,0)
timerstack.settime(f,0,10,0)     #单次 10s 
timerstack.settime(f,0,0,0)      #停止 
timerstack.settime(f,0,5,5)      #每5秒钟轮一次,次数不限制
os.read(f,1024)
```
---

## Test

```shell
python setup.py install
```
---

```shell
python epollfd_timer.py
```
---
