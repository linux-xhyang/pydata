import pandas

import numpy as np

from bokeh.plotting import figure, show

normal_inc = pandas.read_csv(
    "normal_inc.txt", sep=",", dtype={
        'step': np.int32,
        'sharpness': np.float
    })
normal_dec = pandas.read_csv(
    "normal_dec.txt", sep=",", dtype={
        'step': np.int32,
        'sharpness': np.float
    })

reverse_inc = pandas.read_csv(
    "reverse_inc.txt", sep=",", dtype={
        'step': np.int32,
        'sharpness': np.float
    })

reverse_dec = pandas.read_csv(
    "reverse_dec.txt", sep=",", dtype={
        'step': np.int32,
        'sharpness': np.float
    })

tooltips = [("(step,sharpness)", "($x, $y)")]

p1 = figure(plot_width=1000, plot_height=1000, tooltips=tooltips)

p1.xaxis.axis_label = 'Step'
p1.yaxis.axis_label = 'Sharpness'

p1.line(normal_inc['step'], normal_inc['sharpness'], color='#A6CEE3', legend='正常机台正转')
p1.circle(normal_inc['step'], normal_inc['sharpness'], fill_color="red", size=4)

p1.line(normal_dec['step'], normal_dec['sharpness'], color='#BFFF00', legend='正常机台反转')
p1.circle(normal_dec['step'], normal_dec['sharpness'], fill_color="red", size=4)

p1.line(reverse_inc['step'], reverse_inc['sharpness'], color='#E6CEE3', legend='异常机台正转')
p1.circle(reverse_inc['step'], reverse_inc['sharpness'], fill_color="red", size=4)

p1.line(reverse_dec['step'], reverse_dec['sharpness'], color='#FFFF00', legend='异常机台反转')
p1.circle(reverse_dec['step'], reverse_dec['sharpness'], fill_color="red", size=4)

show(p1)
