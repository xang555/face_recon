from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from database import (get_camera_by_camera_id, update_camera,
                      add_camera, delete_camera, list_all_camera)

camera = Blueprint('camera', __name__)

table_column = ['camera_id', 'cameraCode', 'cameraName', 'roomName', 'username', 'password', 'ip', 'port']


# list all cameras
@camera.route('/lists', methods=['GET'])
@jwt_required
def list_camera():
    cameras = list_all_camera()
    list_camera_data = []
    for _camera_ in cameras:
        camera_dict = {}
        for cam_val, label in zip(_camera_, table_column):
            camera_dict[label] = cam_val
        list_camera_data.append(camera_dict)
    return jsonify(list_camera_data), 200


# get camrea by camera_id
@camera.route('/<camera_id>')
@jwt_required
def list_camera_by_camera_id(camera_id):
    __camera__ = get_camera_by_camera_id(camera_id)
    camera_dict = {}
    if len(__camera__) <= 0:
        return jsonify(camera_dict), 200

    for cam_val, label in zip(__camera__[0], table_column):
        camera_dict[label] = cam_val

    return jsonify(camera_dict), 200


# add camrea
@camera.route('/add', methods=['PUT'])
@jwt_required
def add_camera_route():
    if not request.is_json:
        return jsonify(msg="Missing JSON in request"), 400
    camera_code = request.json.get('camera_code', None)
    camera_name = request.json.get('camera_name', None)
    room_name = request.json.get('room_name', None)
    user_name = request.json.get('user_name', None)
    password = request.json.get('password', None)
    ip = request.json.get('ip', None)
    port = request.json.get('port', None)
    if not camera_code or not camera_name or not room_name or not user_name or not password or not ip or not port:
        return jsonify(msg="Bad request, Incorrect body parameter"), 400

    if not add_camera(camera_code, camera_name, room_name, user_name, password, ip, port):
        return jsonify(msg="add Camera Failed"), 400

    return jsonify(msg="add camera Success"), 200


# update camera
@camera.route('/update', methods=['PATCH'])
@jwt_required
def update_camera_route():
    if not request.is_json:
        return jsonify(msg="Missing JSON in request"), 400

    camera_id = request.json.get('camera_id', None)
    camera_code = request.json.get('camera_code', None)
    camera_name = request.json.get('camera_name', None)
    room_name = request.json.get('room_name', None)
    user_name = request.json.get('user_name', None)
    password = request.json.get('password', None)
    ip = request.json.get('ip', None)
    port = request.json.get('port', None)
    if not camera_id or not camera_code or not camera_name or not room_name or not user_name or not password or not ip or not port:
        return jsonify(msg="Bad request, Incorrect body parameter"), 400

    if not update_camera(camera_id, camera_code, camera_name, room_name, user_name, password, ip, port):
        return jsonify(msg="update Camera Failed"), 400

    return jsonify(msg="update camera Success"), 200


# delete camera
@camera.route('/delete', methods=['DELETE'])
@jwt_required
def delete_camera_route():
    if not request.is_json:
        return jsonify(msg="Missing JSON in request"), 400

    camera_id = request.json.get('camera_id', None)

    if not camera_id:
        return jsonify(msg="Bad request, Incorrect body parameter"), 400

    if not delete_camera(camera_id):
        return jsonify(msg="delete Camera Failed"), 400

    return jsonify(msg="delete camera Success"), 200
