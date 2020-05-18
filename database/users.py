from utils import hashPassword, random_some_string
from database.connector import connect_db
from sqlite3 import DatabaseError


# find user
def findUser(uname=None, passwd=None):
    with connect_db() as conn:
        c = conn.cursor()
        query = "SELECT * from tb_users WHERE username=? AND password=?"
        c.execute(query, (uname, hashPassword(passwd)))
        match_lists = c.fetchone()
    return match_lists


# find all user
def find_all_users():
    with connect_db() as conn:
        c = conn.cursor()
        query = "SELECT * from tb_users"
        c.execute(query)
    return c.fetchall()


# insert users
def insertUser(uname=None, password=None, level=1):
    try:
        with connect_db() as conn:
            c = conn.cursor()
            query = "INSERT INTO tb_users VALUES (?, ?, ?, ?)"
            user_id = random_some_string()
            c.execute(query, (user_id, uname, hashPassword(password), level))
            conn.commit()
        return True
    except DatabaseError as e:
        print(e)
        return False


# update user
def update_user(user_id=None, uname=None, passwd=None, level=1):
    try:
        with connect_db() as conn:
            c = conn.cursor()
            query = "UPDATE tb_users SET username=?, password=?, level=? WHERE user_id=?"
            c.execute(query, (uname, hashPassword(passwd), level, user_id))
            conn.commit()
        return True
    except DatabaseError as e:
        print(e)
        return False


# delete users
def delete_user(user_id):
    try:
        with connect_db() as conn:
            c = conn.cursor()
            query = "DELETE FROM tb_users WHERE user_id=?"
            c.execute(query, (user_id,))
            conn.commit()
        return True
    except DatabaseError as e:
        print(e)
        return False
