#set heading(level: 3)

#pagebreak()
= Popup thông báo từ chưa cần được ôn
- *Giao diện*:

#figure(
  image("../images/read.popup.not_due.png", height: 50%),
  caption: [Popup thông báo từ chưa cần được ôn],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Khung popup", kieu: "Details/Popover", rang_buoc: "", y_nghia: "Hiển thị popup thông báo"),
  (ten: "Tiêu đề Popup", kieu: "Summary", rang_buoc: "", y_nghia: "Hiển thị trạng thái"),
  (ten: "Thông báo thời gian", kieu: "Paragraph", rang_buoc: "", y_nghia: "Báo thời gian ôn tiếp"),
  (ten: "Nút Close", kieu: "Button", rang_buoc: "", y_nghia: "Đóng popup"),
  (ten: "Nút Review anyway", kieu: "Button", rang_buoc: "", y_nghia: "Bỏ qua chờ, vẫn ôn"),
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
  caption: [Thành phần của Popup thông báo từ chưa cần được ôn],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn Close", xu_li: "Đóng popup"),
  (bien_co: "Nhấn Review anyway", xu_li: "GET /read/{num}/open?bypass=1"),
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
  caption: [Danh sách biến cố Popup thông báo từ chưa cần được ôn],
)
