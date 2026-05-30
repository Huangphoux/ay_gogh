#set heading(level: 3)

= Trang cài đặt
- *Giao diện*:

#figure(
  image("../images/settings.png", height: 50%),
  caption: [Trang cài đặt],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Tiêu đề Settings", kieu: "Heading", rang_buoc: "", y_nghia: "Nhận diện trang"),
  (ten: "Liên kết FSRS", kieu: "Link", rang_buoc: "", y_nghia: "Đi đến trang cài đặt FSRS"),
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
  caption: [Thành phần của Trang cài đặt],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn FSRS", xu_li: "Đi đến /settings/fsrs"),
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
  caption: [Danh sách biến cố Trang cài đặt],
)
