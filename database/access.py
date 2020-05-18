from database.connector import connect_db
from sqlite3 import Error
from datetime import datetime, timezone


# insert access people
def insert_people_access(kp_id, camera_id, full_img_path, face_img_path):
    try:
        with connect_db() as conn:
            c = conn.cursor()
            sql = 'INSERT INTO tb_access (kp_id, camera_id, cap_full_image_path, face_image_path, detected_time)' \
                  ' VALUES(?, ?, ?, ?, ?)'
            dt = datetime.now(timezone.utc).isoformat()
            c.execute(sql, (kp_id, camera_id, full_img_path, face_img_path, dt))
            conn.commit()
        return True
    except Error as e:
        print(e)
        return False


# select access unknown people from datetime
def query_unknown_people_access(start_date, end_date):
    with connect_db() as conn:
        c = conn.cursor()
        sql = 'SELECT * FROM v_unknown_people_access WHERE detected_time >= ? AND detected_time <= ?'
        c.execute(sql, (start_date, end_date))
    return c.fetchall()
