#set heading(level: 4)
= Kiểm tra vốn từ vựng
#figure(
  image("/out/docs/bao_cao/300_phan_tich_thiet_ke/use_case/Kiểm tra vốn từ vựng.png"),
  caption: [Sơ đồ Use Case Kiểm tra vốn từ vựng],
)


#figure(
  table(
    columns: 2,
    align: (left, left),
    [Use Case], [Kiểm tra vốn từ vựng],
    [Tác nhân chính], [User],
    [Mô tả ngắn gọn], [Thực hiện bài kiểm tra mới hoặc tiếp tục bài đang dở.],
    [Điều kiện tiên quyết], [Đã đăng nhập và có kết nối mạng.],
    [Sự kiện kích hoạt], [Người dùng chọn mục Kiểm tra vốn từ vựng.],
    [Điều kiện thực hiện], [Có bộ câu hỏi hoặc bài kiểm tra chưa hoàn thành.],
    [Luồng sự kiện chính],
    [
      + Chọn làm mới hoặc tiếp tục.
      + Hệ thống tải câu hỏi.
      + Người dùng trả lời.
      + Hệ thống chấm điểm hoặc lưu tiến trình.
      + Hiển thị kết quả.
    ],
  ),
  caption: [Bảng mô tả Use Case Kiểm tra vốn từ vựng],
)
