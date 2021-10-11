import cv2
import numpy
import scipy.integrate


def strokeEdges(src, blurKsize=7, edgeKsize=3):
    blurredSrc = cv2.medianBlur(src, blurKsize) ##中值滤波去除噪声
    graysrc = cv2.cvtColor(blurredSrc, cv2.COLOR_BGR2GRAY)

    cv2.Laplacian(graysrc, cv2.CV_8U, graysrc, ksize=edgeKsize)  #边缘检测 增加黑色线条

    normalizedAlpha = (1.0 / 255) * (255 - graysrc) ## 归一化算子，乘图像后能将图像边缘变黑
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = channel * normalizedAlpha
    cv2.imshow('result', cv2.merge(channels))
    cv2.imshow('pre',src)
    cv2.waitKey()
    cv2.destroyAllWindows()


strokeEdges(cv2.imread('dijia.png'))
