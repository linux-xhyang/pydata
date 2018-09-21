#!/usr/bin/env python

import cv2 as cv

imgName = "focus_bg.png"
kernel_size = (1, 1)
sigma = 0.8

img = cv.imread(imgName)
dst = cv.GaussianBlur(img, kernel_size, sigma)
dst = cv.Sobel(dst, cv.CV_8UC1, 1, 1, 5)
cv.imshow("gaussian(9,9) sigma 0.8", dst)

kernel_size = (9, 9)
sigma = 3
dst = cv.GaussianBlur(img, kernel_size, sigma)
dst = cv.Sobel(dst, cv.CV_8UC1, 1, 1, 5)
cv.imshow("gaussian(9,9) sigma 3", dst)

kernel_size = (9, 9)
sigma = 8
dst = cv.GaussianBlur(img, kernel_size, sigma)
dst = cv.Sobel(dst, cv.CV_8UC1, 1, 1, 5)
cv.imshow("gaussian(9,9) sigma 8", dst)

cv.waitKey(0)

cv.destroyAllWindows()
