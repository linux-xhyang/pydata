import colorsys
import glob
import os
import random

import numpy as np
import pandas
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show

tooltips = [("(time,sharpness)", "($x, $y)")]
p1 = figure(plot_width=1000, plot_height=1000, tooltips=tooltips)
p1.xaxis.axis_label = 'Time'
p1.yaxis.axis_label = 'Sharpness'
mean = [['文件','开机一分钟平均值','最后一分钟平均值','热失焦损失','热失焦损失占比','平均值','标准偏差',]]
writer = pandas.ExcelWriter("/home/xhyang/src/pydata/motor/热失焦统计.xlsx")

def _get_colors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        (red, green, blue) = colorsys.hls_to_rgb(hue, lightness, saturation)
        colors.append('#%02x%02x%02x' % (int(red * 255), int(green * 255), int(blue * 255)))

    return colors

def _get_thermal_files():
    return glob.glob("/home/xhyang/Downloads/autofocus_thermal/autofocus*.txt");

def _plot_thermal(file,color):
    thermal = pandas.read_csv(
        file,
        sep=",",
        dtype={
            'time': np.int32,
            'sharpness': np.float
        })

    p1.line(thermal['time'], thermal['sharpness'], color=color)
    #p1.circle(thermal['time'], thermal['sharpness'], fill_color="red", size=4)
    arr = np.array(thermal['sharpness'])
    return [os.path.basename(file),
            np.mean(arr[:6]),#开机已分一分钟平均值
            np.mean(arr[len(arr) - 6:-1]),#最后一分钟平均值
            np.mean(arr[:6]) - np.mean(arr[len(arr) - 6:-1]), #热失焦损失
            (np.mean(arr[:6]) - np.mean(arr[len(arr) - 6:-1])) / np.mean(arr[:6]), #热失焦损失占比
            np.mean(arr), #平均值
            np.sqrt(np.var(arr)) #标准偏差
    ]

def _main_():
    files = _get_thermal_files()
    colors = _get_colors(20)
    for file,color in zip(files,colors):
        mean.append(_plot_thermal(file,color))

_main_()
show(p1)
pdsum = pandas.DataFrame(mean)
pdsum.to_excel(excel_writer=writer)
writer.save()
writer.close()
