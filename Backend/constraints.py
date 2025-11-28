# ---------------------------
# QUY TẮC CHO Ô TÔ
# ---------------------------
def allow_car(edge):
    banned = {"footway", "cycleway", "path", "steps", "pedestrian"}
    
    if edge["highway"] in banned:
        return False
    
    if edge["access"] in {"no", "private"}:
        return False

    if edge["width"] < 3.0:
        return False  # đường quá hẹp

    return True


# ---------------------------
# QUY TẮC CHO XE MÁY
# ---------------------------
def allow_motorcycle(edge):
    banned = {"footway", "cycleway", "steps", "pedestrian"}

    if edge["highway"] in banned:
        return False

    if edge["access"] in {"motorcycle=no", "no"}:
        return False
    
    if edge["width"] < 1.2:
        return False  # hẻm quá nhỏ

    return True


# ---------------------------
# QUY TẮC CHO ĐI BỘ
# ---------------------------
def allow_walk(edge):
    banned = {"motorway", "trunk"}

    if edge["highway"] in banned:
        return False

    if edge["access"] in {"private"}:
        return False

    return True


# ---------------------------
# LẤY HÀM KIỂM TRA THEO TÊN PHƯƠNG TIỆN
# ---------------------------
def get_constraint(vehicle):
    if vehicle == "car":
        return allow_car
    if vehicle == "motorcycle":
        return allow_motorcycle
    if vehicle == "walk":
        return allow_walk

    raise ValueError("Phương tiện không hợp lệ!")
