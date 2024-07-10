import cv2   
import numpy as np
import RPi.GPIO as GPIO                    #Import GPIO library
import time

from picamera2 import Picamera2
#print(cv2.__version__)

picam = Picamera2()
picam.preview_configuration.main.size = (600,400)
picam.preview_configuration.main.format = "RGB888"
#picam.preview_configuration.align()
#picam.configure("preview")
picam.start()# programming the GPIO by BCM pin numbers


#Import time library
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

m11=16
m12=12
m21=21
m22=20
EN1 =17
EN2 = 18

GPIO.setup(m11,GPIO.OUT)
GPIO.setup(m12,GPIO.OUT)
GPIO.setup(m21,GPIO.OUT)
GPIO.setup(m22,GPIO.OUT)

GPIO.setup(EN1,GPIO.OUT)
GPIO.setup(EN2,GPIO.OUT)

pwm_a = GPIO.PWM(EN1,100)
pwm_b = GPIO.PWM(EN2,100)

pwm_a.start(0)
pwm_b.start(0)

def set_speed(speed):
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def stop():
    set_speed(0)
    print ('stop')
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)

def forward(speed):
    set_speed(speed)
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print('Forward')


while True:
	img = picam.capture_array()
	img = cv2.flip(img, 1)
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	#definig the range of red color
	red_lower=np.array([136,87,111],np.uint8)
	red_upper=np.array([180,255,255],np.uint8)
	
	#defining the Range of green color
	green_lower=np.array([66, 122, 129],np.uint8)
	green_upper=np.array([86,255,255],np.uint8)
	
	#finding the range of red,green color in the image
	red=cv2.inRange(hsv, red_lower, red_upper)
	green=cv2.inRange(hsv,green_lower,green_upper)
	
	#Morphological transformation, Dilation  	
	kernal = np.ones((5 ,5), "uint8")
	
	red=cv2.dilate(red, kernal)
	res=cv2.bitwise_and(img, img, mask = red)
	
	green=cv2.dilate(green,kernal)
	res2=cv2.bitwise_and(img, img, mask = green)
	
	#Tracking the Red Color
	(contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area>300):
			

			x,y,w,h = cv2.boundingRect(contour)	
			img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
			cv2.putText(img,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))	
			print('Red')
			#time.sleep(1)
			#print('stop')	
			stop()

	#Tracking the green Color
	(contours,hierarchy)=cv2.findContours(green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area>300):
			x,y,w,h = cv2.boundingRect(contour)	
			img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
			cv2.putText(img,"Green  color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0))  
			print('green')
			#time.sleep(1)
			#print('fwd')
			forward(30)
	
	cv2.imshow('detection', img)

	if cv2.waitKey(100) & 0xFF == ord('q'):
		break 
    
cv2.destroyAllWindows()
