

#let dict = (
  (id: 1, name: "Trang chủ", note: "Giới thiệu trang web, các tính năng chính"),
  (id: 2, name: "Trang Đăng nhập", note: "Xác thực người dùng"),
  (id: 3, name: "Trang Đăng kí", note: "Tạo tài khoản mới"),
  (id: 4, name: "Trang tiến độ học tập", note: "Hiển thị kết quả kiểm tra, tiến độ hoàn thành sách"),
  (id: 5, name: "Trang kết quả kiểm tra", note: "Xem kết quả và thống kê kiểm tra"),
  (id: 6, name: "Trang hướng dẫn kiểm tra", note: "Giới thiệu và hướng dẫn cách thực hiện bài kiểm tra"),
  (id: 7, name: "Trang tiến độ kiểm tra", note: "Hiện từng câu hỏi của bài kiểm tra"),
  (id: 8, name: "Trang cài đặt", note: "Quản lí các cài đặt của hệ thống"),
  (id: 9, name: "Trang cài đặt các thông số", note: "Điều chỉnh tham số desired retention, tối ưu thông số thuật toán"),
  (id: 10, name: "Trang danh sách 10 bài đọc đầu tiên", note: "Hiển thị 10 bài đọc đầu tiên cho người dùng"),
  (id: 11, name: "Trang danh sách tất cả các bài đọc", note: "Liệt kê toàn bộ bài đọc"),
  (id: 12, name: "Trang bài đọc", note: "Hiển thị nội dung bài đọc, nút hiện popup, nút đánh dấu hoàn thành"),
  (id: 13, name: "Trang đánh giá độ khó bài đọc", note: "Trang phân tích mức độ khó của bài đọc"),
  (id: 14, name: "Popup tìm kiếm từ điển cá nhân", note: "Tìm kiếm từ trong từ điển cá nhân của người dùng"),
  (id: 15, name: "Popup tìm kiếm từ điển trực tuyến", note: "Tìm kiếm từ trên từ điển trực tuyến"),
  (
    id: 16,
    name: "Popup thông báo ngày mai mới có thể học từ",
    note: "Nhắc người dùng từ này ngày mai mới có thể được học",
  ),
  (id: 17, name: "Popup trả lời nhớ hay không", note: "Người dùng trả lời nhớ hay không nhớ nghĩa của từ"),
  (id: 18, name: "Popup các thao tác khác", note: "Cung cấp thao tác hoãn từ và xoá từ"),
  (id: 19, name: "Popup hiển thị từ bị hoãn", note: "Cho biết từ này đã bị hoãn"),
  (id: 20, name: "Popup thông báo từ chưa cần được ôn", note: "Thông báo từ chưa đến thời gian ôn tập"),
)

#figure(
  table(
    table.header([*STT*], [*Tên màn hình*], [*Diễn giải*]),
    align: (center, left, left),
    columns: 3,
    ..for item in dict {
      ([#item.id], [#item.name], [#item.note])
    },
  ),
  caption: [Danh sách các màn hình],
)
