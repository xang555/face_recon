import sqlite3 as sql
from os import path


# sqlite connection
def connect_db():
    dir_path = path.dirname(__file__)
    conn = sql.connect(path.join(dir_path, "db", "face_recon.db"))
    return conn


