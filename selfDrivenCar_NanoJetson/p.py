import cv2
import numpy  as np

cap = cv2.VideoCapture('road.mp4')

# Get the total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"Total number of frames in the video: {total_frames}")


def canny (image):
    gray = cv2.cvtColor(image , cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray , (5,5) , 0)
    canny = cv2.Canny(blur , 100,200)
    return canny


def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(9,314) , (375,175)  , (695,309)]]) 
    mask = np.zeros_like(image)                 #creating original frame sized zero indexing frame
    cv2.fillPoly(mask , polygons , 255)
    masked_image = cv2.bitwise_and(cany , mask)
    return masked_image


while True:
    ret,frame = cap.read()
    frame = cv2.resize(frame, (700, 400), interpolation=cv2.INTER_LINEAR)
    
    
    # use canny edge detection algorithm 
    cany = canny(frame)
    region = region_of_interest(cany)

    cv2.imshow('cany',cany)
    cv2.imshow('region',region)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()