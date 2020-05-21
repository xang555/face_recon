from flask import Blueprint, jsonify, Response, send_file
from flask_jwt_extended import jwt_required
from core import reconnizer
from database import get_camera_by_camera_id
from os import path, getcwd

monitor = Blueprint('minotor', __name__)
reconnizer_arrs = {}


@monitor.route('/feed_video/<camera_id>')
@jwt_required
def feed_video(camera_id):
    global reconnizer_arrs
    if camera_id in reconnizer_arrs:
        rz = reconnizer_arrs[camera_id]
        return Response(rz.camera_generator(), mimetype="multipart/x-mixed-replace; boundary=frame")
    else:
        no_signal_img = path.join(getcwd(), 'asset', 'images_no_signal.jpg')
        return send_file(no_signal_img)


@monitor.route('/camera/start/<camera_id>', methods=['POST'])
@jwt_required
def start_camera_by_id(camera_id):
    global reconnizer_arrs
    if camera_id in reconnizer_arrs:
        return jsonify(msg='Already running'), 400

    cameras = get_camera_by_camera_id(camera_id)
    if len(cameras) <= 0:
        return jsonify(msg='No Camera ID'), 404
    cam = cameras[0]
    try:
        rz = reconnizer.Reconnizer(cam[0], cam[4], cam[5], cam[6], cam[7]).start_camera(frame_count_for_predict=5)
    except:
        return jsonify(msg='Start Camera {} Failed'.format(cam[1])), 503
    if rz is not None:
        reconnizer_arrs[cam[0]] = rz
    return jsonify(msg='Start Camera {} Success'.format(cam[1])), 200


@monitor.route('/camera/stop/<camera_id>', methods=['POST'])
@jwt_required
def stop_camera_by_id(camera_id):
    if camera_id in reconnizer_arrs:
        rz = reconnizer_arrs[camera_id]
        rz.stop_camera()
        del reconnizer_arrs[camera_id]
        return jsonify(msg='Stop camera success'), 200
    else:
        no_signal_img = path.join(getcwd(), 'images', 'no_signal.jpg')
        return send_file(no_signal_img)


@monitor.route('/camera/restart/<camera_id>', methods=['POST'])
@jwt_required
def restart_camera_by_id(camera_id):
    global reconnizer_arrs
    if camera_id in reconnizer_arrs:
        # stop camera
        rz = reconnizer_arrs[camera_id]
        rz.stop_camera()
        del reconnizer_arrs[camera_id]

    # start camera again
    cameras = get_camera_by_camera_id(camera_id)
    if len(cameras) <= 0:
        return jsonify(msg='No Camera ID'), 404
    cam = cameras[0]
    try:
        rz = reconnizer.Reconnizer(cam[0], cam[4], cam[5], cam[6], cam[7]).start_camera(frame_count_for_predict=5)
    except:
        return jsonify(msg='Start Camera {} Failed'.format(cam[1])), 503

    if rz is not None:
        reconnizer_arrs[cam[0]] = rz
    return jsonify(msg='restart Camera {} Success'.format(cam[1])), 200

