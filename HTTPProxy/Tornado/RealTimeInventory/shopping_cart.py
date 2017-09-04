# -*- coding: utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4

# 维护我们的库存中商品的数量，以及把商品加入购物车的购物者列表
class ShoppingCart(object):
    totalInventory = 10
    callbacks = []
    carts = {}

    def register(self, callback):
        self.callbacks.append(callback)

    def moveItemToCart(self, session):
        if session in self.carts:
            return

        self.carts[session] = True
        self.notifyCallbacks()

    def removeItemFromCart(self, session):
        if session not in self.carts:
            return

        del(self.carts[session])
        self.notifyCallbacks()

    def notifyCallbacks(self):
        for c in self.callbacks:
            self.callbackHelper(c)

        # 通知完成后即长轮询的连接已经关闭，所以必须必须删除已注册的回调函数列表中的函数
        self.callbacks = []

    def callbackHelper(self, callback):
        callback(self.getInventoryCount())

    def getInventoryCount(self):
        return self.totalInventory - len(self.carts)

# 为每个页面产生一个唯一标识符，在每次请求时提供库存数量，并渲染HTML模板
class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        session = uuid4()
        count = self.application.ShoppingCart.getInventoryCount()
        self.render("index.html", session=session, count=count)

# 为浏览器提供了一个API来请求从访客的购物车中添加或删除物品
class CartHandler(tornado.web.RequestHandler):
    def post(self):
        action = self.get_argument('action')
        session = self.get_argument('session')

        if not session:
            self.get_status(400)
            return

        if action == 'add':
            self.application.ShoppingCart.moveItemToCart(session)
        elif action == 'remove':
            self.application.ShoppingCart.removeItemFromCart(session)
        else:
            self.get_status(400)

class StatusHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        # 注册了一个带有购物车控制器的回调函数
        # 使用self.async_callback包住回调函数以确保回调函数中引发的异常不会使RequestHandler关闭连接
        # 然而在1.1之后的版本，这不再是显示必须的了
        self.application.ShoppingCart.register(self.async_callback(self.on_message))

    def on_message(self, count):
        self.write('{"inventoryCount":"%d"' % count)
        self.finish()

class Application(tornado.web.Application):
    def __init__(self):
        self.ShoppingCart = ShoppingCart()

        handlers = [
            (r'/', DetailHandler),
            (r'/cart', CartHandler),
            (r'/cart/status', StatusHandler)
        ]

        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }

        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
