import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np


cap = cv2.VideoCapture(0)       # enable our camera module
cap.set(3 , 1280)               # setting window width 
cap.set(4 , 720)                # setting window height 

# cap.set(cv2.CAP_PROP_FRAME_WIDTH,1080)    # setting window width 
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)    # setting window height 

print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))        # printing the width of window
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))       # printing the height of window

# converting all the images into numpy array
background = cv2.imread("Resources/Background.png")
ball = cv2.imread("Resources/ball.png" ,  cv2.IMREAD_UNCHANGED)   # IMREAD_UNCHANGED flag try to read image with 4 channel (Red ,Green ,Blue Alpha)  
bat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
bat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)
gameover = cv2.imread("Resources/gameover.png", cv2.IMREAD_UNCHANGED)
# print(background)

# Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

# declaring dynamic ball cordinates
ballpos = [100,100]
speedx = 15
speedy = 15


#counting scres
scores =[0,0]

# Game Over
game_over = False


while True:
    success ,image = cap.read()
    
    image = cv2.flip(image , 1)     # flipping the image on horizontle axis

    # Find hands in the current frame
    # The 'draw' parameter draws landmarks and hand outlines on the image if set to True
    # The 'flipType' False parameter flips the image, making it easier for some detections
    hands, img = detector.findHands(image, draw=True, flipType=False)
    # print(hands)

    #overlaping images on our window
    image = cv2.addWeighted(image , 0.2 , background , 0.8 , 0)     #setting up background image upon camera taking image    -> syntax(src1 , tranparency1 , src2 ,tranparency2 , 0 )

    if hands:
        for hand in hands:
            # finding cordinates of hands and bats
            x,y,w,h = hand['bbox']          # hand bounding box cordinates
            h1 , w1, _ = bat1.shape         # height and width of bat image
            y1 = y-h1//2                    # for grabing bat from center with finger
            y1 = np.clip(y1 , 20 , 415)     # limiting y value of bat in array to stop going outside the window


            # overlaping bat images to our background
            if hand['type'] == 'Left':
                image = cvzone.overlayPNG(image , bat1 , (59,y1))        # moving bat with our hand by giving y cordinates dynamic
                if 59 < ballpos[0] < 59+w1 and y1 < ballpos[1] <y1 +h1:  # checking upon both axis-x,y ,  if ball position is colliding with bat 
                    speedx = -speedx
                    ballpos[0] +=30                                      # making ball a lit bit faster upon colliding with bat 
                    scores[0] +=1


            if hand['type'] == 'Right':
                image = cvzone.overlayPNG(image , bat2 , (1195,y1))
                if 1195-50 < ballpos[0] < 1199 and y1  < ballpos[1] <y1+h1:
                    speedx = -speedx
                    ballpos[0] -=30                                      # making ball a lit bit faster upon colliding with bat (negative because have to speedup in reverse direction)
                    scores[1] +=1

    if 40 > ballpos[0] or ballpos[0] >1200:                              # checking the cordinates beyond bats
        game_over = True

    if game_over == True:
        image = gameover
        if scores[0] > scores[1]:
            cv2.putText(image , str(scores[0]).zfill(2) , (585,360) , cv2.FONT_HERSHEY_COMPLEX ,2.5 , (200,0,200) ,5 )
        if scores[1] > scores[0]:
            cv2.putText(image , str(scores[1]).zfill(2) , (585,360) , cv2.FONT_HERSHEY_COMPLEX ,2.5 , (200,0,200) ,5 )
        if scores[0] == scores[1]:
            cv2.putText(image , str('Draw') , (565,360) , cv2.FONT_HERSHEY_COMPLEX ,1.8 , (200,0,200) ,5 )
    else:                                                                   # if game not over continue to move the ball
        if ballpos[1] >= 500 or ballpos[1] <= 10:
            speedy = -speedy

        ballpos[0] +=speedx
        ballpos[1] +=speedy

        # Draw the Ball
        image = cvzone.overlayPNG(image , ball , ballpos)

        cv2.putText(image , str(scores[0]) , (300,650) , cv2.FONT_HERSHEY_COMPLEX ,3 ,(255,255,255) , 5)
        cv2.putText(image , str(scores[1]) , (900,650) , cv2.FONT_HERSHEY_COMPLEX ,3 ,(255,255,255) , 5)

    cv2.imshow("Ping Pong" ,image)
    key = cv2.waitKey(1)
    if key == ord('r'):
        ballpos = [100,100]
        speedx = 15
        speedy = 15
        gameover = cv2.imread("Resources/gameover.png", cv2.IMREAD_UNCHANGED)
        game_over = False
        scores =[0,0]
    elif key == ord('s'):
        break
