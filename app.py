import mysql.connector
from flask import Flask, jsonify, render_template
import config
app = Flask(__name__)

# lấy các thông số từ file config.py
app.config.from_object(config)
# kết nối đến database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=app.config['PASSWORD_DB'],
    database=app.config['DATABASE_NAME']
)

# tạo API để lấy dữ liệu từ database

@app.route('/data', methods=['GET'])
def get_data():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM subject")
    result = cursor.fetchall()
    return jsonify(result)


@app.route('/', methods=['GET'])
def display_data():
    return render_template('index.html', data='xinchao', title='Trang chủ')


# chạy ứng dụng trên cổng 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)
