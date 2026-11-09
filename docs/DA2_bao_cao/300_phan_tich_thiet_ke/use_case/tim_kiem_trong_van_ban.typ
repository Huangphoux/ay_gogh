#set heading(level: 4)
= Tìm kiếm trong văn bản

#figure(
  image("/out/docs/DA2_bao_cao/300_phan_tich_thiet_ke/use_case/Tìm kiếm trong văn bản.png", height: 25%),
  caption: [Sơ đồ Use Case Tìm kiếm trong văn bản],
)


#figure(
  table(
    columns: 2,
    align: (left, left),
    [Use Case], [Tìm kiếm trong văn bản],
    [Tác nhân chính], [User],
    [Mô tả ngắn gọn], [Tìm các từ mà người dùng chưa nắm vững để thu thập vào từ điển của bản thân.],
    [Điều kiện tiên quyết], [Đã đăng nhập. Truy cập vào mục Đọc sách.],
    [Sự kiện kích hoạt], [Người dùng gõ từ cần tìm vào ô tìm kiếm.],
    [Điều kiện thực hiện], [Có kết nối mạng khi truy cập.],
    [Luồng sự kiện chính],
    [
      + Hiện kết quả tìm kiếm từ.
      + Người dùng có thể bấm vào liên kết đến chương chứa từ.
    ],
  ),
  caption: [Bảng mô tả Use Case Tìm kiếm trong văn bản],
)
