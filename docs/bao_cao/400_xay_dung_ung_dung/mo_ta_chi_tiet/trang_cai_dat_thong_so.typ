#set heading(level: 3)

= Trang cài đặt các thông số
- *Giao diện*:

#figure(
  image("../images/settings.fsrs.png", height: 50%),
  caption: [Trang cài đặt các thông số],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Tiêu đề FSRS", kieu: "Heading", rang_buoc: "", y_nghia: "Nhận diện trang"),
  (ten: "Mô tả FSRS", kieu: "Paragraph", rang_buoc: "", y_nghia: "Giới thiệu thuật toán"),
  (ten: "Khối Desired Retention", kieu: "Section", rang_buoc: "", y_nghia: "Thiết lập tỉ lệ ghi nhớ"),
  (ten: "Input Desired Retention", kieu: "Input", rang_buoc: "", y_nghia: "Nhập giá trị 70-100"),
  (ten: "Nút Save", kieu: "Button", rang_buoc: "", y_nghia: "Lưu tỉ lệ ghi nhớ"),
  (ten: "Thông báo retention", kieu: "Notice", rang_buoc: "", y_nghia: "Phản hồi sau khi lưu"),
  (ten: "Khối Parameters", kieu: "Section", rang_buoc: "", y_nghia: "Giải thích tham số"),
  (ten: "Danh sách tham số", kieu: "Paragraph", rang_buoc: "", y_nghia: "Hiển thị tham số hiện tại"),
  (ten: "Nút Optimize", kieu: "Button", rang_buoc: "", y_nghia: "Tối ưu tham số"),
  (ten: "Thông báo tối ưu", kieu: "Notice", rang_buoc: "", y_nghia: "Trạng thái tối ưu hóa"),
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
  caption: [Thành phần của Trang cài đặt các thông số],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn Save", xu_li: "Gửi PATCH /settings/fsrs/save"),
  (bien_co: "Nhấn Optimize", xu_li: "Gửi GET /settings/fsrs/optimize"),
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
  caption: [Danh sách biến cố Trang cài đặt các thông số],
)
