from flask import Flask, render_template, url_for
import os

# Đường dẫn tuyệt đối đến thư mục Frontend
frontend_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../Frontend'))

# Tạo app, template_folder = Frontend, static_folder = Frontend luôn
app = Flask(
    __name__,
    template_folder=frontend_path,  # HTML files
    static_folder=frontend_path,    # CSS, JS, images trực tiếp trong Frontend
    static_url_path='/'       # URL prefix
)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/admin')
def home_admin():
    return render_template('admin.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
