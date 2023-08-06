# niffer-python

# 一、日志收集和事件收集
## 本SDK 日志收集工具在结构上分为两层，第一层为业务属性，第二层为事件属性:properties
```json
{
	"type": "order",
	"time": 1622104453359,
	"distinct_id": "123456",
	"properties": {
		"name": "test_add_event_ConcurrentLoggingConsumer",
		"age": "10",
		"addr": "u5317u4eac",
		"now": "2021-05-27"
	},
	"lib": {
		"$lib": "python",
		"$lib_version": "1.0.1",
		"$lib_method": "code",
		"$lib_detail": "test_add_event_ConcurrentLoggingConsumer##test_add_event_ConcurrentLoggingConsumer##/Users/show/workspace/bluetale/niffer-python/nifflieranalytics/test_sdk.py##113"
	},
	"event_id": "50d0e2d4bec611eb8167acde48001122",
	"project_name": "production",
	"event": "woman_order"
}
```

## 本SDK 仅提供日志收集操作 ，具体用法参见以下 demo code :

### debug 模式调试代码，此模式下，日志信息直接以post形式发送至指定服务器. (_注意此模式不要应用于生产环境_)
````python
# coding=utf-8
from sdk import *


def test_add_log_ConsoleConsumer():
    # 打印日志
    consumer = ConsoleConsumer()
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production')
    properties = {
        'id': 1,
        'name': 'test',
        'age': '10',
        'addr': '北京',
        'time': datetime.datetime.now()

    }
    niffer.add_log(log_type="es", properties=properties)
    niffer.close()


def test_add_log_LoggingConsumer():
    # 打印日志
    # log_name 为log存储的绝对路径+log名称，此路径与filebeat中的配置文件paths要一致
    log_name = "data0/logs/event1.log"
    consumer = LoggingConsumer(log_name)
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production')
    properties = {
        'id': 1,
        'name': 'test',
        'age': '10',
        'addr': '北京',
        'time': datetime.date.today()

    }
    niffer.add_log(log_type="es", properties=properties)
    niffer.close()


def test_add_log_ConcurrentLoggingConsumer():
    # 打印日志
    # log_name 为log存储的绝对路径+log名称，此路径与filebeat中的配置文件paths要一致
    log_name = "/data0/logs/event.log"
    consumer = ConcurrentLoggingConsumer(log_name)
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production')
    properties = {
        'id': 1,
        'name': 'test',
        'age': '10',
        'addr': '北京',
        'time': datetime.date.today()

    }
    niffer.add_log(log_type="", properties=properties)
    niffer.close()


def test_add_event_ConsoleConsumer():
    # 打印日志
    consumer = ConsoleConsumer()
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production')
    properties = {
        'name': 'test_add_event_ConcurrentLoggingConsumer',
        'age': '10',
        'addr': u'北京',
        'now': datetime.date.today()

    }
    distinct_id = '123456'
    event_type = "order"
    event_name = "woman_order"
    niffer.add_event(distinct_id, event_type, event_name, properties)

    niffer.close()


def test_add_event_LoggingConsumer():
    # 打印日志
    # log_name 为log存储的绝对路径+log名称，此路径与filebeat中的配置文件paths要一致
    log_name = "/data0/logs/event1.log"
    consumer = LoggingConsumer(log_name)
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production')
    properties = {
        'name': 'test_add_event_LoggingConsumer',
        'age': '10',
        'addr': u'北京',
        'now': datetime.date.today()
    }
    distinct_id = '123456'
    event_type = "order"
    event_name = "woman_order"
    niffer.add_event(distinct_id, event_type, event_name, properties)
    niffer.close()


def test_add_event_ConcurrentLoggingConsumer():
    # 打印日志
    # log_name 为log存储的绝对路径+log名称，此路径与filebeat中的配置文件paths要一致
    log_name = "/data0/logs/event2.log"
    consumer = ConcurrentLoggingConsumer(log_name, encoding='utf-8')
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production')
    properties = {
        'name': 'test_add_event_ConcurrentLoggingConsumer',
        'age': '10',
        'addr': u'北京',
        'now': datetime.date.today()

    }
    distinct_id = '123456'
    event_type = "order"
    event_name = "woman_order"
    niffer.add_event(distinct_id, event_type, event_name, properties)
    niffer.close()


