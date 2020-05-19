import cv2
import core.face_detection as fd
from keras_vggface import VGGFace
from keras_vggface.utils import preprocess_input
from core.face_detection import face_locations, load_image_file
import numpy as np

# encode face from image
def face_encode_from_file(image_path=None):
    image = load_image_file(image_path)
    image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
    face_box_locations = face_locations(image)
    __face_encodings__ = face_encodings(image, face_box_locations)

    if len(__face_encodings__) != 1:
        print("{} no face or more than 1 face".format(image_path))
        return None

    return __face_encodings__[0]


# get face from image
def get_face(image, face_box):
    # extract position face
    top, right, bottom, left = face_box
    face = image[top:bottom, left:right]
    img = cv2.resize(face, (224, 224))
    return img

# extract faces and calculate face embeddings for a list of photo files
def face_encodings(image, face_locations):
    faces = [get_face(image, face_box) for face_box in face_locations]
    samples = np.asarray(faces, dtype=np.float32)
    samples = preprocess_input(samples, version=2)
    model = VGGFace(model='resnet50', include_top=False,
                    input_shape=(224, 224, 3), pooling='avg')
    yhat = model.predict(samples)
    return yhat
