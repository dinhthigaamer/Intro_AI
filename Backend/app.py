from flask import Flask, render_template, url_for
import os
import astar
import update_weight
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


@app.route('/path')
# Trả về danh sách các đỉnh trên đường đi
def path(start, target, vehicle):
    return astar.astar(start, target, vehicle)


@app.route('/admin/path')
# Trả về danh sách các đỉnh trên đường đi
def path_admin(start, target, vehicle):
    return astar.astar(start, target, vehicle)


@app.route('/admin/update')
# cập nhật trạng thái đường đi
def update_admin(start, target, new_weight=1, vehicle=None):
    update_weight.update_weight(start, target, new_weight, vehicle)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