if __name__ == '__main__':
    # test_add_log_ConsoleConsumer()
    # test_add_log_LoggingConsumer()
    test_add_log_ConcurrentLoggingConsumer()

    # test_add_event_ConsoleConsumer()
    # test_add_event_LoggingConsumer()
    test_add_event_ConcurrentLoggingConsumer()


````

# 二、事件传递到神策

### 1、支持神策的方法
sdk中sensor_开头的方法为神策方法，可通过此方法通过后端将事件传递给神策
``` python
{
    "sensor_track": "track",
    "sensor_item_set": "item_set",
    "sensor_item_delete": "item_delete",
    "sensor_track_signup": "track_signup",
    "sensor_profile_set": "profile_set",
    "sensor_profile_set_once": "profile_set_once",
    "sensor_profile_increment": "profile_increment",
    "sensor_profile_append": "profile_append",
    "sensor_profile_unset": "profile_unset",
    "sensor_profile_delete": "profile_delete",
}
```
### 2、测试样例
调用NifflerAnalytics时必须传sensor_project_name参数，此参数会指定神策的具体项目，
从而将事件信息传递到指定的项目中
```

def test_sensor_track():
    # 打印日志
    # log_name 为log存储的绝对路径+log名称，此路径与filebeat中的配置文件paths要一致
    log_name = "/data0/logs/sensor.log"
    consumer = ConcurrentLoggingConsumer(log_name, encoding='utf-8')
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production', sensor_project_name="production")
    properties = {
        'name': 'test_sensor_track',
        'age': '10',
        'addr': u'北京',
        'now': datetime.date.today()

    }
    distinct_id = '123456'
    event_name = "woman_order"
    niffer.sensor_track(distinct_id, event_name, properties, is_login_id=False)
    niffer.close()
```


### 发送日志数据，程序会自动校验不可使用的关键字及字段名称、长度、类型
`关键字: distinct_id、time、properties、events、event、user_id、date、datetime、type`
`String 类型,长度不应超过 8192 `
`支持的数据类型: string,int64,float64,bool,time.Time,[]string `


### 线上环境中产生的日志，需要单独通过 filebeat 软件监控并增量的传输至kafka ，再由数据团队解析使用， 安装及配置filebeat方式如下:
```
# 1、首先下载 filebeat 软件, 个人偏好下载放置于  /usr/local 内， 方便好找
wget -P /usr/local https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.11.1-linux-x86_64.tar.gz

# 2、解压
tar -xvf filebeat-7.11.1-linux-x86_64.tar.gz

# 3、进入文件夹 ， 修改 filebeat.yml 文件内容为: 
#=========================== Filebeat inputs =============================
filebeat.inputs:
- type: log

  # Change to true to enable this input configuration.
  enabled: true

  # 配置监控的日志地址， 请自行修改监控的日志地址
  # 此路径要与LoggingConsumer、ConcurrentLoggingConsumer中的log_name路径一致
  # 如果只想日志存储到本地，不通过filebeat传递至后端，可不将日志路径添加在此
  paths:
    - /usr/local/log-data/event_log.*
    #- c:\programdata\elasticsearch\logs\*

  close_renamed: true
  clean_removed: true
  close_removed: true

# -------------------------------- Kafka Output -------------------------------
output.kafka:
  # Boolean flag to enable or disable the output module.
  enabled: true

  # 设置 kafka的访问地址， 集群可以设置多个。
  hosts: ["XXX.XXX:9092"]

  # The Kafka topic used for produced events. 
  # 设置kafka 的主题, 需要自行指定
  topic: XXX


#================================ Processors =====================================
# 可以在这里删除一些不需要的字段，
processors:
  - add_host_metadata: ~
  - add_cloud_metadata: ~
  - drop_fields:
     fields: ["beat.hostname", "beat.name", "beat.version", "beat","host","agent","input","ecs","@metadata"]

# ============================= X-Pack Monitoring ==============================
monitoring.enabled: true
monitoring:
  cluster_uuid: "xxx"
  elasticsearch:
    hosts: ["xxx:9200"]

# 4、创建logs文件夹，方便存放 filebaat 日志文件
mkdir logs 

# 5、启动执行
nohup ./filebeat -e -c filebeat.yml >> logs/output.log 2>&1 &
```

