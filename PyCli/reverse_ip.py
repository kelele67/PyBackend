# Reverse IP Lookup By: Joinse7en

import urllib2, urllib, sys, json
from optparse import OptionParser

url = "http://domains.yougetsignal.com/domains.php"

contenttype = "application/x-www-form-urlencoded; charset=UTF-8"

def banner():
    print """
+-----------------------------------+
|         Reverse IP Lookup         |
|           By: Kelele67            |
+-----------------------------------+"""

def parseArgs():
    # optionparser is kinda gay, will probaly change ??
    parser = OptionParser()

    parser.add_option("-t", "--target", dest="target",
                      help="Domain or IP to reverse IP lookup", metavar="TARGET")

    parser.add_option("-p", "--proxy", dest="proxy",
                      help="HTTPS proxy to use", metavar="PROXY")

    parser.add_option("-a", "--agent", dest="agent",
                      help="Custom User Agent", metavar="AGENT")

    return parser

def request(target, httpsproxy=None, useragent=None):
    global contenttype

    if not useragent:
        useragent = "Mozilla/5.0 (X11; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0 Iceweasel/22.0"
    else:
        print "User-Agent: " + useragent

    if httpsproxy:
        print "Proxy: " + httpsproxy + "\n"
        opener = urllib2.build_opener(
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.ProxyHandler({'http': 'http://' + httpsproxy}))
        urllib2.install_opener(opener)

    postdata = [('remoteAddress', target), ('key', '')]
    postdata = urllib.urlencode(postdata)

    request = urllib2.Request(url, postdata)

    request.add_header("Content-type", contenttype)
    request.add_header("User-Agent", useragent)
    try:
        result = urllib2.urlopen(request).read()
    except urllib2.HTTPError, e:
        print "Error" + str(e.code)
    except urllib2.URLError, e:
        print "Error" + str(e.args)

    obj = json.loads(result)
    return obj

def output(obj):
    print "Status" + obj["status"]
    if obj["status"] == "Fail":
        message = obj["message"].split(". ")
        print "Error:    " + message[0] + "."
        sys.exit(1)

    print "Domains:    " + obj["domainCount"]
    print "Target:     " + obj["remoteAddress"]
    print "Target IP:  " + obj["remoteIpAddress"]
    print "\n" + "Results:"

    for domain, hl in obj["domainArray"]:
        print domain

def main():
    banner()
    parser = parseArgs()
    (options, args) = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        print "Examples:\n"
        print sys.argv[0] + " --target domain.com"
        print sys.argv[0] + " --target domain.com --proxy 192.168.0.1:8080"
        print sys.argv[0] + " --target domain.com --agent \"Googlebot/2.1 (+http://www.googlebot.com/bot.html)\""

        sys.exit()

    target = options.target
    print "\n"
    obj = request(target, options.proxy, options.agent)
    output(obj)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "KeyboardInterrupt detected!\nBye~"
        sys.exit()
