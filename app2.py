import face_recognition
import cv2
import os

image_load = 'image1.jpg'
image_data_folder = 'faces/'

# Load the images in the image_data_folder and save their face encodings in a list
image_dataset = []
for filename in os.listdir(image_data_folder):
    image_data_path = os.path.join(os.getcwd(), image_data_folder, filename)
    image_data = face_recognition.load_image_file(image_data_path)
    image_data_encoding = face_recognition.face_encodings(image_data)[0]
    image_dataset.append((filename, image_data_encoding))

# Load the image_load and find the face locations and encodings
image_load_path = os.path.join(os.getcwd(), image_load)
image_load = face_recognition.load_image_file(image_load_path)
image_load_face_locations = face_recognition.face_locations(image_load)
image_load_face_encodings = face_recognition.face_encodings(image_load, image_load_face_locations)

# Compare the face encodings in image_load to the face encodings in image_dataset
for (top, right, bottom, left), face_encoding in zip(image_load_face_locations, image_load_face_encodings):
    matches = face_recognition.compare_faces([x[1] for x in image_dataset], face_encoding, tolerance=0.55)
    if True in matches:
        # Find the name of the matching face
        name = image_dataset[matches.index(True)][0]
        # Draw a box around the face and show the name on the top right of the box
        cv2.rectangle(image_load, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(image_load, name, (right, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Display the image with the boxes and names around the matching faces
cv2.imshow('Image', image_load)
cv2.waitKey(0)
cv2.destroyAllWindows()