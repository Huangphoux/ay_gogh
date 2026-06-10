#set heading(level: 3)

#pagebreak()
= Popup trả lời nhớ hay không
- *Giao diện*:

#figure(
  image("../images/read.popup.due.rate.png", height: 50%),
  caption: [Popup trả lời nhớ hay không],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Khung popup", kieu: "Details/Popover", rang_buoc: "", y_nghia: "Hiển thị popup ôn tập"),
  (ten: "Tiêu đề Popup", kieu: "Summary", rang_buoc: "", y_nghia: "Hiển thị trạng thái"),
  (ten: "Tiêu đề Word", kieu: "Heading", rang_buoc: "", y_nghia: "Hiển thị từ đang ôn"),
  (ten: "Khối Recall before reveal", kieu: "Details", rang_buoc: "", y_nghia: "Khu vực trả lời nhớ/không"),
  (ten: "Label Definition", kieu: "Label", rang_buoc: "", y_nghia: "Nhãn định nghĩa"),
  (ten: "Textarea định nghĩa", kieu: "Textarea", rang_buoc: "", y_nghia: "Nhập/ghi định nghĩa"),
  (ten: "Nút I forgot", kieu: "Button", rang_buoc: "", y_nghia: "Đánh giá quên"),
  (ten: "Nút I remembered", kieu: "Button", rang_buoc: "", y_nghia: "Đánh giá nhớ"),
  (ten: "Nút Close", kieu: "Button", rang_buoc: "", y_nghia: "Đóng popup"),
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
  caption: [Thành phần của Popup trả lời nhớ hay không],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn I forgot", xu_li: "PATCH /read/{num}/forgot"),
  (bien_co: "Nhấn I remembered", xu_li: "PATCH /read/{num}/remembered"),
  (bien_co: "Nhấn Close", xu_li: "Đóng popup"),
  (bien_co: "Nhấn Esc", xu_li: "GET /read/{num}/close và ẩn popup"),
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
  caption: [Danh sách biến cố Popup trả lời nhớ hay không],
)
