#set heading(level: 3)

= Trang chủ
- *Giao diện*:

Do kích cỡ hình ảnh quá khổ, kính mời bạn đọc xem thiết kế của #link("https://raw.githubusercontent.com/Huangphoux/ay_gogh/refs/heads/main/docs/bao_cao/400_xay_dung_ung_dung/images/index.png")[Trang chủ].

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Header", kieu: "Khu vực", rang_buoc: "", y_nghia: "Chứa điều hướng và tiêu đề"),
  (ten: "Nav (chưa đăng nhập)", kieu: "Liên kết", rang_buoc: "", y_nghia: "Điều hướng cơ bản"),
  (ten: "Tiêu đề Ay Gogh!", kieu: "Heading", rang_buoc: "", y_nghia: "Nhận diện thương hiệu"),
  (ten: "Hero: Just Read", kieu: "Section", rang_buoc: "", y_nghia: "Thông điệp chính"),
  (ten: "Nút Sign up", kieu: "Button/Link", rang_buoc: "", y_nghia: "Đi đến đăng kí"),
  (ten: "Video giới thiệu", kieu: "Video", rang_buoc: "", y_nghia: "Nội dung demo"),
  (ten: "Giới thiệu Ay Gogh!", kieu: "Paragraph", rang_buoc: "", y_nghia: "Mô tả nền tảng"),
  (ten: "NGSL/FSRS/Nature Method", kieu: "Section", rang_buoc: "", y_nghia: "Giới thiệu công nghệ"),
  (ten: "Testimonials", kieu: "Blockquote", rang_buoc: "", y_nghia: "Đánh giá người dùng"),
  (ten: "Last chance CTA", kieu: "Section", rang_buoc: "", y_nghia: "Kêu gọi đăng kí"),
  (ten: "Profile heading", kieu: "Heading", rang_buoc: "", y_nghia: "Tên người dùng"),
  (ten: "Khối Test", kieu: "Section", rang_buoc: "", y_nghia: "Trạng thái kiểm tra"),
  (ten: "Khối Read", kieu: "Section", rang_buoc: "", y_nghia: "Tiến độ đọc"),
  (ten: "Footer", kieu: "Khu vực", rang_buoc: "", y_nghia: "Thông tin bản quyền và liên kết"),
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
  (bien_co: "Nhấn Home", xu_li: "Đi đến /"),
  (bien_co: "Nhấn Log In", xu_li: "Đi đến /auth/login/"),
  (bien_co: "Nhấn Sign Up", xu_li: "Đi đến /auth/signup"),
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
