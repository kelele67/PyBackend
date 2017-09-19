# -*- coding:utf-8 -*-
"""
扫描固定端口的小工具
接收参数：
起始IP，终止IP，目标端口
"""
import socket, time, sys

def banner():
    print """+-----------------------------------+
|      IP Segment Port Scanner      |
|           By: Kelele67            |
+-----------------------------------+"""

def portScanner(ip, port):
    server = (ip, port)
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd.settimeout(0.1)
    ret = sockfd.connect_ex(server) # 返回0则成功
    if not ret:
        sockfd.close()
        print "%s:%s is opened..." % (ip, port)
    
    else:
        sockfd.close()
        print "%s:%s is closed..." % (ip, port) 

def ip2num(ip):
    lp = map(int, ip.split('.'))
    return lp[0] << 24 | lp[1] << 16 | lp[2] << 8 | lp[3]

def num2ip(num):
    ip = [''] * 4
    ip[3] = (num & 0xff)
    ip[2] = (num & 0xff00) >> 8
    ip[1] = (num & 0xff0000) >> 16
    ip[0] = (num & 0xff000000) >> 24
    return ".".join(str(x) for x in ip)

if __name__ == "__main__":
    print "start time : %s" % time.ctime(time.time())
    banner()

    if len(sys.argv) < 4:
        print "Usage: %s [startip] [endip] [port]" % sys.argv[0]
        sys.exit()
    startip = sys.argv[1]
    endip = sys.argv[2]
    port = int(sys.argv[3])

    diff = ip2num(endip) - ip2num(startip)
    if diff < 0:
        print "endip must be bigger than startip"
        sys.exit()
    elif diff == 0:
        portScanner(startip, port)
    else:
        startipnum = ip2num(startip)
        for i in xrange(diff + 1):
            portScanner(num2ip(startipnum), port)
            startipnum = startipnum + 1
    print "end time   : %s" % time.ctime(time.time())