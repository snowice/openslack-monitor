### 提供数据的采集，可以用多种插件,比如logstash,flume
### 自带Heartbeat. 所有Agent都会连到etcd，每分钟发一次心跳，汇报自己的hostname、ip、agent version、plugin version，据此 填充host表。
### agent还会通过etcd拿到应该监控的端口、进程，应该执行的插件等信息。
### apent动态从etcd。如此一来，agent可以每分钟从etcd读取一次数据。
