#set heading(level: 3)

#pagebreak()
= Popup các thao tác khác
- *Giao diện*:

#figure(
  image("../images/read.popup.due.more.png", height: 50%),
  caption: [Popup các thao tác khác],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Khung popup", kieu: "Details/Popover", rang_buoc: "", y_nghia: "Hiển thị popup thao tác"),
  (ten: "Tiêu đề Popup", kieu: "Summary", rang_buoc: "", y_nghia: "Hiển thị trạng thái"),
  (ten: "Tiêu đề Word", kieu: "Heading", rang_buoc: "", y_nghia: "Hiển thị từ đang ôn"),
  (ten: "Khối More actions", kieu: "Details", rang_buoc: "", y_nghia: "Các thao tác khác"),
  (ten: "Nút Retire", kieu: "Button", rang_buoc: "", y_nghia: "Đánh dấu từ đã hoãn"),
  (ten: "Nút Delete", kieu: "Button", rang_buoc: "", y_nghia: "Xóa từ khỏi bộ nhớ"),
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
  caption: [Thành phần của Popup các thao tác khác],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn Retire", xu_li: "PATCH /read/{num}/retire"),
  (bien_co: "Nhấn Delete", xu_li: "DELETE /read/{num}/delete (có xác nhận)"),
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
  caption: [Danh sách biến cố Popup các thao tác khác],
)
