import face_recognition as fr
import cv2
import core.face_detection as fd


# encode face
def encode(image_path=None):
    image = fr.load_image_file(image_path)
    image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
    face_locations = fd.face_locations(image)
    face_encodings = fr.face_encodings(image, face_locations, num_jitters=2)

    if len(face_encodings) != 1:
        print("{} no face or more than 1 face".format(image_path))
        return None

    return face_encodings[0]
