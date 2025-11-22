document.addEventListener("DOMContentLoaded", () => {
  // 1. Lấy các phần tử cần thiết bằng ID
  const toggleButton = document.getElementById("toggle-admin-mode");
  const userModePanel = document.getElementById("user-mode");
  const adminModePanel = document.getElementById("admin-mode");

  let isAdminMode = false;

  toggleButton.addEventListener("click", () => {
    isAdminMode = !isAdminMode;

    if (isAdminMode) {
      // Chuyển sang chế độ Admin
      userModePanel.classList.remove("active");
      adminModePanel.classList.add("active");

      toggleButton.textContent = "Chế Độ Người Dùng";
      toggleButton.style.backgroundColor = "#28a745";
    } else {
      // Chuyển về chế độ Người dùng
      adminModePanel.classList.remove("active");
      userModePanel.classList.add("active");

      toggleButton.textContent = "Chế Độ Admin";
      toggleButton.style.backgroundColor = "#6c757d";
    }
  });

  // TODO: Thêm logic gọi API cho các nút Tìm Đường và Cập Nhật Đường Đi tại đây
});
