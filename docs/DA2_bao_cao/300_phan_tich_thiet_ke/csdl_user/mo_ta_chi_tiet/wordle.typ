#set heading(level: 5)


= Bảng Wordle

#let thanh_phan = (
  (thuoc_tinh: "number", kieu_du_lieu: "INTEGER", rang_buoc: "PRIMARY KEY", dien_giai: "Số lần đoán từ"),
  (thuoc_tinh: "guess", kieu_du_lieu: "TEXT", rang_buoc: "NOT NULL", dien_giai: "Nội dung từ đoán"),
  (thuoc_tinh: "is_submitted", kieu_du_lieu: "INTEGER", rang_buoc: "NOT NULL", dien_giai: "Trạng thái nộp của đáp án"),
)

#figure(
  table(
    table.header([*STT*], [*Thuộc tính*], [*Kiểu dữ liệu*], [*Ràng buộc*], [*Diễn giải*]),
    align: (center, left, left, left, left),
    columns: 5,
    ..for (i, item) in thanh_phan.enumerate() {
      (str(i + 1), [#item.thuoc_tinh], [#item.kieu_du_lieu], [#item.rang_buoc], [#item.dien_giai])
    },
  ),
  caption: [Bảng diễn giải cho Table Wordle],
)
