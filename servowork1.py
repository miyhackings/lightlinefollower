import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32,GPIO.OUT)
GPIO.setup(33,GPIO.OUT)
q = GPIO.PWM(32,50)
p = GPIO.PWM(33,50)
tilt=90
pan=90
prevtilt=90
prevpan=90
def angle(s):
    if (s > 180):
        print('ulimit')
        return 12.5
    elif (s < 0):
        print('llimit')
        return 2.5
    else:
        return ((s/18)+2.5)
p.start(angle(pan))
q.start(angle(tilt))
time.sleep(1)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        orig = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        cv2.circle(image, maxLoc, 4, (255, 0, 0), 2)
        x=maxLoc[0]
        y=maxLoc[1]
        xmovement=320-x
        ymovement=240-y
        print(xmovement)
        if (ymovement >= 20) & (ymovement < 80):
            tilt=tilt+.5
            print('up')
        elif (ymovement >= 80) & (ymovement < 180):
            tilt=tilt+1.5
            print('uupp')
        elif (ymovement >= 200):
            tilt=tilt+10
            print('uuuppp')
        elif (ymovement <= -20) & (ymovement >= -80):
            tilt=tilt-.5
            print('do')
        elif (ymovement < -80) & (ymovement > -180):
            tilt=tilt-1.5
            print('ddoo')
        elif (ymovement <= -200):
            tilt=tilt-10
            print('dddooo')
        if tilt != prevtilt:
            q.ChangeDutyCycle(angle(tilt))
            prevtilt=tilt
        else :
            q.ChangeDutyCycle(0)
        if (xmovement >= 20) & (xmovement < 80):
            pan=pan-.5
            print('l')
        elif (xmovement >= 80) & (xmovement < 180):
            pan=pan-1.5
            print('ll')
        elif (xmovement >= 200):
            pan=pan-10
            print('lll')
        elif (xmovement <= -20) & (xmovement >= -80):
            pan=pan+.5
            print('r')
        elif (xmovement < -80) & (xmovement > -180):
            pan=pan+1.5
            print('rr')
        elif (xmovement <= -200):
            pan=pan+10
            print('rrr')
        if pan != prevpan:
            p.ChangeDutyCycle(angle(pan))
            prevpan=pan
        else :
            p.ChangeDutyCycle(0)
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            cv2.destroyAllWindows()
            break
        
