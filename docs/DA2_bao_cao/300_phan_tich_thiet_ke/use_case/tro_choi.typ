#set heading(level: 4)
= Trò chơi

#figure(
  image("/out/docs/DA2_bao_cao/300_phan_tich_thiet_ke/use_case/Trò chơi.png", height: 25%),
  caption: [Sơ đồ Use Case Trò chơi],
)


#figure(
  table(
    columns: 2,
    align: (left, left),
    [Use Case], [Trò chơi],
    [Tác nhân chính], [User],
    [Mô tả ngắn gọn], [Trò chơi đoán các từ trong danh sách NGSL.],
    [Điều kiện tiên quyết], [Đã đăng nhập.],
    [Sự kiện kích hoạt], [Người dùng bấm vào mục Trò chơi.],
    [Điều kiện thực hiện], [Có kết nối mạng khi truy cập.],
    [Luồng sự kiện chính],
    [
      + Hiện trò chơi.
      + Người dùng thử đoán từ qua 6 lần.
      + Nếu qua 6 lần người dùng đoán không được, cho người dùng biết đáp án từ cần đoán.
      + Hiện nút để người dùng đoán từ khác.
    ],
  ),
  caption: [Bảng mô tả Use Case Trò chơi],
)
