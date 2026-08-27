
#figure(
  table(
    table.header([*STT*], [*Use Case chính*], [*Phân rã*], [*Ý nghĩa*]),
    align: (center, left, left, left),
    columns: 4,
    [1], table.cell(rowspan: 3)[Quản lí tài khoản], [Đăng ký], [Tạo tài khoản mới],
    [2], [Đăng nhập], [Truy cập hệ thống bằng tài khoản],
    [3], [Đăng xuất], [Kết thúc phiên đăng nhập],

    [4], table.cell(rowspan: 2)[Kiểm tra vốn từ vựng], [Làm bài kiểm tra mới], [Bắt đầu một bài kiểm tra mới],
    [5], [Tiếp tục bài kiểm tra chưa hoàn thành], [Tiếp tục bài kiểm tra chưa hoàn thành],

    [6], table.cell(rowspan: 6)[Đọc sách], [Truy cập bài đọc], [Mở nội dung bài đọc],
    [7], [Xem phân tích độ khó bài đọc], [Xem đánh giá độ khó bài đọc],
    [8], [Đánh dấu hoàn thành bài đọc], [Ghi nhận đã đọc xong],
    [9], [Huỷ đánh dấu hoàn thành bài đọc], [Bỏ trạng thái đã hoàn thành],
    [10], [Hiện/ẩn đánh dấu các từ trong từ điển cá nhân], [Bật hoặc tắt tô dấu từ cá nhân],
    [11], [Hiện/ẩn các chú thích trong bài đọc], [Bật hoặc tắt chú thích],

    [12], table.cell(rowspan: 11)[Thu thập từ vựng], [Tìm từ trong từ điển cá nhân], [Tra cứu từ đã lưu],
    [13], [Tìm nghĩa của từ trong từ điển trực tuyến], [Tra nghĩa từ trực tuyến],
    [14], [Tìm từ khác trong khi đang hiển thị nghĩa của một từ], [Tra cứu từ khác mà vẫn ở màn hình nghĩa],
    [15], [Lưu từ vào từ điển cá nhân], [Thêm từ mới vào danh sách cá nhân],
    [16], [Bỏ qua ràng buộc thời gian và ôn từ vựng], [Ôn từ ngay, bỏ giới hạn thời gian],
    [17], [Đánh giá nhớ từ vựng], [Ghi nhận mức độ nhớ],
    [18], [Đánh giá quên từ vựng], [Ghi nhận mức độ quên],
    [19], [Hoãn việc ôn tập từ vựng], [Lùi lịch ôn tập],
    [20], [Bỏ hoãn việc ôn tập từ vựng], [Khôi phục lịch ôn tập],
    [21], [Xoá từ vựng khỏi từ điển cá nhân], [Xóa từ khỏi danh sách cá nhân],
    [22], [Ẩn ô tìm kiếm], [Ẩn khung tìm kiếm],

    [23],
    table.cell(rowspan: 2)[Chỉnh thông số thuật toán],
    [Chỉnh thông số Desired Retention],
    [Điều chỉnh tỉ lệ ghi nhớ mong muốn],
    [24], [Tối ưu các thông số thuật toán], [Tinh chỉnh tham số để tối ưu hiệu quả],
  ),
  caption: [Bảng danh sách use case],
)
