import numpy as np
import cv2

"""
均值漂移检测
区域检测，该算法寻找概率函数离散样本的最大密度
这个可以作为图像的预处理
这种做法是否适用于多目标？ 按道理应该不行，因为聚类只有一个感兴趣的区域

"""
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
r, h, c, w = 10, 200, 10, 200
track_window = (c, r, w, h)

roi = frame[r:r + h, c:c + w]

hsv_hist = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_hist, np.array((100., 30., 32.)), np.array((180., 120., 255.)))

roi_hist = cv2.calcHist([hsv_hist],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,1)

while True:
    ret,frame = cap.read()

    if ret is True:
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        ret, track_window = cv2.meanShift(dst,track_window,term_crit)

        x,y,w,h = track_window
        img2 = cv2.rectangle(frame,(x,y),(x+w,y+h),255,2)
        cv2.imshow('img2',img2)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break
    else:
        break
cv2.destroyAllWindows()
cap.release()