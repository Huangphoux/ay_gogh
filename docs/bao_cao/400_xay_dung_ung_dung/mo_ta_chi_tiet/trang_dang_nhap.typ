#set heading(level: 3)

= Trang Đăng nhập
- *Giao diện*:

#figure(
  image("../images/auth.login.png", height: 50%),
  caption: [Trang Đăng nhập],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Tiêu đề Log In", kieu: "Heading", rang_buoc: "", y_nghia: "Nhận diện màn hình"),
  (ten: "Form đăng nhập", kieu: "Form", rang_buoc: "", y_nghia: "Gửi thông tin đăng nhập"),
  (ten: "Username", kieu: "Input", rang_buoc: "", y_nghia: "Nhập tên đăng nhập"),
  (ten: "Password", kieu: "Input", rang_buoc: "", y_nghia: "Nhập mật khẩu"),
  (ten: "Show Password", kieu: "Checkbox", rang_buoc: "", y_nghia: "Hiện/ẩn mật khẩu"),
  (ten: "Log In", kieu: "Button", rang_buoc: "", y_nghia: "Xác nhận đăng nhập"),
  (ten: "Sign Up", kieu: "Link", rang_buoc: "", y_nghia: "Chuyển sang đăng kí"),
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
  (bien_co: "Bấm vào Log In", xu_li: "Gửi POST /auth/login"),
  (bien_co: "Bấm Show Password", xu_li: "Đổi kiểu input password/text"),
  (bien_co: "Bấm Sign Up", xu_li: "Đi đến /auth/signup"),
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
