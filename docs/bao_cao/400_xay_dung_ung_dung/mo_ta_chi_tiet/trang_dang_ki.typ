#set heading(level: 3)

#pagebreak()
= Trang Đăng kí
- *Giao diện*:

#figure(
  image("../images/auth.signup.png", height: 40%),
  caption: [Trang Đăng kí],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Tiêu đề Sign Up", kieu: "Heading", rang_buoc: "", y_nghia: "Nhận diện màn hình"),
  (ten: "Form đăng kí", kieu: "Form", rang_buoc: "", y_nghia: "Gửi thông tin đăng kí"),
  (ten: "Username", kieu: "Input", rang_buoc: "", y_nghia: "Nhập tên đăng kí"),
  (ten: "Password", kieu: "Input", rang_buoc: "", y_nghia: "Nhập mật khẩu"),
  (ten: "Show Password", kieu: "Checkbox", rang_buoc: "", y_nghia: "Hiện/ẩn mật khẩu"),
  (ten: "Sign Up", kieu: "Button", rang_buoc: "", y_nghia: "Xác nhận đăng kí"),
  (ten: "Log In", kieu: "Link", rang_buoc: "", y_nghia: "Chuyển sang đăng nhập"),
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
  caption: [Thành phần của Trang Đăng kí],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Bấm vào Sign Up", xu_li: "Gửi POST /auth/signup"),
  (bien_co: "Bấm Show Password", xu_li: "Đổi kiểu input password/text"),
  (bien_co: "Bấm Log In", xu_li: "Đi đến /auth/login"),
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
  caption: [Danh sách biến cố Trang Đăng kí],
)
