# daftar karyawan baru menggunakan haarcascade
import cv2
import json

dataset = "dataset.json" # dataset karyawan



# open the dataset file
with open(dataset, 'r') as f:
    data = json.load(f)

# check the last data
last_data = data[-1]

# check the name    
name = last_data["name"]

# Open a video capture from the default camera (0)
video_capture = cv2.VideoCapture(0)

# Set the window to normal so it can be resized
cv2.namedWindow('Image Capture', cv2.WINDOW_NORMAL)

# Set the window to full screen
cv2.setWindowProperty('Image Capture', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    # Capture a frame from the video stream
    ret, frame = video_capture.read()

    # Convert the frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Initialize the key variable to None
    key = cv2.waitKey(1)

    # Press 'q' to save the entire image, but only if faces were detected
    if len(faces) > 0 and key == ord('q'):
        # Save the frame before drawing the rectangle
        cv2.imwrite('faces/' + name + '.jpg', frame)
        break

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('Image Capture', frame)

# Release the video capture and close the OpenCV window
video_capture.release()
cv2.destroyAllWindows()