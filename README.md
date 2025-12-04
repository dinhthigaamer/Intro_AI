# Intro_AI

# Hướng dẫn
- Mỗi người tạo brach của mình để push code, ko push trực tiếp lên main
- Tải các packet cần ở requirement
- Nếu bổ sung thêm packet nào, ghi vào requirement, không push cả gói lên repo. 

# API:
Xem ở phần app.py
- .../path: Tìm đường đi giữa 2 đỉnh
  + start: id đỉnh bắt đầu 
  + target: id đỉnh kết thúc trong đồ thị
  + vehicle: phương tiện, mặc định là car
- update_weight: Cập nhật đường đi
  + start
  + target
  + new_weight: trọng số mới cần cập nhật, mặc định = 1
  + vehicle
