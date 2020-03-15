import math
import sys

######根据像素个数计算##########
w = 100.0  # mm
f = 1158.2827
delta = (-1.70 * math.pi / 180.0)  # 0.2044
alpha_angle = 23.6

def emu_d():
    compute_d(-177)
    compute_d(-121)
    compute_d(-55)
    compute_d(67)
    compute_d(121)
    compute_d(189)


def emu_theta():
    sample = [5, 6, 7, 9, 10, 11]
    ds = [1100# , 800, 1490, 980
    ]
    tests = [[602, 662, 725, 848, 908, 972],
             # [638, 701, 763, 888, 950, 1013],
             # [579, 638, 699, 821, 883, 944],
             # [607, 671, 735, 863, 927, 991]
    ]

    for (d, test) in zip(ds, tests):
        print("d = ",d)
        for (pi, i) in zip(test, sample):
            compute_theta(640 - pi, i, d)


def compute_d(pi):
    ki = (f*math.tan(delta)-pi)/(f+pi*math.tan(delta))
    d = w/ki
    print("d = ", d)

def compute_theta(pia, i, d):
    print(pia,i,d)
    alpha = (alpha_angle * 2 * math.pi / 180.0)
    g = ((31.2646 / 2) / math.tan(alpha / 2))

    n = 16
    ki = (f*math.tan(delta)-pia)/(f+pia*math.tan(delta))

    x1 = (n * w + ((2 * i - n) * math.tan(alpha / 2) - ki) * g + ((2 * i - n) *
                                                              math.tan(alpha / 2) - n * ki) * d) / ((ki + w) * (2 * i - n) * math.tan(alpha / 2))

    theta = math.atan(x1)
    print('angle theta = ', theta/math.pi*180)
