import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH , 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT , 400)


# cap.set(CAP_PROP)
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame , 1)
    
    hsvframe = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
    height , width ,_ = frame.shape

    cx = int(width/2)
    cy = int(height/2)

    print(cx ,cy)


    pixel_center = hsvframe[cy,cx]
    hue_value = pixel_center[0]

    color ='undefined'
    if hue_value < 5:
        color = "Red"
    # elif hue_value <22:
    #     color = "Orange"
    # elif hue_value <33 :
    #     color = "Yellow"
    elif hue_value >45 and hue_value <78  :
        color = "Green"
    # elif hue_value <131:
    #     color = "Blue"
    # elif hue_value <167:
    #     color = "Violet"
    else :
        color = 'No'

    print(hue_value)
    print(color)    
    cv2.putText(frame , color , (10,50) ,0 , 1 , (255,0,0) , 2)
    cv2.circle(frame , (cx ,cy) , 5 , (255,0,0) ,2)
    
    cv2.imshow('frame', frame)

    cv2.waitKey(200)
        

cap.release()

cv2.destroyAllWindows()