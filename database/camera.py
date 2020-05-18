from database.connector import connect_db
from utils.randomString import random_some_string
from sqlite3 import Error


# List cameras
def list_all_camera():
    with connect_db() as conn:
        c = conn.cursor()
        sql = "SELECT * from tb_camera"
        c.execute(sql)
        cameras = c.fetchall()
    return cameras


# get camera by id
def get_camera_by_camera_id(camera_id):
    with connect_db() as conn:
        c = conn.cursor()
        sql = "SELECT * from tb_camera WHERE camera_id=?"
        c.execute(sql, (camera_id,))
        cameras = c.fetchall()
    return cameras


# add camera
def add_camera(camera_code=None, camera_name=None, room_name=None,
               username=None, password=None, ip=None, port=554):
    try:
        with connect_db() as conn:
            c = conn.cursor()
            sql = "INSERT INTO tb_camera VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
            camera_id = random_some_string(10)
            c.execute(sql, (camera_id, camera_code, camera_name, room_name, username, password, ip, port))
            conn.commit()
        return True
    except Error as e:
        print(e)
        return False


# update camera
def update_camera(camera_id=None, camera_code=None, camera_name=None, room_name=None,
                  username=None, password=None, ip=None, port=554):
    try:
        with connect_db() as conn:
            c = conn.cursor()
            sql = "UPDATE tb_camera set cameraCode=?, cameraName=?, roomName=?, userName=?, password=?, ip=?, port=?" \
                  "WHERE " \
                  "camera_id=? "
            c.execute(sql, (camera_code, camera_name, room_name, username, password, ip, port, camera_id))
            conn.commit()
        return True
    except Error as e:
        print(e)
        return False


# delete camera
def delete_camera(camera_id):
    try:
        with connect_db() as conn:
            c = conn.cursor()
            sql = "DELETE FROM tb_camera WHERE camera_id=?"
            c.execute(sql, (camera_id,))
            conn.commit()
        return True
    except Error as e:
        print(e)
        return False
