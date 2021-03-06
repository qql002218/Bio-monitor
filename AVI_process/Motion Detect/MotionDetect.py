#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
帧差法实现物体的运动检测
思想是 以第一张图像作为背景图像，后边的图像与背景做差
优点是 检测不会出现空洞
缺点是第一帧必须是背景图像，而且可能对光线的要求较高，后续的光线不能有太大的变化
"""
import cv2
import numpy as np

camera = cv2.VideoCapture(0)

es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))

kernal = np.ones((5, 5), np.uint8)
background = None

while True:
    ret, frame = camera.read()
    if background is None: #取第一帧图像做背景
        background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 灰度转化
        background = cv2.GaussianBlur(background, (21, 21), 0) #高斯模糊
        continue
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    diff = cv2.absdiff(background, gray_frame)  # 与背景图片做差
    diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.dilate(diff, es, iterations=2) #膨胀图像 把diff的孔进行修补
    image, cnts, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #找分割出来的图像块轮廓

    for c in cnts:
        if cv2.contourArea(c) < 1500: # 设定面积大小
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #做出矩形框
    cv2.imshow('contours', frame)
    cv2.imshow('dif', diff) #显示差分图像
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cv2.destroyAllWindows()
camera.release()
