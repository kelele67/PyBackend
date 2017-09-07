# -*- coding: utf-8 -*-

"""
推率的同步版本
"""
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import urllib
import json
import datetime
import time

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

# 处理到应用根路径请求的IndexHandler
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_argument('q')
        # 实例化了一个Tornado的HTTPClient类
        client = tornado.httpclient.HTTPClient()
        # rpp参数指定我们想获得搜索结果首页的100个推文
        # 而result_type参数指定我们只想获得匹配搜索的最近推文
        # new API https://api.twitter.com/1.1/search/tweets.json
        response = client.fetch("https://api.twitter.com/1.1/search/tweets.json?" + urllib.urlencode({"q": query, "result_type": "recent", "rpp": 100}))
        body = json.loads(response.body)
        result_count = len(body['result'])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['result'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at, "%a, %d %b %Y %H:%M:%S +0000")
        seconds_diff = time.mktime(now.timetuple()) - \
                    time.mktime(oldest_tweet_at.timetuple())
        tweets_per_second = float(result_count) / seconds_diff
        self.write("""
            <div style="text-align: center">
            <div style="font-size: 72px">%s</div>
            <div style="font-size: 144px">%.02f</div>
            <div style="font-size: 24px">tweets per second</div>
            </div>""" % (query, tweets_per_second))

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
