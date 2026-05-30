#set heading(level: 3)

= Popup các thao tác khác
- *Giao diện*:

#figure(
  image("../images/read.popup.due.more.png", height: 50%),
  caption: [Popup các thao tác khác],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Popup các thao tác khác", kieu: "", rang_buoc: "", y_nghia: ""),
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
  (bien_co: "", xu_li: ""),
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
