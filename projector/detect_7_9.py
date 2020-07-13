import os
import math
import cv2
import numpy as np

src_dir = os.path.split(os.path.realpath(__file__))[0] + "\\"

N = 16
F = 1158
W = 100
JK = 31.2646
G = JK / 2 / math.tan(44.4 * (math.pi/180) / 2) # 38.305781820952646

names = []
deltas = []
angles = []
distances = []
pis = []

cnrx, cnry = 15, 8

flags = 0
flags |= cv2.CALIB_CB_ADAPTIVE_THRESH
flags |= cv2.CALIB_CB_FAST_CHECK
flags |= cv2.CALIB_CB_NORMALIZE_IMAGE

def _find_corners(gray, cnrx, cnry):
    ret, corners = cv2.findChessboardCorners(gray, (cnrx, cnry), flags=flags)
    if not ret:
        gray = 255 - gray
        ret, corners = cv2.findChessboardCorners(gray, (cnrx, cnry), flags=flags)
    if ret:
        cv2.cornerSubPix(gray, corners, (cnrx, cnry), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01))
    return ret, corners

def find_corners(img_name):
    image = cv2.imread(src_dir + img_name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # gray= cv2.medianBlur(gray,5)
    if img_name == '0.5-+15.jpg':
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(7, 7))
        clahe = cv2.createCLAHE(clipLimit=2., tileGridSize=(8, 8))
        hist = clahe.apply(gray)

        hist = cv2.morphologyEx(hist, cv2.MORPH_CLOSE, kernel)
        gray = cv2.morphologyEx(hist, cv2.MORPH_OPEN, kernel)

    for n in range(3):
        ret, corners = _find_corners(gray, cnrx - n, cnry)
        if ret:
            cv2.drawChessboardCorners(image, (cnrx - n, cnry), corners, ret)
            break

    # print(img_name)
    # cv2.imshow("hist",hist)
    # cv2.imshow("img", image)
    # cv2.waitKey(0)

    return ret, corners


with open(src_dir + 'src_data.txt', 'r') as f:
    for i, line in enumerate(f.readlines()):
        if i == 0: continue
        
        ls = line.strip().split('\t')
        ret, corners = find_corners(ls[0])
        if ret:
            n = len(corners) // 8
            pi_list = []
            for j in range(0, n, 1):
                pi_list.append(640 - corners[n*7 + j][0][0])
                # print(corners[15*3 + j - 1][0][0])
            # print(pi_list)
            pis.append(pi_list)
            names.append(ls[0])
            angles.append(int(ls[1]))
            distances.append(float(ls[2]) * 1000)
# print(pis[0])
# print(angles)
# exit()

def calculate_delta(index):
    # tan_delta = (W / distances[index] * F + pis[index][7]) / (F + W / distances[index] * pis[index][7])
    tan_delta =  (pis[index][7] + W*F / distances[index]) / (F - pis[index][7]*W / distances[index])
    delta = math.atan(tan_delta)
    return delta * (180 / math.pi)

def calculate_alpha(index, i):
    _delta = delta * (math.pi / 180)
    K = (F*math.tan(_delta) - pis[index][i-1]) / (F + pis[index][i-1]*math.tan(_delta))

    tan_alpha_2 = (K * G + N * K * distances[index] - N * W) / ((2 * i - N) * (G + distances[index]))
    alpha = math.atan(tan_alpha_2) * 2
    return alpha * (180 / math.pi)

delta_list = []
for idx in range(len(angles)):
    if angles[idx] == 0:
        delta_tmp = calculate_delta(idx)
        delta_list.append(delta_tmp)
delta = np.mean(delta_list)
# delta = delta_list[3]
print(">>>> delta:", delta, delta_list)
# exit()

alpha_list = []
for idx in range(len(angles)):
    if angles[idx] == 0:
        _alpha = 0
        for i in range(1, len(pis[idx])+1, 1):
            if i == 8: continue
            _alpha += calculate_alpha(idx, i)
        _alpha /= len(pis[idx])-1
        alpha_list.append(_alpha)
# alpha  = np.mean(alpha_list)
alpha = alpha_list[3]
print(">>>> alpha:", alpha, alpha_list)


def cal_distance(index):
    _delta = delta * (math.pi / 180)
    K = (F*math.tan(_delta) - pis[index][7]) / (F + pis[index][7]*math.tan(_delta))
    dis = W / K
    return dis

def cal_theta(index, i, dis):
    _alpha = alpha * (math.pi / 180)
    _delta = delta * (math.pi / 180)
    K = (F*math.tan(_delta) - pis[index][i-1]) / (F + pis[index][i-1]*math.tan(_delta))

    numerator = N*W + ((2*i-N)*math.tan(_alpha/2) - K) * G + ((2*i-N)*math.tan(_alpha/2) - N*K) * dis
    denominator = (K + W) * (2*i-N) * math.tan(_alpha/2)

    # print('------------------------', i, N*W, ((2*i-N)*math.tan(_alpha/2) - K) * G, ((2*i-N)*math.tan(_alpha/2) - N*K) * dis)
    # print('------------------------', i, round(numerator), round(denominator))

    tan_theta = numerator / denominator
    theta = math.atan(tan_theta)
    return theta*(180 / math.pi)

def handle_theta():
    for index in range(len(names)):
        dis = cal_distance(index)
        theta = 0
        size = len(pis[index])
        for i in range(N-size, size+1, 1):
            if i == 8: continue
            theta_tmp = cal_theta(index, i, dis)
            theta += theta_tmp
            # print(index, i, "theta:", theta_tmp)
        # print('-'*30)
        print("{:<2d} 名称：{:<12s} 角度：{:3d} theta:{:3d} 实际距离：{:.1f} 预测距离:{:.1f} 距离误差：{:.1%}".format( \
            index, names[index], angles[index], round(theta/(size-1)), distances[index],round(dis), (round(dis)-distances[index]) / distances[index] ))
        # print('-'*60)

def test():
    index = 0
    dis = cal_distance(index)
    theta = 0
    for i in range(5, 12, 1):
        if i == 8: continue
        pis[index][i-5] -= 3
        for j in range(5):
            pis[index][i-5] += 1
            theta_tmp = cal_theta(index, i, dis)
            theta += theta_tmp
            print(index, i, "pi:", pis[index][i-5], "theta:", round(theta_tmp))
    print(index, angles[index], "theta:", round(theta/6), "实际距离:", distances[index], "distance:", round(dis))

handle_theta()


# image = cv2.imread("1_15.jpg")
# # access_pixels(image)
# image = 255 - image
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# ret, corners = cv2.findChessboardCorners(gray, (cnrx, cnry), flags=flags)

# print(ret, corners)
# image2 = image.copy()
# cv2.drawChessboardCorners(image, (cnrx, cnry), corners, ret)
# cv2.imshow("img", image)
# # cv2.waitKey(0)

# cv2.cornerSubPix(gray, corners, (cnrx, cnry), (-1, -1),
#                 (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01))
# print(ret, corners)
# cv2.drawChessboardCorners(image2, (cnrx, cnry), corners, ret)

# cv2.imshow("img2", image2)
# cv2.waitKey(0)