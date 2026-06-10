#set heading(level: 4)
= Thu thập từ vựng
#figure(
  image("/out/docs/bao_cao/300_phan_tich_thiet_ke/use_case/Thu thập từ vựng.png", height: 70%),
  caption: [Sơ đồ Use Case Thu thập từ vựng],
)


#figure(
  table(
    columns: 2,
    align: (left, left),
    [Use Case], [Thu thập từ vựng],
    [Tác nhân chính], [User],
    [Mô tả ngắn gọn], [Tra cứu, lưu, đánh giá và quản lý ôn tập từ vựng.],
    [Điều kiện tiên quyết], [Đã đăng nhập và có từ điển cá nhân.],
    [Sự kiện kích hoạt], [Người dùng mở chức năng từ vựng hoặc tra cứu từ.],
    [Điều kiện thực hiện], [Có kết nối mạng khi tra cứu trực tuyến.],
    [Luồng sự kiện chính],
    [
      + Nhập từ cần tra.
      + Hệ thống hiển thị nghĩa hoặc từ trong từ điển cá nhân.
      + Người dùng lưu, đánh giá nhớ/quên, hoãn hoặc bỏ hoãn.
      + Hệ thống cập nhật từ điển và lịch ôn tập.
    ],
  ),
  caption: [Bảng mô tả Use Case Thu thập từ vựng],
)
