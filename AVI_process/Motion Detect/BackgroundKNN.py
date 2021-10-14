"""
背景分离器，前面的方法是通过帧差法+膨胀，选取运动物体的轮廓进行标定

opencv有现成的背景分割器
BackgroundSubtractor ：执行背景分割,阴影检测
"""
import numpy as np
import cv2

bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    fgmask = bs.apply(frame) ## 应用分割器过滤出来前景
    th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1] #增加一层threshold，二极管非黑即白，阈值化后的图像更加纯净
    dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2) #再次膨胀
    image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #找区域
    for c in contours: #区域画框
        if cv2.contourArea(c) > 1600:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
    cv2.imshow('mog', fgmask)
    cv2.imshow('thresh', th)
    cv2.imshow('detection', frame)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
