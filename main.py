import face_recognition
import os
import cv2
import numpy as np
import math
import sys
import time
import json
from datetime import datetime

absensi_file = "absensi.json"

today_date = time.strftime("%d/%m/%Y")

# open the dataset file
with open(absensi_file, 'r') as f:
    data = json.load(f)

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance < face_match_threshold:
        return str(round(linear_val * 100, 2)) + "%"
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + "%"

class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir("faces"):
            face_image = face_recognition.load_image_file(f'faces/{image}')
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image.split(".")[0])
        print(self.known_face_names)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

         # Set the window to normal so it can be resized
        cv2.namedWindow('Face Attendance', cv2.WINDOW_NORMAL)

        # Set the window to full screen
        cv2.setWindowProperty('Face Attendance', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        if not video_capture.isOpened():
            sys.exit('Video capture is not opened')

        no_face_timer = 0
        no_face_threshold = 5  # Adjust this to your desired timeout in seconds

        while True:
            ret, frame = video_capture.read()

            if self.process_current_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]

                self.face_locations = face_recognition.face_locations(rgb_small_frame)

                if not self.face_locations:
                    no_face_timer += 1
                else:
                    no_face_timer = 0

                if no_face_timer >= no_face_threshold * 30:  # 30 frames per second
                    # Close the OpenCV window after the timeout
                    break

                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = 'Unknown'

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        confidence = face_confidence(face_distances[best_match_index])

                        if float(confidence.split("%")[0]) > 55:
                            name = self.known_face_names[best_match_index]
                            confidence = face_confidence(face_distances[best_match_index])


                            time_now = time.strftime("%H:%M:%S")
                            current_time = datetime.strptime(time.strftime("%H:%M:%S"), "%H:%M:%S")

                            print('this is the time now: ', time_now)
                            print('this is the current time: ', current_time)

                            compare_time = datetime.strptime("12:00:00", "%H:%M:%S")

                            print('this is the compare time: ', compare_time)

                            # check the last data to see if today's date is already there
                            if len(data) > 0:
                                last_data = data[-1]
                            else:
                                last_data = None    

                            if last_data:
                                if last_data["date"] == today_date:
                                    # loop through the "absensi" key to see if the name is already there
                                    data_absensi = last_data["absensi"]
                                    name_found = False

                                    for absensi in data_absensi:
                                        if absensi["name"] == name:
                                            name_found = True
                                            break
                                    
                                    if not name_found:
                                        # add new data
                                        # if time_now > "12:00:00": then add the "jam_keluar" key
                                        
                                        if current_time > compare_time:
                                            data_absensi.append({
                                                "name": name,
                                                "jam_masuk": time_now,
                                                "jam_keluar": time_now,
                                            }) 
                                        else:
                                            data_absensi.append({
                                                "name": name,
                                                "jam_masuk": time_now,
                                            })
                                        
                                    
                                    # else update the data and change the "jam_keluar" key
                                    else:
                                        for absensi in data_absensi:
                                            if absensi["name"] == name:
                                                 
                                                if current_time > compare_time:
                                                    absensi["jam_keluar"] = time_now
                                                # else do nothing
                                                else:
                                                    pass

                                        
                                                break

                                else:
                                    # create new data
                                    if current_time > compare_time:
                                        data.append({
                                            "date": today_date,
                                            "absensi": [
                                                {
                                                    "name": name,
                                                    "jam_masuk": time_now,
                                                    "jam_keluar": time_now,
                                                }
                                            ]
                                        })
                                    else:
                                        data.append({
                                            "date": today_date,
                                            "absensi": [
                                                {
                                                    "name": name,
                                                    "jam_masuk": time_now,
                                                }
                                            ]
                                        })
                            else:
                                # create new data
                                if current_time > compare_time:
                                    data.append({
                                        "date": today_date,
                                        "absensi": [
                                            {
                                                "name": name,
                                                "jam_masuk": time_now,
                                                "jam_keluar": time_now,
                                            }
                                        ]
                                    })
                                else:
                                    data.append({
                                        "date": today_date,
                                        "absensi": [
                                            {
                                                "name": name,
                                                "jam_masuk": time_now,
                                            }
                                        ]
                                    })

                                
                            # write the data to the file
                            with open(absensi_file, 'w') as f:
                                json.dump(data, f, indent=4)

                        else:
                            name = "Unknown"
                            confidence = 'Unknown'

                    self.face_names.append(f'{name} {confidence}')

            self.process_current_frame = not self.process_current_frame

            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

            cv2.imshow('Face Attendance', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()
