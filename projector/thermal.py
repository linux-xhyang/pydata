import random
import pandas
import os

import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

dateparse = lambda x: pandas.datetime.strptime(x, '%Y-%m-%d  %H:%M:%S')


def datetime(x):
    return np.array(x, dtype=np.datetime64)


data = pandas.read_csv(
    "record.txt",
    sep=",",
    date_parser=dateparse,
    parse_dates=['date'],
    dtype={
        'fan1': np.int32,
        'fan2': np.int32,
        'fan3': np.int32,
        'temp0': np.int32,
        'temp1': np.int32,
        'temp2': np.int32,
        'temp3': np.int32
    })
p1 = figure(
    x_axis_type="datetime", title="Stock", plot_width=1000, plot_height=600)

p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Temp&Speed'

p1.line(datetime(data['date']), data['fan1'], color='#A6CEE3', legend='FAN 1')
p1.line(datetime(data['date']), data['fan2'], color='#A6CEE3', legend='FAN 2')
p1.line(datetime(data['date']), data['fan3'], color='#A6CEE3', legend='FAN 3')

p1.line(datetime(data['date']), data['temp0'], color='#000000', legend='环温')
p1.line(datetime(data['date']), data['temp1'], color='#FF0000', legend='色轮')
p1.line(datetime(data['date']), data['temp2'], color='#FFFF00', legend='光源1')
p1.line(datetime(data['date']), data['temp3'], color='#FF00FF', legend='光源2')

show(p1)
