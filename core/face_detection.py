from mtcnn.mtcnn import MTCNN
import PIL.Image
import numpy as np

detector = MTCNN()

# find face form mat image
def face_locations(img):
    boxes = []
    face_boxes = detector.detect_faces(img)
    for loc in face_boxes:
        (x, y, w, h) = loc['box']
        box = refined_box(x, y, w, h)
        boxes.append(box)
    return boxes


# laod image from file
def load_image_file(file, mode='RGB'):
    im = PIL.Image.open(file)
    if mode:
        im = im.convert(mode)
    return np.array(im)

# convert localization face
def refined_box(left, top, width, height):
    right = left + width
    bottom = top + height

    original_vert_height = bottom - top
    top = int(top + original_vert_height * 0.15)
    bottom = int(bottom - original_vert_height * 0.05)

    margin = ((bottom - top) - (right - left)) // 2
    left = left - margin if (bottom - top - right + left) % 2 == 0 else left - margin - 1

    right = right + margin

    return top, right, bottom, left
