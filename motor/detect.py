import cv2
import numpy as np


class Detect:
    def __init__(self, path):
        self.ori_img = cv2.imread(path)
        self.gray = cv2.cvtColor(self.ori_img, cv2.COLOR_BGR2GRAY)
        self.blur_img = self.gray
        self.res_img = self.gray

    def lap_detect(self):
        self.blur_img = cv2.GaussianBlur(
            self.gray, ksize=(5, 5), sigmaX=2.4, sigmaY=2.4)
        self.res_img = cv2.Laplacian(self.blur_img, ddepth=-1, ksize=5)
        self.res_img = cv2.convertScaleAbs(self.res_img)
        #self.res_img = self.thresh_proc()

    def canny_detect(self):
        self.blur_img = cv2.GaussianBlur(
            self.gray, ksize=(9, 9), sigmaX=3, sigmaY=3)
        #self.res_img = cv2.Sobel(self.gray, ddepth=-1, dx=1, dy=1, ksize=5)
        self.res_img = cv2.Canny(self.blur_img, 90, 180, apertureSize=5)
        #thresh = self.thresh_proc()
        #img_morph = cv2.morphologyEx(self.res_img, cv2.MORPH_OPEN, (3, 3))
        #cv2.erode(img_morph, (3, 3), img_morph, iterations=3)
        #cv2.dilate(img_morph, (3, 3), img_morph, iterations=3)
        #self.res_img = img_morph

    def thresh_proc(self):
        _, thresh = cv2.threshold(self.res_img, 0, 255,
                                  cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh

    def key_points_tap(self, img):
        img_cp = img.copy()
        # 按结构树模式找所有轮廓
        cnts, _ = cv2.findContours(img_cp, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
        # 按区域大小排序,找到第二大轮廓
        print(len(cnts))
        print(cnts[0])
        cnt_second = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        # 找轮廓的最小外接矩形((point), (w, h))
        box = cv2.minAreaRect(cnt_second)
        # ->(points)->(l_ints)
        return np.int0(cv2.boxPoints(box))

    def key_cnt_draw(self, points):
        mask = np.zeros(self.gray.shape, np.uint8)
        cv2.drawContours(mask, [points], -1, 255, 2)
        return mask

    def process_main(self):
        self.canny_detect()

        points = self.key_points_tap(self.res_img)

        cnt_img = self.key_cnt_draw(points)

        cv2.imshow('cnts', cnt_img)
        cv2.imshow("blur", self.blur_img)
        cv2.imshow("result", self.res_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


d = Detect("/home/xhyang/my_photo-1.jpg")
d.process_main()
