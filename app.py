import face_recognition
import cv2
import os

image_load = 'image1.jpg'
# image_data = 'faces/rika.png'
image_data = 'faces/rika.png'

# Load the images
image_load_path = os.path.join(os.getcwd(), image_load)
image_data_path = os.path.join(os.getcwd(), image_data)
image_load = face_recognition.load_image_file(image_load_path)
image_data = face_recognition.load_image_file(image_data_path)

# Find the face locations and encodings in each image
image_load_face_locations = face_recognition.face_locations(image_load)
image_load_face_encodings = face_recognition.face_encodings(image_load, image_load_face_locations)
image_data_face_locations = face_recognition.face_locations(image_data)
image_data_face_encodings = face_recognition.face_encodings(image_data, image_data_face_locations)

# Compare the face encodings
matches = face_recognition.compare_faces(image_data_face_encodings, image_load_face_encodings[0])

# Draw boxes around the faces in the image_load image
for (top, right, bottom, left), match in zip(image_load_face_locations, matches):
    if match:
        cv2.rectangle(image_load, (left, top), (right, bottom), (0, 0, 255), 2)

# Display the image with the boxes around the matching faces
cv2.imshow('Image', image_load)
cv2.waitKey(0)
cv2.destroyAllWindows()