from database.connector import connect_db
from utils.randomString import random_some_string
from sqlite3 import DatabaseError

know_people_column = ['kp_id', 'name', 'lname', 'age', 'sex', 'profile_image']


# add know people
def add_know_people(name=None, lname=None, age=None, sex=None):
    try:
        with connect_db() as conn:
            c = conn.cursor()
            sql = "INSERT INTO tb_know_people VALUES(?, ?, ?, ?, ?, NULL)"
            kp_id = random_some_string(10)
            c.execute(sql, (kp_id, name, lname, age, sex))
            conn.commit()
            return True
    except DatabaseError as e:
        print(e)
        return False


# update know people
def update_know_people(kp_id=None, name=None, lname=None, age=None, sex=None):
    try:
        with connect_db() as conn:
            c = conn.cursor()
            sql = "UPDATE tb_know_people SET name=?, lname=?, age=?, sex=? WHERE kp_id=?"
            c.execute(sql, (name, lname, age, sex, kp_id))
            conn.commit()
            return True
    except DatabaseError as e:
        print(e)
        return False


# delete know people
def delete_know_people(kp_id=None):
    try:
        with connect_db() as conn:
            c = conn.cursor()
            sql = "DELETE FROM tb_know_people WHERE kp_id=?"
            c.execute(sql, (kp_id,))
            conn.commit()
            return True
    except DatabaseError as e:
        print(e)
        return False


# list all know people
def list_all_know_people():
    with connect_db() as conn:
        c = conn.cursor()
        sql = "SELECT * FROM tb_know_people"
        c.execute(sql)
    return c.fetchall()


# list know people by kp_id
def list_know_people_by_id(kp_id=None):
    with connect_db() as conn:
        c = conn.cursor()
        sql = "SELECT * FROM tb_know_people WHERE kp_id=?"
        c.execute(sql, (kp_id,))
    return c.fetchall()


# update profile image
def change_profile_img(kp_id=None, profile_image=None):
    try:
        with connect_db() as conn:
            c = conn.cursor()
            sql = "UPDATE tb_know_people SET profile_image=? WHERE kp_id=?"
            c.execute(sql, (profile_image, kp_id))
            conn.commit()
            return True
    except DatabaseError as e:
        print(e)
        return False
