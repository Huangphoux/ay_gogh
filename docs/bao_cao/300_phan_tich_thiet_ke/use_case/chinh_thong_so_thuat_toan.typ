#set heading(level: 4)
= Chỉnh thông số thuật toán

#figure(
  image("/out/docs/bao_cao/300_phan_tich_thiet_ke/use_case/Chỉnh thông số thuật toán.png"),
  caption: [Sơ đồ Use Case Chỉnh sửa hồ sơ],
)


#figure(
  table(
    [*Use Case*: Chỉnh thông số thuật toán],
    [*Tác nhân chính*: User ],
    [*Mô tả ngắn gọn*: Điều chỉnh Desired Retention và tối ưu các tham số.],
    [*Điều kiện tiên quyết*: Đã đăng nhập và có quyền chỉnh thông số.],
    [*Sự kiện kích hoạt*: Người dùng mở phần cài đặt thuật toán.],
    [*Điều kiện thực hiện*: Giá trị tham số trong phạm vi cho phép.],
    [*Luồng sự kiện chính*: 1) Mở cài đặt. 2) Chỉnh giá trị Desired Retention hoặc tham số khác. 3) Hệ thống kiểm tra hợp lệ. 4) Lưu và áp dụng cấu hình.],
  ),
  caption: [Bảng mô tả Use Case Chỉnh thông số thuật toán],
)
