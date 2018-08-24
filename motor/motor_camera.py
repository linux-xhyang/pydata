import random
import pandas
import os

import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

big = pandas.read_csv(
    "big.txt", sep=",", dtype={
        'step': np.int32,
        'sharpness': np.float
    })
middle = pandas.read_csv(
    "middle.txt", sep=",", dtype={
        'step': np.int32,
        'sharpness': np.float
    })

less = pandas.read_csv(
    "less.txt", sep=",", dtype={
        'step': np.int32,
        'sharpness': np.float
    })

tooltips = [("(step,sharpness)", "($x, $y)")]

p1 = figure(plot_width=1000, plot_height=1000, tooltips=tooltips)

p1.xaxis.axis_label = 'Step'
p1.yaxis.axis_label = 'Sharpness'

p1.line(big['step'], big['sharpness'], color='#A6CEE3', legend='从左到右')
p1.circle(big['step'], big['sharpness'], fill_color="red", size=4)

p1.line(middle['step'], middle['sharpness'], color='#FFFF00', legend='从右到左')
p1.circle(middle['step'], middle['sharpness'], fill_color="red", size=4)

p1.line(less['step'], less['sharpness'], color='#D6CEE3', legend='从左到右2')
p1.circle(less['step'], less['sharpness'], fill_color="red", size=4)

show(p1)
