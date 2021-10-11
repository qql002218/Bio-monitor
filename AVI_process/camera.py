import cv2

clicked = False


def onmouse(event, x, y, flags, params):
    global clicked  # 收取全局变量
    if event == cv2.EVENT_LBUTTONDOWN:  # 鼠标左键点击监控
        clicked = True


cam = cv2.VideoCapture(0)
cv2.namedWindow('MyWindow')
cv2.setMouseCallback('MyWindow', onmouse)
print("camera is working, click window or press any key to quit")
success, frame = cam.read()
while success and not clicked and cv2.waitKey(1) == -1:  # waitkey 1ms轮询键盘输入，无键盘按下为-1
    cv2.imshow('MyWindow', frame)
    success, frame = cam.read()
cv2.destroyAllWindows()
cam.release()
