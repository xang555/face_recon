from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required
from database import (list_all_know_people, list_know_people_by_id,
                      update_know_people, add_know_people, change_profile_img,
                      know_people_column, delete_know_people)
from werkzeug.utils import secure_filename
from os import getcwd, path, mkdir, listdir, remove
from shutil import rmtree
from utils import allowed_file
from core import face_encoder
import pickle

know_people = Blueprint('know_people', __name__)


@know_people.route('/all')
@jwt_required
def lists_all_know_people_route():
    know_peoples = list_all_know_people()
    list_know_peoples = []
    for person in know_peoples:
        person_dict = {}
        for col, val in zip(know_people_column, person):
            if col == 'profile_image':
                continue
            person_dict[col] = val
        list_know_peoples.append(person_dict)
    return jsonify(list_know_peoples), 200


@know_people.route('/add', methods=['PUT', 'POST'])
@jwt_required
def add_know_people_route():
    if not request.is_json:
        return jsonify(msg="Missing JSON in request"), 400

    name = request.json.get('name', None)
    lname = request.json.get('lname', None)
    age = request.json.get('age', None)
    sex = request.json.get('sex', None)

    if not name or not lname or not age or not sex:
        return jsonify(msg='Bad request'), 400

    if not add_know_people(name, lname, age, sex):
        return jsonify(msg='Add know people failed'), 400

    return jsonify(msg='add know people success'), 200


@know_people.route('/profile/upload', methods=['POST', 'PATCH'])
@jwt_required
def change_profile_img_route():
    kp_id = request.form['kp_id']
    f = request.files['profile_image']

    if not kp_id or not f:
        return jsonify(msg='Bad request'), 400

    if f.filename == '':
        return jsonify(msg='No selected image'), 400
    if not allowed_file(f.filename):
        return jsonify(msg='Please selected image'), 400

    know_people = list_know_people_by_id(kp_id)

    images_dir = path.join(getcwd(), 'images')
    if not path.exists(images_dir):
        mkdir(images_dir)

    profile_image_path = path.join(images_dir, secure_filename(f.filename))
    if not change_profile_img(kp_id=kp_id, profile_image=secure_filename(f.filename)):
        return jsonify(msg='change profile image failed'), 400
    try:
        if len(know_people) > 0:
            profile_image = path.join(images_dir, secure_filename(know_people[0][5]))
            if path.exists(profile_image):
                remove(profile_image)
    except:
        print("Delete old image failed")

    f.save(profile_image_path)
    return jsonify(msg='change profile image success'), 200


@know_people.route('/update', methods=['PATCH', 'POST'])
@jwt_required
def update_know_people_route():
    if not request.is_json:
        return jsonify(msg="Missing JSON in request"), 400

    kp_id = request.json.get('kp_id', None)
    name = request.json.get('name', None)
    lname = request.json.get('lname', None)
    age = request.json.get('age', None)
    sex = request.json.get('sex', None)

    if not kp_id or not name or not lname or not age or not sex:
        return jsonify(msg='Bad request'), 400

    if not update_know_people(kp_id, name, lname, age, sex):
        return jsonify(msg='Update know people failed'), 400

    return jsonify(msg='Update know people success'), 200


@know_people.route('/img/<kp_id>')
@jwt_required
def get_profile_image(kp_id):
    know_people = list_know_people_by_id(kp_id)
    if len(know_people) <= 0 or not know_people[0][5]:
        return jsonify(msg='No image'), 404
    profile_image_path = path.join(getcwd(), 'images', know_people[0][5])
    if not path.exists(profile_image_path):
        return jsonify(msg='Image not found in server'), 404
    return send_file(profile_image_path)


@know_people.route('/person/<kp_id>')
@jwt_required
def lists_know_people_by_id_route(kp_id):
    know_peoples = list_know_people_by_id(kp_id)
    person_dict = {}
    for person in know_peoples:
        for col, val in zip(know_people_column, person):
            if col == 'profile_image':
                continue
            person_dict[col] = val
    return jsonify(person_dict), 200


