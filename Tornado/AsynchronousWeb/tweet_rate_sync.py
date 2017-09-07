# -*- coding: utf-8 -*-

"""
推率的异步版本
缺点在于，有多个异步请求要执行的时候，需要大量地嵌套调用回调函数
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
define("port", default=8000, help"run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        query = self.get_argument('q')
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch("https://api.twitter.com/1.1/search/tweets.json?" + \
            urllib.urlencode({"q": query, "result_type": "recent", "rpp": 100}),
            callback=self.on_response)

    # 指定on_response方法作为回调函数
    def on_response(self, response):
        body = json.loads(response.body)
        result_count = len(body['results'])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['result'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
            "%a, %d %b %Y %H:%M:%S +0000")
        seconds_diff = time.mktime(now.timetuple()) - time.mktime(oldest_tweet_at.timetuple())
        tweets_per_second = float(result_count) / seconds_diff
        self.write("""
            <div style="text-align: center">
            <div style="font-size: 72px">%s</div>
            <div style="font-size: 144px">%.02f</div>
            <div style="font-size: 24px">tweets per second</div>
            </div>""" % (self.get_argument('q'), tweets_per_second))
        # 使用@tornado.web.asynchonous装饰器时，Tornado永远不会自己关闭连接
        self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.http_server.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance.start
    