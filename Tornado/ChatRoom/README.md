## ChatRoom

实现了一个 使用 长轮询(long polling) 的AJAX聊天室. 

长轮询的可能想要覆盖 on_connection_close() 来在客户端关闭连接之后进行清理

### 获取新消息的原理

1、在 chat.js 中有一个定时器会定时执行 update 操作
2、当没有新消息时 tornado 会一直 hold 住 chat.js 发来的 update 请求
3、当有新消息时 tornado 将包含新消息的数据返回给所有 hold 的 update 请求
4、此时 chat.js 收到 update 回复后更新返回数据在聊天室中，同时再进行一次 update 请求， 然后又从 1. 开始执行。

### 发送新消息的原理

1、输入消息， 点击 post 按钮， chat.js 获取表单后用 ajax 方式发送请求 new
2、tornado 收到请求 new ，返回消息本身， 同时通知所有 hold 住的 update 请求 ( 这里也包括发送 new 请求的 chat.js 所发送的 update 请求 ) 返回新消息
3、所有在线的 chat.js 收到 update 请求回复，更新返回信息到聊天室，同时再进行一次 update 请求。