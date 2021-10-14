"""
背景分离器，前面的方法是通过帧差法+膨胀，选取运动物体的轮廓进行标定

opencv有现成的背景分割器
BackgroundSubtractor ：执行背景分割
"""
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

mog = cv2.createBackgroundSubtractorMOG2()
while 1:
    ret, frame = cap.read()

    fgmask = mog.apply(frame)

    cv2.imshow('frame', fgmask)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
