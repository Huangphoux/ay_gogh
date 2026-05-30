#set heading(level: 3)

= Popup tìm kiếm từ điển cá nhân
- *Giao diện*:

#figure(
  image("../images/read.popup.search.png", height: 50%),
  caption: [Popup tìm kiếm từ điển cá nhân],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Khung popup", kieu: "Details/Popover", rang_buoc: "", y_nghia: "Hiển thị popup tra cứu"),
  (ten: "Tiêu đề Popup", kieu: "Summary", rang_buoc: "", y_nghia: "Trạng thái Searching"),
  (ten: "Thông báo Searching", kieu: "Paragraph", rang_buoc: "", y_nghia: "Báo trạng thái tìm kiếm"),
  (ten: "Label nhập từ", kieu: "Label", rang_buoc: "", y_nghia: "Hướng dẫn nhập từ"),
  (ten: "Ô nhập từ", kieu: "Input", rang_buoc: "", y_nghia: "Nhập từ cần tra"),
  (ten: "Nút Close", kieu: "Button", rang_buoc: "", y_nghia: "Đóng popup"),
  (ten: "Nút Search", kieu: "Button", rang_buoc: "", y_nghia: "Bắt đầu tra cứu"),
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
  caption: [Thành phần của Popup tìm kiếm từ điển cá nhân],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn Search", xu_li: "GET /read/{num}/open"),
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
  caption: [Danh sách biến cố Popup tìm kiếm từ điển cá nhân],
)
