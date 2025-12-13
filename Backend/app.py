from flask import Flask, render_template, url_for, request, jsonify, send_from_directory
import os
import astar
import update_weight
import convertor
# Đường dẫn tuyệt đối đến thư mục Frontend
frontend_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../Frontend'))
map_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../map_data'))

# Tạo app, template_folder = Frontend, static_folder = Frontend luôn
app = Flask(
    __name__,
    template_folder=frontend_path,  # HTML files
    # CSS, JS, images trực tiếp trong Frontend
    static_folder=frontend_path,
    static_url_path='/'       # URL prefix
)

MAP_PATH = {
    "all": "../map_data/phuong_lang.graphml",
    "car": "../map_data/phuong_lang_drive.graphml",
    "bike": "../map_data/phuong_lang_bike.graphml",
    "walk": "../map_data/phuong_lang_walk.graphml",
    "motorcycle": "../map_data/phuong_lang_motorcycle.graphml",
}


def path(request):
    try:
        body = request.get_json()

        nodes = body["nodes"]
        vehicle = body["vehicle"]

        # print(nodes)

        nodes = convertor.coordinate_to_node(MAP_PATH[vehicle], nodes)

        print(nodes)
        if (len(nodes) == 2):
            path, length = astar.astar(
                MAP_PATH[vehicle], nodes[0], nodes[1], vehicle)
            print(path, length)
        else:
            print(nodes)

        # print(path)
        path = convertor.node_to_coordinate(MAP_PATH[vehicle], path)

        # path = convertor.test(MAP_PATH)
        # length = 0
        return {
            "state": "success",
            "path": path,
            "length": length
        }
    except:
        return {
            "state": "fail",
        }


@app.route('/full-graph', methods=["POST"])
def full_graph():
    body = request.get_json()

    vehicle = body["vehicle"]
    coords, nodes = convertor.test(MAP_PATH[vehicle])
    return {
        "state": "success",
        "path": coords,
        "nodes": nodes
    }


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/admin')
def home_admin():
    return render_template('admin.html')


@app.route('/path', methods=["GET", "POST"])
# Trả về danh sách các đỉnh trên đường đi
def _path():
    return path(request)


@app.route('/admin/path', methods=["GET", "POST"])
# Trả về danh sách các đỉnh trên đường đi
def _path_admin():
    path(request)


@app.route('/admin/update', methods=["POST"])
# cập nhật trạng thái đường đi
def update_admin():
    try:
        body = request.get_json()

        nodes = body["nodes"]
        vehicle = body["vehicle"]
        new_weight = body["new_weight"]

        nodes = convertor.coordinate_to_node(MAP_PATH[vehicle], nodes)

        if (len(nodes) == 2):
            update_weight.update_weight(
                MAP_PATH[vehicle], nodes[0], nodes[1], new_weight, vehicle)

        return {
            "state": "success"
        }
    except:
        return {
            "state": "fail"
        }


@app.route('/admin/ban_vehicle', methods=["POST"])
# cập nhật trạng thái đường đi
def ban_admin():
    try:
        body = request.get_json()

        nodes = body["nodes"]
        vehicle = body["vehicle"]
        # new_weight = body["new_weight"]

        nodes = convertor.coordinate_to_node(MAP_PATH[vehicle], nodes)

        if (len(nodes) == 2):
            update_weight.update_weight_one_vehicle(
                MAP_PATH[vehicle], nodes[0], nodes[1], 9999, vehicle)

        return {
            "state": "success"
        }
    except:
        return {
            "state": "fail"
        }


@app.route('/admin/unban_vehicle', methods=["POST"])
# cập nhật trạng thái đường đi
def unban_admin():
    try:
        body = request.get_json()

        nodes = body["nodes"]
        vehicle = body["vehicle"]
        # new_weight = body["new_weight"]

        nodes = convertor.coordinate_to_node(MAP_PATH[vehicle], nodes)

        if (len(nodes) == 2):
            update_weight.update_weight_one_vehicle(
                MAP_PATH[vehicle], nodes[0], nodes[1], 1, vehicle)

        return {
            "state": "success"
        }
    except:
        return {
            "state": "fail"
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
