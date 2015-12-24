# openslack日志收集和时时监控系统

## 技术选型和想法如下
### agent组件： flume、colectd、logstash、Heka、statsd、fluentd等数据收集通过gateway上报到当前IDC的kafka，
### gateway可以作为中转地支持socket、rpc、http、thrift等方式数据上报到当前IDC的kafka，此处可以集群，避免单点。
### gateway可以作为consumer把当前IDC的kafka数据上报到到中心IDC的kafka。所以gateway每个数据中心都有
### consumer(transfer)负责消费kafka到存储、告警，此处也可以分布式
###
### elk 搜索日志
### spark、esper、storm等对日志类型的流式数据聚合和规则判断，
### influxdb/opentsdb/graphite做时间序列数据存储
### Grafana前端展示
### open-falcon可以借鉴
