from mtcnn.mtcnn import MTCNN

detector = MTCNN()


def face_locations(img):
    boxes = []
    face_boxes = detector.detect_faces(img)
    for loc in face_boxes:
        (x, y, w, h) = loc['box']
        box = refined_box(x, y, w, h)
        boxes.append(box)
    return boxes


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
