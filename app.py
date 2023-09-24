import face_recognition
import cv2
import os

image_to_scan = 'image1.jpg'
image_dataset_folder = 'faces'

# Load the image to scan
image = face_recognition.load_image_file(image_to_scan)

# Detect the faces in the image
face_locations = face_recognition.face_locations(image)

# Draw a rectangle around each detected face using OpenCV
for (top, right, bottom, left) in face_locations:
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

# Display the image with the detected faces in a window
cv2.imshow('Faces', image)
cv2.waitKey(0)

# Load the images from the 'faces' folder and store them in a list
images = []
for filename in os.listdir(image_dataset_folder):
    # if the file name ends with '.jpg' or '.png'
    if filename.endswith('.jpg') or filename.endswith('.png'):
        images.append(face_recognition.load_image_file(os.path.join(image_dataset_folder, filename)))

# Loop through the list of images and detect the faces in each image using face_recognition
for image in images:
    # Detect the faces in the image
    face_locations = face_recognition.face_locations(image)

    # Draw a rectangle around each detected face using OpenCV
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

    # Display the images with the detected faces in a window
    cv2.imshow('Faces', image)
    cv2.waitKey(0)

# Wait for the user to press a key to exit the program
cv2.destroyAllWindows()