@know_people.route('/train/upload/<kp_id>', methods=['POST', 'PUT'])
@jwt_required
def upload_train_images(kp_id):
    know_peoples = list_know_people_by_id(kp_id)
    if len(know_peoples) <= 0:
        return jsonify(msg='No know person ID'), 200

    f = request.files.getlist('train_img')
    if len(f) <= 0:
        return jsonify(msg='Bad request, No file upload'), 400

    # check all file to upload is correct format
    is_upload = True
    for f_img in f:
        if f_img.filename == '':
            is_upload = False
            break

        if not f_img or not allowed_file(f_img.filename):
            is_upload = False
            break

    # if upload file not correct format
    if not is_upload:
        return jsonify(msg='Bad file to upload'), 400

    # create upload folder
    dataset_dir = path.join(getcwd(), 'dataset')
    if not path.exists(dataset_dir):
        mkdir(dataset_dir)
    root_img_path = path.join(dataset_dir, kp_id)
    if not path.exists(root_img_path):
        mkdir(root_img_path)
    # save file
    for f_img in f:
        img_path = path.join(root_img_path, secure_filename(f_img.filename))
        f_img.save(img_path)

    return jsonify(msg='upload train images success'), 200


@know_people.route('/train/img/<kp_id>')
@jwt_required
def get_train_images(kp_id):
    data_set = path.join(getcwd(), 'dataset', kp_id)
    if not path.exists(data_set):
        return jsonify(images=[]), 404
    list_files = listdir(data_set)
    return jsonify(images=list_files)


@know_people.route('/train/img/<kp_id>/<filename>')
@jwt_required
def render_train_image(kp_id, filename):
    data_set_img = path.join(getcwd(), 'dataset', kp_id, secure_filename(filename))
    if not path.exists(data_set_img):
        return jsonify(msg='No image'), 404
    return send_file(data_set_img)


@know_people.route('/train/img/<kp_id>/<filename>', methods=['DELETE'])
@jwt_required
def delete_train_image(kp_id, filename):
    data_set_img = path.join(getcwd(), 'dataset', kp_id, secure_filename(filename))
    if not path.exists(data_set_img):
        return jsonify(msg='No image'), 404
    try:
        remove(data_set_img)
    except:
        return jsonify(msg='delete failed'), 501

    return jsonify(msg='delete success'), 200


@know_people.route('/delete', methods=['DELETE'])
@jwt_required
def delete_know_people_route():
    if not request.is_json:
        return jsonify(msg='Missing json request'), 400
    kp_id = request.json.get('kp_id', None)
    if not kp_id:
        return jsonify(msg='Bad request'), 400

    know_people = list_know_people_by_id(kp_id)
    data_set_img = path.join(getcwd(), 'dataset', kp_id)

    if not delete_know_people(kp_id):
        return jsonify(msg='Delete Failed'), 503

    try:
        if len(know_people) > 0:
            profile_image = path.join(getcwd(), 'images', secure_filename(know_people[0][5]))
            if path.exists(profile_image):
                remove(profile_image)
        if path.exists(data_set_img):
            rmtree(data_set_img)
    except:
        print("Delete file Failed")
    return jsonify(msg='Delete Success'), 200


@know_people.route('/train/run', methods=['POST'])
@jwt_required
def run_train_face():
    train_encoding_path = path.join(getcwd(), 'train')
    if not path.exists(train_encoding_path):
        mkdir(train_encoding_path)
    dataset_path = path.join(getcwd(), 'dataset')
    if not path.exists(dataset_path):
        return jsonify(msg='No data for train'), 404
    list_images_dir_name = listdir(dataset_path)
    all_face_encodings = {}
    for image_dir_name in list_images_dir_name:
        image_dir_path = path.join(dataset_path, image_dir_name)
        list_train_images = listdir(image_dir_path)
        for image_name in list_train_images:
            image_path = path.join(image_dir_path, image_name)
            img_encode = face_encoder.encode(image_path)
            if img_encode is None:
                continue
            all_face_encodings[image_dir_name] = img_encode
            break

    with open(path.join(train_encoding_path, "dataset_faces.pck"), 'wb') as f:
        pickle.dump(all_face_encodings, f)

    return jsonify(msg='Train success'), 200
