#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import datetime
import getopt
import json
import math
import os
import re
import sys

import pandas as pd

filter_less_distance = 500
filter_greater_time = 4000


class tof_data:
    def __init__(self, sn, date, build_num, temp, distance, step, take_time,
                 ip):
        self.sn = sn
        self.date = date
        self.build_num = build_num
        self.temp = temp
        self.distance = distance
        self.step = step
        self.take_time = take_time
        self.ip = ip

    def to_dict(self):
        return {
            'sn': self.sn,
            'ip': self.ip,
            'date': self.date,
            'build_num': self.build_num,
            'temp': self.temp,
            'distance': self.distance,
            'step': self.step,
            'take_time': self.take_time,
        }


class tof_user:
    def __init__(self, path):
        self.tof_datas = []
        self.count = 0
        fo = open(path, "r")

        for line in fo.readlines():
            data_list = json.loads(line)

            if 'device_pid' in data_list and 'payload' in data_list:
                sn = data_list['device_pid'] + "/" + data_list['device_sn']
                date = pd.to_datetime(data_list['__time__'], unit='s')
                date = date.strftime('%Y-%m-%dT%H:%M:%S')
                payload = json.loads(data_list['payload'])
                temp = ''
                distance = ''
                step = ''
                take_time = ''
                build_num = data_list['fingerprint']
                ip = data_list['real_ip']

                if 'env_temp' in payload:
                    temp = payload['env_temp']

                if 'step' in payload:
                    step = payload['step']

                if 'distance' in payload:
                    distance = payload['distance']
                    if int(distance) <= filter_less_distance:
                        continue

                if 'take_time' in payload:
                    take_time = payload['take_time']
                    if int(take_time) > filter_greater_time:
                        self.count += 1

                self.tof_datas.append(
                    tof_data(sn, date, build_num, temp, distance, step,
                             take_time, ip))

        df = pd.DataFrame.from_records([s.to_dict() for s in self.tof_datas])
        df.to_excel(
            'tof_user.xlsx',
            sheet_name='tof_user',
            engine='openpyxl',
            index=False)
        print("> 4000 : ", self.count)
        print(self.count / len(self.tof_datas), "%")


if __name__ == '__main__':
    inputfile = sys.argv[1]

    print('输入的文件为：', inputfile)
    tof_user(os.path.abspath(inputfile))
