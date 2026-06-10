#set heading(level: 3)

= Trang hướng dẫn kiểm tra
- *Giao diện*:

#figure(
  image("../images/test.intro.png", height: 48%),
  caption: [Trang hướng dẫn kiểm tra],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Tiêu đề Intro", kieu: "Heading", rang_buoc: "", y_nghia: "Nhận diện trang"),
  (ten: "Mô tả bài test", kieu: "Paragraph", rang_buoc: "", y_nghia: "Giới thiệu bài kiểm tra"),
  (ten: "Nút Start", kieu: "Button", rang_buoc: "", y_nghia: "Bắt đầu làm bài"),
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
  caption: [Thành phần của Trang hướng dẫn kiểm tra],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn Start", xu_li: "Đi đến /test/progress"),
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
  caption: [Danh sách biến cố Trang hướng dẫn kiểm tra],
)
