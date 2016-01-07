### 提供数据的采集，可以用多种插件,比如logstash,flume
### 自带Heartbeat. 所有Agent都会连到etcd，每分钟发一次心跳，汇报自己的hostname、ip、agent version、plugin version，据此 填充host表。
### agent还会通过etcd拿到应该监控的端口、进程，应该执行的插件等信息。
### apent动态从etcd。如此一来，agent可以每分钟从etcd读取一次数据。



每台机器上会有一个Agent去同步这些日志，这是个典型的队列模型，业务进程在不断的push，Agent在不停地pop。
Agent需要有记忆功能，用来保存同步的位置（offset），这样才尽可能保证数据准确性，但不可能做到完全准确。由于发送数据和保存offset是两个动作，不具有事务性，
不可避免的会出现数据不一致性情况，通常是发送成功后保存offset，那么在Agent异常退出或机器断电时可能会造成多余的数据。 Agent需要足够轻，这主要体现在运维和逻辑两个方面。
Agent在每台机器上都会部署，运维成本、接入成本是需要考虑的。
Agent不应该有解析日志、过滤、统计等动作，这些逻辑应该给数据消费者。倘若Agent有较多的逻辑，那它是不可完成的，不可避免的经常会有升级变更动作。

数据收集这块的技术选择，Agent是用Go自己研发的，消息中间件Kafka，数据传输工具Flume。说到数据收集经常有人拿Flume和Kafka做比较，我看来这两者定位是不同的，Flume更倾向于数据传输本身，Kakfa是典型的消息中间件用于解耦生产者消费者。

 

具体架构上，Agent并没把数据直接发送到Kafka，在Kafka前面有层由Flume构成的forward。这样做有两个原因：

Kafka的API对非JVM系的语言支持很不友好，forward对外提供更加通用的HTTP接口。
forward层可以做路由、Kafka topic和Kafka partition key等逻辑，进一步减少Agent端的逻辑。
 

forward层不含状态，完全可以做到水平扩展，不用担心成为瓶颈。出于高可用考虑，forward通常不止一个实例，这会带来日志顺序问题，Agent按一定规则（round-robin、failover等）来选择forward实例，即使Kafka partition key一样，由于forward层的存在，最终落入Kafka的数据顺序和Agent发送的顺序可能会不一样。我们对乱序是容忍的，因为产生日志的业务基本是分布式的，保证单台机器的日志顺序意义不大。如果业务对顺序性有要求，那得把数据直接发到Kafka，并选择好partition key，Kafka只能保证partition级的顺序性。

 

多机房的情形，通过上述流程，先把数据汇到本地机房Kafka集群，然后汇聚到核心机房的Kafka，最终供消费者使用。由于Kafka的mirror对网络不友好，这里我们选择更加的简单的Flume去完成跨机房的数据传送。