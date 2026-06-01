#let thanh_phan =(
  (actor:"User", y_nghia:"Người dùng"),
)

#figure(
  table(
    table.header([*STT*], [*Actor*], [*Ý nghĩa*]),
    align: (center, left, left),
    columns: 3,
    ..for (i, item) in thanh_phan.enumerate() {
      (str(i + 1), [#item.actor], [#item.y_nghia])
    },
  ),
  caption: [Bảng mô tả các bảng dữ liệu của hệ thống],
)