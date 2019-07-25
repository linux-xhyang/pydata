import time

import cv2
import numpy as np


class Detect:
    def __init__(self):
        self.vcp = None
        self.ori = None
        self.gray = None
        self.result = None

    def __init__(self, path):
        self.ori = cv2.imread(path)
        self.gray = cv2.cvtColor(self.ori, cv2.COLOR_BGR2GRAY)
        self.result = self.gray

    def open_camera(self, path):
        self.vcp = cv2.VideoCapture(path)
        if self.vcp.isOpened():
            self.vcp.set(cv2.CAP_PROP_POS_FRAMES, 1)
            self.vcp.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.vcp.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.vcp.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        print("open_camera")
        return self.query_camera()

    def query_camera(self):
        print("query_camera")
        if self.vcp.isOpened():  # try to get the first frame
            rval, self.ori = self.vcp.read()
            if rval is True:
                print("read frame success")
            else:
                print("read frame failed")
            self.gray = cv2.cvtColor(self.ori, cv2.COLOR_BGR2GRAY)
            self.result = self.gray
        else:
            rval = False

        return rval

    def lap_detect(self):
        self.result = cv2.GaussianBlur(self.gray, ksize=(5, 5), sigmaX=2.4)
        lap = cv2.Laplacian(self.result, ddepth=-1, ksize=5)
        lap = cv2.convertScaleAbs(lap)
        _, lap = cv2.threshold(lap, 0, 255,
                               cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        self.result = lap

    def canny_detect(self):
        self.result = cv2.GaussianBlur(self.gray, ksize=(9, 9), sigmaX=2.4)
        canny = cv2.Canny(self.result, 90, 180, apertureSize=5)

        img_morph = cv2.morphologyEx(self.canny, cv2.MORPH_CLOSE, (3, 3))
        cv2.dilate(img_morph, (3, 3), img_morph, iterations=3)
        cv2.erode(img_morph, (3, 3), img_morph, iterations=2)

        self.result = img_morph

    def thresh_detect(self):
        self.result = cv2.GaussianBlur(self.gray, ksize=(7, 7), sigmaX=2.4)
        canny = cv2.Canny(self.result, 100, 200, apertureSize=5)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        cv2.dilate(canny, kernel, canny, iterations=1)
        self.result = canny

        # thresh = cv2.adaptiveThreshold(self.gray, 255,
        #                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                                cv2.THRESH_BINARY, 31, 2)
        # cv2.bitwise_not(thresh, thresh)
        # cv2.dilate(thresh, (7, 5), thresh, iterations=7)
        # self.result = thresh

    def key_points_find(self, img):
        img_cp = img.copy()
        width, height = img.shape[1], img.shape[0]

        # 按外部模式找所有轮廓
        boxs = []

        cnts, hie = cv2.findContours(img_cp, cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)

        # for cnt in cnts:
        #     x, y, w, h = cv2.boundingRect(cnt)
        #     if abs(1 - w / h) < 0.3 and w > 40:
        #         if x > 10:
        #             x -= 10
        #         if y > 10:
        #             y -= 10

        #         if x + w + 20 <= width:
        #             w += 20
        #         else:
        #             w = (width - x)

        #         if y + h + 20 <= height:
        #             h += 20
        #         else:
        #             h = (height - y)

        #         boxs.append([x, y, w, h])

        if len(boxs) == 0:
            # 按结构树模式找所有轮廓
            print("External found zero,try with Tree")
            parent = -1
            self.counts = []
            ic = 0
            cnts, hie = cv2.findContours(img_cp, cv2.RETR_TREE,
                                         cv2.CHAIN_APPROX_NONE)

            print(len(cnts))
            # for i in range(64, 67):
            #     x, y, w, h = cv2.boundingRect(cnts[i])
            #     cv2.rectangle(img_cp, (x, y), (x + w, y + h), (255, 255, 255),
            #                   1)
            # cv2.imshow("sort", img_cp)
            for i in range(0, len(cnts)):
                if hie[0][i][2] != -1 and ic == 0:
                    parent = i
                    ic = ic + 1
                elif hie[0][i][2] != -1:
                    ic = ic + 1
                elif hie[0][i][2] == -1:
                    if ic >= 12:
                        print("found 1")
                        self.counts.append([parent, ic])
                    ic = 0
                    parent = -1

            print(self.counts)
            for i in range(self.counts[0][0],
                           self.counts[0][0] + self.counts[0][1]):
                x, y, w, h = cv2.boundingRect(cnts[i])
                cv2.rectangle(img_cp, (x, y), (x + w, y + h), (255, 255, 255),
                              1)
            cv2.imshow("sort", img_cp)

            for rect in self.counts:
                if rect[0] > 12:
                    boxs.append(cv2.boundingRect(cnts[rect[0] + rect[1] % 12]))
                else:
                    boxs.append(cv2.boundingRect(cnts[rect[0]]))

        return boxs

    def key_cnts_draw(self, points):
        mask = np.zeros(self.gray.shape, np.uint8)

        for point in points:
            x, y, w, h = point[0], point[1], point[2], point[3]
            cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), 2)

        return mask

    def sharpness_compute(self, img, points):
        img_cp = img.copy()

        sharpness = 0
        for [x, y, w, h] in points:
            roi = img[y:y + h, x:x + w]
            blur = cv2.GaussianBlur(roi, (5, 5), sigmaX=2.4)
            lap = cv2.Laplacian(blur, ddepth=-1, ksize=5)
            lap = cv2.convertScaleAbs(lap)
            lap = abs(lap)
            sharpness += cv2.mean(lap)[0]
            cv2.imshow('lap', lap)
        print("sharpness =" + str(sharpness))

    def process_main(self):
        self.thresh_detect()

        points = self.key_points_find(self.result)
        print(points)
        cnt_img = self.key_cnts_draw(points)

        self.sharpness_compute(self.gray, points)
        cv2.imshow('cnts', cnt_img)
        cv2.imshow("result", self.result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def vcp_main(self):
        success = self.open_camera(1)

        for i in range(0, 6):
            capture = self.query_camera()
            cv2.imshow("gray", self.gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            time.sleep(1)

        self.thresh_detect()
        points = self.key_points_find(self.result)
        print(points)
        cnt_img = self.key_cnts_draw(points)
        cv2.imshow('cnts', cnt_img)

        while success:
            capture = self.query_camera()
            if capture is True:
                self.sharpness_compute(self.gray, points)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

            time.sleep(1)
        self.vcp.release()


d = Detect("/home/xhyang/my_photo-23.jpg")
#d = Detect("/home/xhyang/src/pydata/motor/autofocus.png")
d.process_main()
#d.vcp_main()
