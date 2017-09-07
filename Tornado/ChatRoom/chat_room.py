# -*- coding:utf-8 -*-

import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
import uuid

from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

# 用来储存聊天消息和连接到此聊天室的人的信息的类
class MessageBuffer(object):
    def __init__(self):
        self.waiters = set() # 所有被 hold 住的 updates 请求队列
        self.cache = []
        self.cache_size = 200

    def wait_for_messages(self, cursor=None):
        result_future = Future()
        if cursor:
            new_count = 0
            for msg in reversed(self.cache):
                if msg['id'] == cursor:
                    break
                new_count += 1
            if new_count:
                # 返回这些缓存中已有的但对于这个 waiter 来说是新的的数据
                result_future.set_result(self.cache[-new_count:])
                return result_future
        self.waiters.add(result_future)
        return result_future

    def cancel_wait(self, future):
        self.waiters.remove(future)
        future.set_result([])

    def new_messages(self, messages):
        logging.info("Sending new message to %r listeners", len(self.waiters))
        for future in self.waiters:
            # 给所有的等待者返回新消息
            future.set_result(messages)
        # 清空等待者队列
        self.waiters = set()
        # 把消息加到缓存 cache 里
        self.cache.extend(messages)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size]

global_message_buffer = MessageBuffer()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=global_message_buffer.cache)

class MessageNewHandler(tornado.web.RequestHandler):
    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "body": self.get_argument("body")
        }
        # to_basestring is necessary for Python 3's json encoder,
        # which doesn't accept byte strings.
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        global_message_buffer.new_messages([message])

class MessageUpdatesHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        cursor = self.get_argument("cursor", None)
        self.future = global_message_buffer.wait_for_messages(cursor=cursor)
        messages = yield self.future
        if self.request.connection.stream.closed():
            return
        self.write(dict(messages=messages))

    def on_connection_close(self):
        global_message_buffer.cancel_wait(self.future)

def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/a/message/new", MessageNewHandler),
            (r"/a/message/updates", MessageUpdatesHandler),
            ],
        cookie_secret="TODO......",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
        )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
