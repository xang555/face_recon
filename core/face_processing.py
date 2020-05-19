import cv2
import numpy as np
import math
from database import list_know_people_by_id, insert_people_access
from os import path, getcwd
from datetime import datetime
import core.face_detection as fd
import core.face_verification as fveri
import core.face_encoder as fencodeer

class faceproc:

    def __init__(self, resize_frame=4, camera_id=None):
        self.known_face_encodings = None
        self.known_face_names = None
        self.resize_frame = resize_frame
        self.camera_id = camera_id

    # detect face and use that face to compare known face fro reconition
    def detect_face_and_recognition(self, rgb_image=None):

        if self.known_face_encodings is None or self.known_face_names is None or rgb_image is None:
            raise AttributeError("known_face_encodings, known_face_encodings, rgb_image is None")

        face_predictions = []
        
        # detect face
        face_locations = fd.face_locations(rgb_image)
        # encode face lists
        face_encode = fencodeer.face_encodings(rgb_image, face_locations)

        # loop face list encode 
        for f_encode in face_encode:
            # compare known face encode and new face encode for checking
            matches = fveri.compare_faces(self.known_face_encodings, f_encode)

            name = 'Unknown'
            acc_percent = 0

            # calurate face distance for known face lists encode and unknow face encode
            face_distance = fveri.face_distance(self.known_face_encodings, f_encode)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                # calurate percent similar face 
                acc = math.floor(self.__face_distance_to_conf(face_distance[best_match_index]) * 100)
                # if accuracy face compare greater than 80 percent is know face otherwise unknow face
                if acc >= 80:
                    name = self.known_face_names[best_match_index]
                    acc_percent = acc

            # append name and accuracy in percent
            face_predictions.append((name, acc_percent))

        return face_locations, face_predictions

    # preapre output frame after process for showing
    def show_face_recognition(self, frame=None, face_locations=None, face_predictions=None):

        for (top, right, bottom, left), (kp_id, acc_percent) in zip(face_locations, face_predictions):
            top *= self.resize_frame
            right *= self.resize_frame
            bottom *= self.resize_frame
            left *= self.resize_frame

            face_box_color = (0, 0, 255)
            if acc_percent > 0:
                face_box_color = (255, 0, 0)

            cv2.rectangle(frame, (left, top), (right, bottom), face_box_color, 2)

            name = kp_id
            if acc_percent > 0:
                know_people = list_know_people_by_id(kp_id)
                if len(know_people) > 0:
                    person = know_people[0]
                    name = person[1]

            label_str = "{name} {percent}%".format(name=name, percent=acc_percent)
            (w, h), _ = cv2.getTextSize(label_str, cv2.FONT_HERSHEY_DUPLEX, 0.5, 1)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), face_box_color, cv2.FILLED)
            cv2.putText(frame, label_str, (left + 6, bottom - h), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        return frame

    # save unknow face to database
    def save_face(self, frame, face_locations, face_predictions):

        plot_2d_map = []
        _image_path = path.join(getcwd(), 'images')

        for (top, right, bottom, left), (kp_id, acc_percent) in zip(face_locations, face_predictions):

            top *= self.resize_frame
            right *= self.resize_frame
            bottom *= self.resize_frame
            left *= self.resize_frame

            # if unknown people access
            if acc_percent <= 0:
                plot_2d_map.append(0)
                crop_face = frame[top - 20:bottom, left + 5:right]
                cap_full_image_name = "cap_full_img-{}.jpg".format(datetime.now().strftime('%s'))
                cap_face_image_name = "cap_face_image-{}.jpg".format(datetime.now().strftime('%s'))
                cap_full_image_path = path.join(_image_path, cap_full_image_name)
                cap_face_image_path = path.join(_image_path, cap_face_image_name)

                # save image
                try:
                    cv2.imwrite(cap_face_image_path, crop_face)
                    cv2.imwrite(cap_full_image_path, frame.copy())
                    # insert to database
                    insert_people_access(kp_id, self.camera_id, cap_full_image_name, cap_face_image_name)
                except:
                    continue

    def set_face_encoding(self, face_encodings=None):
        self.known_face_encodings = face_encodings

    def set_face_names(self, face_names):
        self.known_face_names = face_names

    def set_resize_image(self, resize_img):
        self.resize_frame = resize_img

    def __face_distance_to_conf(self, face_distance, face_match_threshold=0.6):
        """
        calculate face acc
        """
        if face_distance > face_match_threshold:
            range = (1.0 - face_match_threshold)
            linear_val = (1.0 - face_distance) / (range * 2.0)
            return linear_val
        else:
            range = face_match_threshold
            linear_val = 1.0 - (face_distance / (range * 2.0))
            return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))
