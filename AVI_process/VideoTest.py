import cv2
cam =cv2.VideoCapture(0)
fps = 30
size = (int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
videowriter = cv2.VideoWriter('MyoutputVid.avi',cv2.VideoWriter_fourcc('I','4','2','0'),fps,size)
success, frame = cam.read()
numframeremaining = 10*fps
while success and numframeremaining>0:
    videowriter.write(frame)
    success, frame = cam.read()
    numframeremaining -= 1
cam.release()
