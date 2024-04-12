import face_recognition
import cv2
import os

image_data_folder = 'faces/'

# Load the images in the image_data_folder and save their face encodings in a list
image_dataset = []
for filename in os.listdir(image_data_folder):
    image_data_path = os.path.join(os.getcwd(), image_data_folder, filename)
    image_data = face_recognition.load_image_file(image_data_path)
    image_data_encoding = face_recognition.face_encodings(image_data)[0]
    image_dataset.append((filename, image_data_encoding))

# Initialize the webcam
video_capture = cv2.VideoCapture(-1)

while True:
    # Capture a single frame from the webcam
    ret, frame = video_capture.read()

    # Find the face locations and encodings in the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Compare the face encodings in the frame to the face encodings in image_dataset
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces([x[1] for x in image_dataset], face_encoding, tolerance=0.55)
        if True in matches:
            # Find the name of the matching face
            name = image_dataset[matches.index(True)][0]
            # Draw a box around the face and show the name on the top right of the box
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (right, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
video_capture.release()
cv2.destroyAllWindows()