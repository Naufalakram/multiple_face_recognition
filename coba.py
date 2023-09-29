import cv2

# Initialize the webcam
video_capture = cv2.VideoCapture(-1)

while True:
    # Capture a single frame from the webcam
    ret, frame = video_capture.read()

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
video_capture.release()
cv2.destroyAllWindows()