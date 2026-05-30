#set heading(level: 3)

= Trang tiến độ kiểm tra
- *Giao diện*:

#figure(
  image("../images/test.progress.png", height: 50%),
  caption: [Trang tiến độ kiểm tra],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Tiêu đề câu hỏi", kieu: "Heading", rang_buoc: "", y_nghia: "Hiển thị số câu"),
  (ten: "Form trả lời", kieu: "Form", rang_buoc: "", y_nghia: "Gửi lựa chọn"),
  (ten: "Câu hỏi", kieu: "Paragraph", rang_buoc: "", y_nghia: "Nội dung câu hỏi"),
  (ten: "Từ khóa in đậm", kieu: "Strong", rang_buoc: "", y_nghia: "Từ cần trả lời"),
  (ten: "Danh sách lựa chọn", kieu: "Radio list", rang_buoc: "", y_nghia: "4 đáp án"),
  (ten: "Nút Next", kieu: "Button", rang_buoc: "", y_nghia: "Câu tiếp theo"),
)

#figure(
  table(
    table.header([*STT*], [*Tên*], [*Kiểu*], [*Ràng buộc*], [*Ý nghĩa*]),
    align: (center, left, left, left, left),
    columns: 5,
    ..for (i, item) in thanh_phan.enumerate() {
      (str(i + 1), [#item.ten], [#item.kieu], [#item.rang_buoc], [#item.y_nghia])
    },
  ),
  caption: [Thành phần của Trang tiến độ kiểm tra],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Chọn đáp án", xu_li: "Đánh dấu radio"),
  (bien_co: "Nhấn Next", xu_li: "Gửi POST /test/progress_process"),
)

#figure(
  table(
    table.header([*STT*], [*Biến cố*], [*Xử lí*]),
    align: (center, left, left),
    columns: 3,
    ..for (i, item) in bien_co.enumerate() {
      (str(i + 1), [#item.bien_co], [#item.xu_li])
    },
  ),
  caption: [Danh sách biến cố Trang tiến độ kiểm tra],
)
