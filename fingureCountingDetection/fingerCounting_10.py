import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize the camera
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Initialize hand detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    # Read frame from the camera
    success, frame = video.read()
    if not success:
        continue

    # Flip the frame horizontally for a more natural view
    frame = cv2.flip(frame, 1)

    # Find hands in the frame
    hands, _ = detector.findHands(frame, draw=False)  # Not drawing to avoid confusion with text

    # Initialize total fingers count
    total_fingers = 0

    if hands:
        for hand in hands:
            # Detect fingers up for each hand
            fingers_up = detector.fingersUp(hand)
            # Add the count of fingers up in this hand to the total count
            total_fingers += sum(fingers_up)
            print(fingers_up)
        # Display the total count of fingers up on the frame
        cv2.putText(frame, f"Total Fingers: {total_fingers}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Display the frame
    cv2.imshow("Frame", frame)

    # Check for 'q' key to quit the program
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the camera and close all windows
video.release()
cv2.destroyAllWindows()
