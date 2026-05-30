#set heading(level: 3)

= Popup thông báo từ chưa cần được ôn
- *Giao diện*:

#figure(
  image("../images/read.popup.not_due.png", height: 50%),
  caption: [Popup thông báo từ chưa cần được ôn],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Popup thông báo từ chưa cần được ôn", kieu: "", rang_buoc: "", y_nghia: ""),
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
  caption: [Danh sách biến cố Popup thông báo từ chưa cần được ôn],
)
