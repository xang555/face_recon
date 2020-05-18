from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, jwt_required
)
from database import (findUser,
                      find_all_users, update_user, delete_user,
                      insertUser)
from datetime import timedelta

users = Blueprint('users', __name__)


# login
@users.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify(msg="Missing JSON in request"), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify(msg="Missing UserName and Password"), 400

    all_users = find_all_users()
    identity_data = {
        "user_id": "admin_000",
        "user_name": 'admin',
        "level": 1
    }
    if len(all_users) <= 0:
        if username != "admin" or password != "admin":
            return jsonify(msg="Bad Username and password"), 401
    else:
        match_user = findUser(username, password)
        if not match_user:
            return jsonify(msg="Bad Username and password"), 401

        identity_data['user_id'] = match_user[0]
        identity_data['user_name'] = match_user[1]
        identity_data['level'] = match_user[3]

    acces_token = create_access_token(identity=identity_data, expires_delta=timedelta(seconds=24 * 3600))
    return jsonify(access_token=acces_token), 200


# list all user
@users.route('/user', methods=['GET'])
@jwt_required
def list_all_user():
    all_user = find_all_users()

    lists_user = []
    lists_key = ["user_id", "username", "password", "level"]
    for user in all_user:
        user_dict = {}
        for key, val in zip(lists_key, user):
            if key == "password":
                continue
            user_dict[key] = val
        lists_user.append(user_dict)

    return jsonify(lists_user), 200


# Insert User
@users.route('/user/add', methods=['PUT'])
@jwt_required
def insert_user():
    if not request.is_json:
        return jsonify(msg="Missing JSON in request"), 400

    uname = request.json.get('username', None)
    passwd = request.json.get('password', None)
    level = request.json.get('level', None)

    if not uname or not passwd:
        return jsonify(msg="Missing UserName and Password"), 400

    if not level:
        level = 1

    if not insertUser(uname, passwd, level):
        return jsonify(msg="insert user failed"), 400

    return jsonify(msg='insert user success'), 200


# Update user
@users.route('/user/update', methods=['PATCH'])
@jwt_required
def change_user():
    if not request.is_json:
        return jsonify(msg="Missing JSON in request"), 400

    user_id = request.json.get('user_id', None)
    uname = request.json.get('username', None)
    passwd = request.json.get('password', None)
    level = request.json.get('level', None)

    if not uname or not passwd or not user_id:
        return jsonify(msg="Bad request"), 400

    if not level:
        level = 1

    if not update_user(user_id, uname, passwd, level):
        return jsonify(msg="Update user failed"), 400

    return jsonify(msg='update user Success'), 200


# delete user
@users.route('/user/delete', methods=['DELETE'])
@jwt_required
def del_user():
    if not request.is_json:
        return jsonify(msg="Missing JSON in request"), 400

    user_id = request.json.get('user_id', None)

    if not user_id:
        return jsonify(msg="Bad request"), 400

    if not delete_user(user_id):
        return jsonify(msg="Delete user failed"), 400

    return jsonify(msg='Delete user Success'), 200
