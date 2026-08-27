#set heading(level: 3)

= Trang tiến độ học tập
- *Giao diện*:

#figure(
  image("../images/profile.png", height: 37%),
  caption: [Trang tiến độ học tập],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Tiêu đề Profile", kieu: "Heading", rang_buoc: "", y_nghia: "Hiển thị tên người dùng"),
  (ten: "Khối Test", kieu: "Section", rang_buoc: "", y_nghia: "Trạng thái kiểm tra"),
  (ten: "Liên kết Test", kieu: "Link", rang_buoc: "", y_nghia: "Đi đến trang kiểm tra"),
  (ten: "Thông báo Test", kieu: "Notice", rang_buoc: "", y_nghia: "Nhắc làm bài kiểm tra"),
  (ten: "Khối Read", kieu: "Section", rang_buoc: "", y_nghia: "Tiến độ đọc"),
  (ten: "Liên kết Read", kieu: "Link", rang_buoc: "", y_nghia: "Đi đến danh sách đọc"),
  (ten: "Tiến độ chương", kieu: "Paragraph", rang_buoc: "", y_nghia: "Số chương đã hoàn thành"),
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
  caption: [Thành phần của Trang tiến độ học tập],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn Test", xu_li: "Đi đến /test/"),
  (bien_co: "Nhấn Read", xu_li: "Đi đến /read/ hoặc /read/?p=n"),
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
  caption: [Danh sách biến cố Trang tiến độ học tập],
)
