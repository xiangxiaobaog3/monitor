#-*- coding:utf-8 -*-

__author__='xiangxiaobao'

import os
import sys
import re
import telnetlib
import socket
import time
import commands


class MemcachedStats:

    _client = None
    #_slab_regex = re.compile(ur'STAT items:(.*):number')
    _stat_regex = re.compile(ur"STAT (.*) ([0-9]+\.?[0-9]*)\r")

    def __init__(self, host='127.0.0.1', port='11211'):
        self._host = host
        self._port = port

    @property
    def client(self):
        if self._client is None:
            self._client = telnetlib.Telnet(self._host, self._port)
        return self._client

    def command(self, cmd):
        ' Write a command to telnet and return the response '
        self.client.write("%s\n" % cmd)
        return self.client.read_until('END')

    def close(self):
        'close telnet connection'
        return self.client.write("quit\n")

    #def key_details(self, sort=True, limit=100):
    def stats(self):
        ' Return a dict containing memcached stats '
        return dict(self._stat_regex.findall(self.command('stats')))


def main():

    gauges = [ 'get_hit_ratio', 'incr_hit_ratio', 'decr_hit_ratio', 'delete_hit_ratio', 'usage', 'curr_connections', 'total_connections', 'bytes', 'pointer_size', 'uptime', 'limit_maxbytes', 'threads', 'curr_items', 'total_items', 'connection_structures' ]
    data = []

    conn = MemcachedStats()
    stats = conn.stats()
    conn.close()



    # 分配内存使用率
    stats['usage'] = str(100 * float(stats['bytes'])/ float(stats['limit_maxbytes']))

    # get命令总体命中率
    try:
        stats['get_hit_ratio'] = str(100 * float(stats['get_hits']) / (float(stats['get_hits']) + float(stats['get_misses'])))
    except ZeroDivisionError:
        stats['get_hit_ratio'] = '0.0'

    # incr命令总体命中率
    try:
        stats['incr_hit_ratio'] = str(100 * float(stats['incr_hits']) / (float(stats['incr_hits']) + float(stats['incr_misses'])))
    except ZeroDivisionError:
        stats['incr_hit_ratio'] = '0.0'

    # decr命令总体命中率
    try:
         stats['decr_hit_ratio'] = str(100 * float(stats['decr_hits']) / (float(stats['decr_hits']) + float(stats['decr_misses'])))
    except ZeroDivisionError:
        stats['decr_hit_ratio'] = '0.0'

    # delete命令总体命中率
    try:
         stats['delete_hit_ratio'] = str(100 * float(stats['delete_hits']) / (float(stats['delete_hits']) + float(stats['delete_misses'])))
    except ZeroDivisionError:
        stats['delete_hit_ratio'] = '0.0'


    metric = "memcached"

    for key in stats:
        value = float(stats[key])
        if key in gauges:
            suffix = ''
            vtype = 'GAUGE'
        else:
            suffix = '_cps'
            vtype = 'COUNTER'

        i = {
            'metric': '%s' % key,
            'value': value,
            'counterType': vtype
        }
        data.append(i)

    for index in range(len(data)):
        if data[index]['metric'] == sys.argv[1]:
            print data[index]['value']

main()