# -*- coding: utf-8 -*-

import os
import time
import logging
import select
import functools

import timerstack

# 设置日志权限 DEBUG < INFO < WARNING < ERROR < CRITICAL
logging.basicConfig(level=logging.INFO)
# 创建Logger对象
logger = logging.getLogger(__name__)

func_map = {}

def go(*args):
    logger.info(args)

def run(inputs):
    outputs = []
    try:
        # 创建 epoll 句柄
        epoll_fd = select.epoll()
        # 向 epoll 句柄中注册监听 socket 的可读事件
        for ff in inputs:
            epoll_fd.register(ff, select.EPOLLIN)
    except select.error, msg:
        logger.error(msg)

    while True:
        epoll_list = epoll_fd.poll()
        for fd, events in epoll_list:
            func_map[fd]()

def io_select():
    while inputs:
        # select()方法接收并监控3个通信列表， 
        # 第一个是所有的输入的data,就是指外部发过来的数据，
        # 第2个是监控和接收所有要发出去的data(outgoing data),
        # 第3个监控错误信息
        # 返回3个新的list，将他们分别赋值为readable, writable, exceptional
        readable, writable, exceptional = select.select(inputs, outputs, inputs, 0.1)
        # 1. readable list 中的socket 可以有3种可能状态
        # 第一种是如果这个socket是main "server" socket,它负责监听客户端的连接，如果这个main server socket出现在readable里，那代表这是server端已经ready来接收一个新的连接进来了，为了让这个main server能同时处理多个连接，在下面的代码里，我们把这个main server的socket设置为非阻塞模式
        # 第二种情况是这个socket是已经建立了的连接，它把数据发了过来，这个时候你就可以通过recv()来接收它发过来的数据，然后把接收到的数据放到queue里，这样你就可以把接收到的数据再传回给客户端了
        # 第三种情况就是这个客户端已经断开了，所以你再通过recv()接收到的数据就为空了，所以这个时候你就可以把这个跟客户端的连接关闭了
        # 2. 对于writable list中的socket，也有几种状态，如果这个客户端连接在跟它对应的queue里有数据，就把这个数据取出来再发回给这个客户端，否则就把这个连接从output list中移除，这样下一次循环select()调用时检测到outputs list中没有这个连接，那就会认为这个连接还处于非活动状态
        # 3. 最后，如果在跟某个socket连接通信过程中出了错误，就把这个连接对象在inputs\outputs\message_queue中都删除，再把连接关闭掉
        for s in readable:
            os.read(s, 1024)
            func_map[s](123)

def test():
    for i in range(100000):
        i += 10
        f = timerstack.create(timerstack.CLOCK_REALTIME, 0)
        timerstack.settime(f, 0, i, i)
        # 飘逸的把key:时间 + value:logger.info(i) 放进map
        func_map[f] = functools.partial(go, i)

    f = timerstack.create(timerstack.CLOCK_REALTIME, 0)
    timerstack.settime(f, 0, 10, 0) # only once
    func_map[f] = functools.partial(go, i)
    run(func_map.keys())
    
if __name__ == "__main__":
    test()