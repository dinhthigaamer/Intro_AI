from flask import Flask, render_template
import os

# Xác định đường dẫn tuyệt đối đến thư mục Frontend
frontend_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../Frontend'))

# Tạo app, chỉ định template_folder
app = Flask(__name__, template_folder=frontend_path)


@app.route('/')
def home():
    return render_template('user.html')  # Chỉ cần tên file


@app.route('/admin')
def home_admin():
    return render_template('admin.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
