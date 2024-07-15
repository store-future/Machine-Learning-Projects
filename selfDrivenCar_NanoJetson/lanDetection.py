import cv2
import numpy  as np

cap = cv2.VideoCapture('road.mp4')

# Get the total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"Total number of frames in the video: {total_frames}")


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # checks mouse left button down condition
        colors = hsv[y, x]
        print("HSV Values at (", x, ",", y, ") -", colors)

while True:
    ret,frame = cap.read()
    frame = cv2.resize(frame, (700, 400), interpolation=cv2.INTER_LINEAR)
    
    # road
    hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
    low_white = np.array([0, 0, 180])
    up_white = np.array([180, 80, 255])
    mask = cv2.inRange(hsv , low_white , up_white)

    # road-2
    # low_white = np.array([75, 40, 115])
    # up_white  = np.array([85, 70, 140])
    # mask = cv2.inRange(hsv , low_white , up_white)

    # use canny edge detection algorithm 
    edges = cv2.Canny(mask , 75,250)
    # print(edges)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)

    print(lines)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            # cv2.line(hsv, (x1, y1), (x2, y2),   (255, 255, 0), 5)
            cv2.line(mask, (x1, y1), (x2, y2),  (255, 255, 255), 3)
            cv2.line(edges, (x1, y1), (x2, y2),  (255, 255, 255), 3)

    cv2.imshow('normal',frame)
    cv2.imshow('hsv',hsv)
    cv2.imshow('mask',mask)
    cv2.imshow('edges',edges)

    cv2.setMouseCallback('hsv', mouse_callback)


    if cv2.waitKey(100) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()