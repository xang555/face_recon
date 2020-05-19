import numpy as np
from scipy.spatial.distance import cosine

# calurate face distance using cosine
def face_distance(face_encodings, face_to_compare):
    if len(face_encodings) == 0:
        return np.empty((0))
    return np.asarray([cosine(fencode, face_to_compare) for fencode in face_encodings])

# compare faces
def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    return list(face_distance(known_face_encodings, face_encoding_to_check) <= tolerance)


if __name__ == "__main__":
    u = np.array([[0, 1, 0, 1, 0], [1, 1, 0, 1, 1]])
    v = np.array([1, 0, 0, 1, 1])
    print(face_distance(u, v))