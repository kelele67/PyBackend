## RealTimeInventory

## 使用Tornado进行长轮询

在前端使用像JavaScript这样的工具处理异步应用，让客户端承担更多工作，以提高你应用的扩展性

## 实时库存报告

这个例子演示了一个根据多个购物者浏览器更新的零售商库存实时计数服务。这个应用提供一个带有"Add to Cart"按钮的HTML书籍细节页面，以及书籍剩余库存的计数。一个购物者将书籍添加到购物车之后，其他访问这个站点的访客可以立刻看到库存的减少。

## 长轮询的缺陷

当使用长轮询开发应用时，记住对于浏览器请求超时间隔无法控制是非常重要的。由浏览器决定在任何中断情况下重新开启HTTP连接。另一个潜在的问题是许多浏览器限制了对于打开的特定主机的并发请求数量。当有一个连接保持空闲时，剩下的用来下载网站内容的请求数量就会有限制。