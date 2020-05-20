import cv2
import numpy as np
import threading
from os import path, getcwd
import pickle
from core.face_processing import faceproc
from core.IpcameraStream import IpcameraStream
from time import time
import logging

class Reconnizer:

    def __init__(self, camera_id=None, user_name=None, password=None, ip=None, port=None):
        self.camera_id = camera_id
        self.camera_uri = "rtsp://{username}:{password}@{ip}:{port}/Streaming/Channels/101/".format(
            username=user_name, password=password, ip=ip, port=port
        )
        self.is_running = True
        self.my_threading = None
        self.outputFrame = None
        self.lock = threading.Lock()
        self.ips = None

        # load dataset face
        dataset_face_path = path.join(getcwd(), "train", "dataset_faces.pck")
        if not path.exists(dataset_face_path):
            raise Exception('No dataset found, please train first!')
        with open(dataset_face_path, 'rb') as f:
            all_face_encodings = pickle.load(f)
        face_names = list(all_face_encodings.keys())
        face_encodings = np.array(list(all_face_encodings.values()))

        # init face processing
        self.face_proc = faceproc(camera_id=self.camera_id, resize_frame=4)
        self.face_proc.set_face_encoding(face_encodings)
        self.face_proc.set_face_names(face_names)

    # process camera
    def camera_processing(self, frame_count_for_predict=10):
        process_this_frame = frame_count_for_predict - 1
        face_locations = []
        face_predictions = []
        face_count_temp = -1
        diff_frame_count = 4

        while self.is_running:
            frame = self.ips.read()

            if frame is None or np.shape(frame) == ():
                continue

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            process_this_frame = process_this_frame + 1
            if process_this_frame % frame_count_for_predict == 0:

                # detect and recognition face
                face_locations, face_predictions = self.face_proc.detect_face_and_recognition(
                    rgb_small_frame.copy())

                # check different face count per frame
                if len(face_predictions) != face_count_temp:
                    diff_frame_count += 1

                    # check if people in 3 frame
                    if diff_frame_count >= 3:
                        print("save image")
                        self.face_proc.save_face(frame.copy(), face_locations, face_predictions)
                        face_count_temp = len(face_predictions)
                        diff_frame_count = 0
                else:
                    diff_frame_count = 0

                # restart processing
                process_this_frame = 0

            frame = self.face_proc.show_face_recognition(frame.copy(), face_locations, face_predictions)

            if self.lock:
                self.outputFrame = frame.copy()

    # stream generator function
    def camera_generator(self):
        while True:
            with self.lock:
                if self.outputFrame is None or np.shape(self.outputFrame) == ():
                    logging.warning("no output frame")
                    continue
                flag, encodedImage = cv2.imencode(".png", self.outputFrame)
                if not flag:
                    logging.warning("can not encode to image")
                    continue
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                       bytearray(encodedImage) + b'\r\n')

    # read output frame
    def read(self):
        if self.lock:
            return self.outputFrame

    # start camera
    def start_camera(self, frame_count_for_predict=10):
        try:
            self.ips = IpcameraStream(self.camera_uri).start()
            self.my_threading = threading.Thread(target=self.camera_processing, name=self.camera_id,
                                                 args=(frame_count_for_predict,), daemon=True)
            self.my_threading.start()
        except:
            raise Exception("Can not start camera")
        return self

    # stop camera
    def stop_camera(self):
        self.ips.stop()
        self.is_running = False
        if self.my_threading is not None:
            self.my_threading.join()
