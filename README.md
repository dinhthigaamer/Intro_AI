# Intro_AI

# Hướng dẫn

- Mỗi người tạo brach của mình để push code, ko push trực tiếp lên main
- Tải các packet cần ở requirement
- Nếu bổ sung thêm packet nào, ghi vào requirement, không push cả gói lên repo.

# API:

Xem ở phần app.py

Dữ liệu truyền vào từ FE dưới dạn json

- /path, /admin/path: Tìm đường đi giữa 2 đỉnh

  + "start": string, id đỉnh bắt đầu
  + "target": string,  id đỉnh kết thúc trong đồ thị
  + "vehicle": string, phương tiện, có thể nhận ["car", "walk", "motorcycle"]

  => Kết quả nhận 1 json

  - Thành công tìm được đường:

  {"state": "success", "path": Danh sách đỉnh trên đường đi, "len": độ dài đường đi}

  Tìm thất bại: {"state": "fail"}
- /admin/update: Cập nhật đường đi

  + start
  + target
  + "new_weight": float,  trọng số mới cần cập nhật, mặc định = 1
  + vehicle

  Thành công: {"state": "success"}


  Thất bại: {"state": "fail"}
