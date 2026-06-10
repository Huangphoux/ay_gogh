#set heading(level: 3)

#pagebreak()
= Popup hiển thị từ bị hoãn
- *Giao diện*:

#figure(
  image("../images/read.popup.retired.png", height: 50%),
  caption: [Popup hiển thị từ bị hoãn],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Khung popup", kieu: "Details/Popover", rang_buoc: "", y_nghia: "Hiển thị popup từ bị hoãn"),
  (ten: "Tiêu đề Popup", kieu: "Summary", rang_buoc: "", y_nghia: "Hiển thị trạng thái"),
  (ten: "Tiêu đề Word", kieu: "Heading", rang_buoc: "", y_nghia: "Hiển thị từ"),
  (ten: "Label Definition", kieu: "Label", rang_buoc: "", y_nghia: "Nhãn định nghĩa"),
  (ten: "Textarea định nghĩa", kieu: "Textarea", rang_buoc: "", y_nghia: "Chỉnh sửa định nghĩa"),
  (ten: "Nút Close & Save", kieu: "Button", rang_buoc: "", y_nghia: "Lưu và đóng"),
  (ten: "Nút Unretire", kieu: "Button", rang_buoc: "", y_nghia: "Bỏ hoãn từ"),
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
  caption: [Thành phần của Popup hiển thị từ bị hoãn],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn Close & Save", xu_li: "PATCH /read/{num}/close"),
  (bien_co: "Nhấn Unretire", xu_li: "DELETE /read/{num}/retire"),
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
  caption: [Danh sách biến cố Popup hiển thị từ bị hoãn],
)
