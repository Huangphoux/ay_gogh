#set heading(level: 4)

= Quản lí tài khoản
#figure(
  image("/out/docs/bao_cao/300_phan_tich_thiet_ke/use_case/Quản lý tài khoản.png"),
  caption: [Sơ đồ Use Case Quản lí tài khoản],
)


#figure(
  table(
    columns: 2,
    align: (left, left),
    [Use Case], [Quản lí tài khoản],
    [Tác nhân chính], [User],
    [Mô tả ngắn gọn], [Cho phép đăng ký, đăng nhập, đăng xuất tài khoản.],
    [Điều kiện tiên quyết], [Có thiết bị và kết nối mạng.],
    [Sự kiện kích hoạt], [Người dùng chọn Đăng ký/Đăng nhập/Đăng xuất.],
    [Điều kiện thực hiện], [Thông tin hợp lệ; để đăng xuất thì đang đăng nhập.],
    [Luồng sự kiện chính],
    [
      + Chọn thao tác.
      + Nhập thông tin.
      + Hệ thống xác thực hoặc tạo tài khoản.
      + Cập nhật trạng thái và thông báo kết quả.
    ],
  ),
  caption: [Bảng mô tả Use Case Quản lí tài khoản],
)
