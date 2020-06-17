import datetime
import math
import os
import re

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


def backstep_check():
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    df = pd.read_excel("/home/xhyang/Documents/TOF/135/工厂回程差/回程差统计.xlsx")
    heads = df.columns.values
    s_backsteps = []
    d_backsteps = []

    for i in df.index.values:
        row_data = df.ix[i, ['广景测试回程差', '工厂测试回程差']]
        if row_data['广景测试回程差'] != None:
            if math.isnan(row_data['广景测试回程差']):
                s_backsteps.append(0)
            else:
                s_backsteps.append(row_data['广景测试回程差'])

        if row_data['工厂测试回程差'] != None:
            if math.isnan(row_data['工厂测试回程差']):
                d_backsteps.append(0)
            else:
                d_backsteps.append(row_data['工厂测试回程差'])

    df_backstep = pd.DataFrame({
        u'广景测试回程差': s_backsteps,
        u'工厂测试回程差': d_backsteps
    },
                               columns=[u'广景测试回程差', u'工厂测试回程差'])

    bins = [0, 60, 100, 140]
    labels = ["0-60", "61-100", "101-140"]

    df_backstep.plot(alpha=0.4, kind='hist', bins=40, stacked=False)
    plt.show()


backstep_check()
