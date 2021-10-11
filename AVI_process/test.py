#!/usr/bin/python
# coding=utf-8
import os
import cv2
import scipy
global size
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
def savevideo(window_name, video_id, time,fps=30,):
    cam = cv2.VideoCapture(video_id)
    size = (int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #cv2.namedWindow(window_name)
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    videowriter = cv2.VideoWriter('MyoutputVid.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
    print("camera is working, click window or press any key to quit")
    success, frame = cam.read()
    numfps = time * fps
    while cam.isOpened() and numfps > 0:
        success, frame = cam.read()
        if not success:
            break
        frame = strokeEdges(frame)
        videowriter.write(frame)
        # cv2.imshow(window_name, frame)
        c = cv2.waitKey(10)
        numfps -=1
        print('现在是第 : {num}帧'.format(num = numfps))
        if c & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()


def store(frame,size):
    videowriter = cv2.VideoWriter('MyoutputVid.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'), 30, size)
    videowriter.write(frame)


def strokeEdges(src, blurKsize=7, edgeKsize=3):
    blurredSrc = cv2.medianBlur(src, blurKsize)  ##中值滤波去除噪声
    graysrc = cv2.cvtColor(blurredSrc, cv2.COLOR_BGR2GRAY)
    cv2.Laplacian(graysrc, cv2.CV_8U, graysrc, ksize=edgeKsize)  # 边缘检测 增加黑色线条
    normalizedAlpha = (1.0 / 255) * (255 - graysrc)  ## 归一化算子，乘图像后能将图像边缘变黑
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = channel * normalizedAlpha
    return cv2.merge(channels)


if __name__ == '__main__':
    print('open camera...')
    savevideo('mycam', 0,time =400)
