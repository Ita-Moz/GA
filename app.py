from flask import Flask, jsonify, render_template
import sys
sys.path.append('./db')
from mysql_helper import connect_to_mysql
app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    if(connect_to_mysql is None):
        print("Connection to MySQL database failed!")
        exit(1)
    cursor = connect_to_mysql.cursor()
    cursor.execute("SELECT * FROM subjects")
    result = cursor.fetchall()
    return jsonify(result)

@app.route ('/ga', methods=['GET'])
def get_ga():
    cursor = connect_to_mysql.cursor()
    cursor.execute("""
    SELECT courses.id,courses.name,courses.max_students, instructors.name
    FROM courses
    join instructors_subjects on courses.instructor_subject_id = instructors_subjects.id
    join instructors on instructors_subjects.instructor_id = instructors.id
    """)
    array_courses = cursor.fetchall()
    print(array_courses)
    return jsonify(array_courses)

@app.route('/', methods=['GET'])
def display_data():
    return render_template('index.html', data=get_data())


# chạy ứng dụng trên cổng 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
