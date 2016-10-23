zabbix script memcached监控脚本
================================

主要逻辑
--------------------------------
使用telnet stat获取并解析相关数据

汇报字段
--------------------------------
所有memcached stats字段（pid，time除外）均汇报，除此之外，增加了以下原值：

| key |  tag | type | note |
|-----|------|------|------|
memcached.get_hit_ratio|port(实例端口号)|GAUGE|get命令总体命中率|
memcached.incr_hit_ratio|port(实例端口号)|GAUGE|incr命令总体命中率|
memcached.decr_hit_ratio|port(实例端口号)|GAUGE|decr命令总体命中率|
memcached.delete_hit_ratio|port(实例端口号)|GAUGE|delete命令总体命中率|
memcached.usage|port(实例端口号)|GAUGE|分配内存使用率，等于byte/limitmaxbyte|