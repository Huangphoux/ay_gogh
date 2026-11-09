#set heading(level: 4)
= Tính năng trò chơi hoá

#figure(
  image("/out/docs/DA2_bao_cao/300_phan_tich_thiet_ke/use_case/Trò chơi.png", height: 25%),
  caption: [Sơ đồ Use Case Trò chơi],
)


#figure(
  table(
    columns: 2,
    align: (left, left),
    [Use Case], [Chỉnh thông số thuật toán],
    [Tác nhân chính], [User],
    [Mô tả ngắn gọn], [Điều chỉnh Desired Retention và tối ưu các tham số.],
    [Điều kiện tiên quyết], [Đã đăng nhập và có quyền chỉnh thông số.],
    [Sự kiện kích hoạt], [Người dùng mở phần cài đặt thuật toán.],
    [Điều kiện thực hiện], [Giá trị tham số trong phạm vi cho phép.],
    [Luồng sự kiện chính],
    [
      + Mở cài đặt.
      + Chỉnh giá trị Desired Retention hoặc tham số khác.
      + Hệ thống kiểm tra hợp lệ.
      + Lưu và áp dụng cấu hình.
    ],
  ),
  caption: [Bảng mô tả Use Case Chỉnh thông số thuật toán],
)
