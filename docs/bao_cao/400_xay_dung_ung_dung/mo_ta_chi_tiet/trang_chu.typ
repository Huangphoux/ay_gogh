#set heading(level: 3)

= Trang chủ
- *Giao diện*:

#figure(
  image("../images/index.png", height: 50%),
  caption: [Trang chủ],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Home", kieu: "Liên kết", rang_buoc: "", y_nghia: "Liên kết chuyển hướng đến trang chủ"),
  (ten: "Log In", kieu: "Liên kết", rang_buoc: "", y_nghia: "Liên kết chuyển hướng đến trang đăng nhập"),
  (ten: "Sign Up", kieu: "Liên kết", rang_buoc: "", y_nghia: "Liên kết chuyển hướng đến trang đăng kí"),
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
  caption: [Thành phần của Trang chủ],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn Home", xu_li: "Chuyển hướng đến trang chủ"),
  (bien_co: "Nhấn Log In", xu_li: "Chuyển hướng đến trang đăng nhập"),
  (bien_co: "Nhấn Sign Up", xu_li: "Chuyển hướng đến trang đăng kí"),
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
  caption: [Danh sách biến cố Trang chủ],
)
