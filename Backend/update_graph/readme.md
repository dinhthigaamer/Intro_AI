Mô tả chức năng:
- update_weight.update_weight(xu, yu, xv, yv, new_weight=1): Cập nhật trọng số đường đi u->v
    + xu, yu, xv, yv là toạ độ đỉnh đầu và đỉnh cuối
    + new_weight: trọng số mới
    + path = shortest_path_func(xu, yu, xv, yv): Phần này gọi API từ phần tìm đường đi ngắn nhất của Minh, trả về danh sách các đỉnh trên đường đi từ u -> v.