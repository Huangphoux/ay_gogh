#set heading(level: 4)
= Đọc sách
#figure(
  image("/out/docs/bao_cao/300_phan_tich_thiet_ke/use_case/Đọc sách.png"),
  caption: [Sơ đồ Use Case Đọc sách],
)



#figure(
  table(
    [*Use Case*: Đọc sách],
    [*Tác nhân chính*: User ],
    [*Mô tả ngắn gọn*: Truy cập bài đọc, xem độ khó, đánh dấu và tùy chọn hiển thị.],
    [*Điều kiện tiên quyết*: Có bài đọc và kết nối mạng.],
    [*Sự kiện kích hoạt*: Người dùng chọn một bài đọc.],
    [*Điều kiện thực hiện*: Bài đọc tồn tại; quyền truy cập hợp lệ.],
    [*Luồng sự kiện chính*: 1) Chọn bài đọc. 2) Hệ thống hiển thị nội dung và phân tích độ khó. 3) Người dùng đánh dấu hoàn thành hoặc hủy. 4) Bật/tắt đánh dấu từ và chú thích. 5) Hệ thống lưu trạng thái.],
  ),
  caption: [Bảng mô tả Use Case Đọc sách],
)
