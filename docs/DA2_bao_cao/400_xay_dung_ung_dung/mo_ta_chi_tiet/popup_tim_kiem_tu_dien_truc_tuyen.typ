#set heading(level: 3)

#pagebreak()
= Popup tìm kiếm từ điển trực tuyến
- *Giao diện*:

#figure(
  image("../images/read.popup.wiktionary.png", height: 50%),
  caption: [Popup tìm kiếm từ điển trực tuyến],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Khung popup", kieu: "Details/Popover", rang_buoc: "", y_nghia: "Hiển thị popup tra cứu"),
  (ten: "Tiêu đề Popup", kieu: "Summary", rang_buoc: "", y_nghia: "Hiển thị trạng thái"),
  (ten: "Tiêu đề Word", kieu: "Heading", rang_buoc: "", y_nghia: "Hiển thị từ đang tra"),
  (ten: "Label Definition", kieu: "Label", rang_buoc: "", y_nghia: "Nhãn định nghĩa"),
  (ten: "Textarea định nghĩa", kieu: "Textarea", rang_buoc: "", y_nghia: "Nhập/ghi định nghĩa"),
  (ten: "Khối Dictionary", kieu: "Details", rang_buoc: "", y_nghia: "Hiển thị kết quả tra cứu"),
  (ten: "Danh sách định nghĩa", kieu: "Section", rang_buoc: "", y_nghia: "Các nghĩa tìm được"),
  (ten: "Nút Close", kieu: "Button", rang_buoc: "", y_nghia: "Đóng popup"),
  (ten: "Nút Save", kieu: "Button", rang_buoc: "", y_nghia: "Lưu từ vào bộ nhớ"),
  (ten: "Nhãn NGSL", kieu: "Badge", rang_buoc: "", y_nghia: "Thông tin level NGSL"),
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
  caption: [Thành phần của Popup tìm kiếm từ điển trực tuyến],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn Save", xu_li: "POST /read/{num}/save"),
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
  caption: [Danh sách biến cố Popup tìm kiếm từ điển trực tuyến],
)
