from flask import Flask, jsonify, render_template
import mysql.connector
from mysql.connector import errorcode

DB_PASSWORD = 'admin'
DB_NAME= 'GA'
DB_HOST = 'localhost'
DB_USER = 'root'
def connect_to_mysql(host, database_name, user_name, password):
    """
    Kết nối đến MySQL database.
    Args:
        host (str): địa chỉ host của MySQL database.
        database_name (str): tên của database cần kết nối.
        user_name (str): tên đăng nhập cho MySQL.
        password (str): mật khẩu đăng nhập cho MySQL.
    Returns:
        mysql.connector.connection_cext.CMySQLConnection or None: đối tượng connection cho kết nối thành công hoặc None nếu kết nối thất bại.
    Raises:
        mysql.connector.Error: Nếu kết nối đến database thất bại.
    """
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user_name,
            password=password,
            database=database_name
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        # Check connection
        if mydb.is_connected():
            print("Connecting to MySQL database...")
            db_Info = mydb.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            return mydb
        else:
            return None

# Connect to MySQL database
mydb = connect_to_mysql(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
if mydb is None:
    print("Connection to MySQL database failed!")
    exit(1)

mycursor = mydb.cursor()

# # DATABASE OF TIMETABLE GENERATOR GA
# # Create table subjects
# # TODO: NULL
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS subjects (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     name VARCHAR(255) NOT NULL,
#     number_of_periods VARCHAR(255) NULL
# )
# """)
# # Create table instructors
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS instructors (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, 
#     name VARCHAR(60) NOT NULL, 
#     sex VARCHAR(10), 
#     email VARCHAR(40) NULL, 
#     phone_number VARCHAR(15) NULL,
#     address VARCHAR(255) NULL
# )
# """)

# # Create table instructors_subjects (Bảng trung gian thể hiện mối quan hệ N-N giữa instructors và subjects)
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS instructors_subjects (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     subject_id INT NOT NULL,
#     instructor_id INT NOT NULL,
#     FOREIGN KEY (subject_id) REFERENCES subjects(id),
#     FOREIGN KEY (instructor_id) REFERENCES instructors(id)
# )
# """)

# # Create table populations
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS populations (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     size INT NOT NULL,
#     generation INT,
#     fitness DECIMAL(10.3)
# )   
# """)

# # TODO: NULL
# # Create table schedules
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS schedules (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     population_id INT NOT NULL,
#     fitness DECIMAL(10.3) NULL
# )
# """)

# # TODO: NULL
# # Create table courses
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS courses (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     name VARCHAR(255) NOT NULL,
#     max_students INT NOT NULL,
#     instructor_subject_id INT NOT NULL,
#     schedules_id INT ,
#     FOREIGN KEY (instructor_subject_id) REFERENCES instructors_subjects(id),
#     FOREIGN KEY (schedules_id) REFERENCES schedules(id)
# )
# """)

# # Create table timelessons
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS timelessons (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     uuid VARCHAR(6) NOT NULL,
#     period VARCHAR(255)
# )
# """)

# # Create table rooms
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS rooms (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     name VARCHAR(15) NOT NULL,
#     capacity INT NOT NULL,
#     type VARCHAR(15)
# )
# """)

# # Create table rooms_timelessons (Bảng trung gian thể hiện mối quan hệ N-N giữa rooms và timelessons)
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS rooms_timelessons (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     room_id INT NOT NULL,
#     timelesson_id INT NOT NULL,
#     FOREIGN KEY (room_id) REFERENCES rooms(id),
#     FOREIGN KEY (timelesson_id) REFERENCES timelessons(id)
# )
# """)

# ====================================================================
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS subjects (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     name VARCHAR(255) NOT NULL,
#     number_of_periods VARCHAR(255) NULL
# )
# """)
# # Create table instructors
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS instructors (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, 
#     name VARCHAR(60) NOT NULL, 
#     sex VARCHAR(10), 
#     email VARCHAR(40) NULL, 
#     phone_number VARCHAR(15) NULL,
#     address VARCHAR(255) NULL
# )
# """)
# # Create table populations
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS populations (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     size INT NOT NULL,
#     generation INT,
#     fitness DECIMAL(10.3)
# )   
# """)

# # TODO: NULL
# # Create table schedules
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS schedules (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     population_id INT NOT NULL,
#     fitness DECIMAL(10.3) NULL
# )
# """)

# # TODO: NULL
# # Create table courses
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS courses (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     name VARCHAR(255) NOT NULL,
#     max_students INT NOT NULL,
#     instructor_subject_id INT NOT NULL,
#     schedules_id INT ,
#     FOREIGN KEY (instructor_subject_id) REFERENCES instructors_subjects(id),
#     FOREIGN KEY (schedules_id) REFERENCES schedules(id)
# )
# """)

# # Create table timelessons
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS timelessons (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     uuid VARCHAR(6) NOT NULL,
#     period VARCHAR(255)
# )
# """)

# # Create table rooms
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS rooms (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     name VARCHAR(15) NOT NULL,
#     capacity INT NOT NULL,
#     type VARCHAR(15)
# )
# """)
# # Create table instructors_subjects (Bảng trung gian thể hiện mối quan hệ N-N giữa instructors và subjects)
# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS instructors_subjects (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     subject_id INT NOT NULL,
#     instructor_id INT NOT NULL,
#     FOREIGN KEY (subject_id) REFERENCES subjects(id),
#     FOREIGN KEY (instructor_id) REFERENCES instructors(id)
# )
# """)

# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS rooms_timelessons (
#     id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     room_id INT NOT NULL,
#     timelesson_id INT NOT NULL,
#     FOREIGN KEY (room_id) REFERENCES rooms(id),
#     FOREIGN KEY (timelesson_id) REFERENCES timelessons(id)
# )
# """)

# mycursor.execute("""
# CREATE TABLE classes (
#   id INT NOT NULL AUTO_INCREMENT,
#   course_id INT NOT NULL,
#   room_id INT NOT NULL,
#   timelesson_id INT NOT NULL,
#   schedule_id INT NOT NULL,
#   PRIMARY KEY (id),
#   FOREIGN KEY (course_id) REFERENCES courses(id),
#   FOREIGN KEY (room_id) REFERENCES rooms(id),
#   FOREIGN KEY (timelesson_id) REFERENCES timelessons(id),
#   FOREIGN KEY (schedule_id) REFERENCES schedules(id)
# )
# """)
# ===============================================================
mycursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    number_of_periods VARCHAR(255) NULL
)
""")
# Create table instructors
mycursor.execute("""
CREATE TABLE IF NOT EXISTS instructors (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, 
    name VARCHAR(60) NOT NULL, 
    sex VARCHAR(10), 
    email VARCHAR(40) NULL, 
    phone_number VARCHAR(15) NULL,
    address VARCHAR(255) NULL
)
""")

# Create table instructors_subjects (Bảng trung gian thể hiện mối quan hệ N-N giữa instructors và subjects)
mycursor.execute("""
CREATE TABLE IF NOT EXISTS instructors_subjects (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    subject_id INT NOT NULL,
    instructor_id INT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (instructor_id) REFERENCES instructors(id)
)
""")

# TODO: NULL
# Create table schedules
mycursor.execute("""
CREATE TABLE IF NOT EXISTS schedules (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    fitness DECIMAL(10.3) NULL
)
""")

# TODO: NULL
# Create table courses
mycursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    max_students INT NOT NULL,
    instructor_subject_id INT NOT NULL,
    schedules_id INT ,
    FOREIGN KEY (instructor_subject_id) REFERENCES instructors_subjects(id)
)
""")

# Create table timelessons
mycursor.execute("""
CREATE TABLE IF NOT EXISTS timelessons (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    uuid VARCHAR(6) NOT NULL,
    period VARCHAR(255)
)
""")

# Create table rooms
mycursor.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(15) NOT NULL,
    capacity INT NOT NULL,
    type VARCHAR(15)
)
""")

mycursor.execute("""
CREATE TABLE classes (
  id INT NOT NULL AUTO_INCREMENT,
  course_id INT NOT NULL,
  room_id INT NOT NULL,
  timelesson_id INT NOT NULL,
  schedule_id INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (course_id) REFERENCES courses(id),
  FOREIGN KEY (room_id) REFERENCES rooms(id),
  FOREIGN KEY (timelesson_id) REFERENCES timelessons(id),
  FOREIGN KEY (schedule_id) REFERENCES schedules(id)
)
""")