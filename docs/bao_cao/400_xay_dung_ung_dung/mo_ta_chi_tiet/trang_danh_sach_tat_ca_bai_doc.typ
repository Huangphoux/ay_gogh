#set heading(level: 3)

= Trang danh sách tất cả các bài đọc
- *Giao diện*:

#figure(
  image("../images/read.index.all.png", height: 50%),
  caption: [Trang danh sách tất cả các bài đọc],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Trang danh sách tất cả các bài đọc", kieu: "", rang_buoc: "", y_nghia: ""),
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
  caption: [Thành phần của Trang danh sách tất cả các bài đọc],
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
  caption: [Danh sách biến cố Trang danh sách tất cả các bài đọc],
)
