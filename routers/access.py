from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required
from database import (query_unknown_people_access)
from os import path, getcwd

access = Blueprint('access', __name__)


@access.route('/search')
@jwt_required
def face_access_search():
    start_date = request.args.get('startDate')  # Unix Timestamp
    end_date = request.args.get('endDate')  # Unix Timestamp

    unknown_peoples = query_unknown_people_access(start_date, end_date)

    list_known_people_column = ['access_id', 'camera_id', 'cameraCode', 'cameraName', 'roomName', 'cap_full_image_path',
                                'face_image_path', 'detected_time']
    list_unknown_people_access = []
    for unknown_person in unknown_peoples:
        unknown_person_obj = {}
        for key, unknown_val in zip(list_known_people_column, unknown_person):
            unknown_person_obj[key] = unknown_val
        list_unknown_people_access.append(unknown_person_obj)

    return jsonify(list_unknown_people_access), 200


@access.route('/image/<filename>')
@jwt_required
def render_access_people_image(filename):
    images_dir = path.join(getcwd(), 'images')
    image_path = path.join(images_dir, filename)
    return send_file(image_path)

