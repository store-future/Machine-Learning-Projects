import cv2

def capture_and_process_video():
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Set frame width and height
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

    if not cap.isOpened():
        print("Error: Camera could not be opened.")
        return

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: No frame captured.")
                break

            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)

            # Convert the frame to HSV color space
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Get dimensions of the frame
            height, width, _ = frame.shape

            # Calculate the center of the frame
            cx, cy = int(width / 2), int(height / 2)

            # Extract color information from the center pixel
            pixel_center = hsv_frame[cy, cx]
            hue_value = pixel_center[0]

            # Determine th e color based on hue value
            color = 'No'
            if hue_value < 5:
                color = "Red"
            elif 45 < hue_value < 78:
                color = "Green"

            # Display the detected color
            cv2.putText(frame, color, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Draw a rectangle around the center
            x_rect, y_rect = cx - 50, cy - 50  # Rectangle top-left corner
            width_rect, height_rect = 50, 50  # Rectangle dimensions
            cv2.rectangle(frame, (x_rect, y_rect), (x_rect + width_rect, y_rect + height_rect), (0, 255, 0), 2)

            # Show the frame
            cv2.imshow('frame', frame)

            # Basic information 
            print("Hsv frame shape :", hsv_frame.shape)
            print("pixel center :", pixel_center)
            print("Center coordinates:", cx, cy)
            print("Hue value:", hue_value)
            print("Detected color:", color)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(200) & 0xFF == ord('q'):
                break
    finally:
        # Release the camera and close all windows
        cap.release()
        cv2.destroyAllWindows()

# Call the function to start the process
capture_and_process_video()
