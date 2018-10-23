import cv2
import numpy as np
from matplotlib import pyplot as plt

#img = cv2.imread("/home/xhyang/src/pydata/fft/letters/fft1.jpg", 0)
#img = cv2.imread("/home/xhyang/src/pydata/fft/letters/sin3.png", 0)
img = cv2.imread("/home/xhyang/src/pydata/fft/letters/sin1.png", 0)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)

magnitude_spectrum = 20 * np.log(np.abs(fshift))
magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.uint8)
img_and_magnitude = np.concatenate((img, magnitude_spectrum), axis=1)

plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()
