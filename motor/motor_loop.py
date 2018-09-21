import random
import pandas
import os

import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

inc0 = pandas.read_csv(
    "inc_0.txt", sep=",", dtype={
        'step': np.int32,
        'sharpness': np.float
    })
dec0 = pandas.read_csv(
    "dec_0.txt", sep=",", dtype={
        'step': np.int32,
        'sharpness': np.float
    })

inc1 = pandas.read_csv(
    "inc_1.txt", sep=",", dtype={
        'step': np.int32,
        'sharpness': np.float
    })

dec1 = pandas.read_csv(
    "dec_1.txt", sep=",", dtype={
        'step': np.int32,
        'sharpness': np.float
    })

tooltips = [("(step,sharpness)", "($x, $y)")]

p1 = figure(plot_width=1000, plot_height=1000, tooltips=tooltips)

p1.xaxis.axis_label = 'Step'
p1.yaxis.axis_label = 'Sharpness'

p1.line(inc0['step'], inc0['sharpness'], color='black', legend='从左到右')
p1.circle(inc0['step'], inc0['sharpness'], fill_color="red", size=4)

p1.line(dec0['step'], dec0['sharpness'], color='blue', legend='从右到左')
p1.circle(dec0['step'], dec0['sharpness'], fill_color="red", size=4)

p1.line(inc1['step'], inc1['sharpness'], color='green', legend='从左到右2')
p1.circle(inc1['step'], inc1['sharpness'], fill_color="red", size=4)

p1.line(dec1['step'], dec1['sharpness'], color='yellow', legend='从右到左2')
p1.circle(dec1['step'], dec1['sharpness'], fill_color="red", size=4)

show(p1)
