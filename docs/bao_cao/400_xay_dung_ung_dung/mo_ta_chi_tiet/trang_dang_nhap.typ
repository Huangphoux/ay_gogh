#set heading(level: 3)

= Trang Đăng nhập
- *Giao diện*:

#figure(
  image("../images/auth.login.png", height: 50%),
  caption: [Trang Đăng nhập],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Trang Đăng nhập", kieu: "", rang_buoc: "", y_nghia: ""),
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
  caption: [Thành phần của Trang Đăng nhập],
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
  caption: [Danh sách biến cố Trang Đăng nhập],
)
