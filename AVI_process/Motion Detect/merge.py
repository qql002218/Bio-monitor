import cv2
import numpy as np
import sys

import argparse


"""
这个文件是对之前学习的merge，包括背景分割，感兴趣区域roi的识别，camshift+kalman滤波，用面向对象的方法
为每一个待检测的运动物体增加一个识别框
"""
# parser = argparse.ArgumentParser()
# parser.add_argument("-a", "--algorithm",
#     help = "m (or nothing) for meanShift and c for camshift")
# args = vars(parser.parse_args())


def center(points):
    x = (points[0][0] + points[1][0] + points[2][0] + points[3][0]) / 4
    y = (points[0][1] + points[1][1] + points[2][1] + points[3][1]) / 4
    return np.array([np.float32(x), np.float32(y)], np.float32)


font=cv2.FONT_HERSHEY_SIMPLEX
class pridict():
    def __init__(self, id, frame, track_window):
        # 设置roi区域
        self.id = id
        x, y, w, h = track_window
        self.track_window = track_window
        self.roi = cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2HSV)
        roi_hist = cv2.calcHist([self.roi], [0], None, [16], [0, 180])
        self.rio_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

        # 设置kalman
        self.kalman = cv2.KalmanFilter(4, 2)  # 4：状态数，包括（x，y，dx，dy）坐标及速度（每次移动的距离）；2：观测量，能看到的是坐标值
        self.kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)  # 系统测量矩阵
        self.kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]],
                                                np.float32)  # 状态转移矩阵
        self.kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                                               np.float32) * 0.003  # 系统过程噪声协方差

        self.measurement = np.array((2, 1), np.float32)
        self.prediction = np.array((2, 1), np.float32)
        self.term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        self.center = None
        self.update(frame)

    def __del__(self):
        print("mouse {} is destoryed".format(self.id))

    def update(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        back_project = cv2.calcBackProject([hsv], [0], self.rio_hist, [0, 180], 1)
        # if args.get("algorithm") == "c":
        #     ret, self.track_window = cv2.CamShift(back_project, self.track_window, self.term_crit)
        #     pts = cv2.boxPoints(ret)
        #     pts = np.int0(pts)
        #     self.center = center(pts)
        #     cv2.polylines(frame, [pts], True, 255, 1)
        # if not args.get("algorithm") or args.get("algorithm") == "m":
        ret, self.track_window = cv2.meanShift(back_project, self.track_window, self.term_crit)
        x, y, w, h = self.track_window
        self.center = center([[x, y], [x + w, y], [x, y + h], [x + w, y + h]])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 1)
        self.kalman.correct(self.center)
        pridiction = self.kalman.predict()
        cv2.circle(frame, (int(pridiction[0]), int(pridiction[1])), 4, (0, 255, 0), -1)
        cv2.putText(frame, "ID: {id} -> {center}".format(id=self.id, center=self.center), (11, (self.id + 1) * 25 + 1),font,
                    0.6, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, "ID: {id} -> {center}".format(id=self.id, center=self.center), (11, (self.id + 1) * 25),font,
                    0.6, (0, 255, 0), 1, cv2.LINE_AA)


def main():
    cap = cv2.VideoCapture(0)
    history = 20
    bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)
    bs.setHistory(history)
    # cv2.namedWindow('dectect')
    predicts = {}
    firstFrame = True
    frames = 0
    while cap.isOpened():
        ret, frame = cap.read()
        fgmask = bs.apply(frame)
        if frames < history:
            frames = frames + 1
            continue
        th = cv2.threshold(fgmask.copy(), 127, 255, cv2.THRESH_BINARY)[1]
        th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
        dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 3)), iterations=2)

        image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contour = 0
        for c in contours:
            if cv2.contourArea(c) > 2000:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                if firstFrame is True:
                    predicts[contour] = pridict(contour, frame, (x, y, w, h))
                    contour += 1
        for i,p in predicts.items():
            p.update(frame)
        cv2.imshow("detect",frame)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break


if __name__ == '__main__':
    main()
