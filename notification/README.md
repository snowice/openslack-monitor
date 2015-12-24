# openslack告警通知组件

## 以下这些交由celery异步执行，队列为rabbitmq
- judge把报警event交由celery异步执行，
- celery读取event，做相应处理，可能是发报警短信、邮件，可能是callback某个http地址。
- celery会专门负责来发送。
- alarm处理报警event可能会产生报警短信或者报警邮件，并把报警邮件、短信写入celery队列，celery的worker负责读取并发送。

## 这个里面有两个worker
- 处理event，可能会产生邮件内容或者短信内容，也可能是回调或者请求。制作判断和产生内容，不做处理
- 处理这些结果，同时处理这些结果，可能产生mail、http、callback等队列

