#!/usr/bin/python
import numpy as np

def voltage2temp( voltage ):
    resistor = (voltage/10)/(3.27 - voltage/1000)
    temp = 1/(np.log2(resistor/47)/4050 +1/(25+273.15))-273.15
    #from IPython.core.debugger import Tracer;Tracer()()
    if temp.any() > 0:
        temperature = (temp * 100 + 5)/100
    else:
        temperature = (temp * 100 - 5)/100
    return temperature

print "hello"
voltage2temp(600)

