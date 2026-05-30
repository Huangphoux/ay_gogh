#set heading(level: 5)


= Bảng NGSL

#let thanh_phan = (
  (thuoc_tinh: "number", kieu_du_lieu: "INTEGER", rang_buoc: "PRIMARY KEY", dien_giai: "Số thứ tự"),
  (thuoc_tinh: "lemma", kieu_du_lieu: "TEXT", rang_buoc: "UNIQUE", dien_giai: "Từ gốc"),
  (thuoc_tinh: "level", kieu_du_lieu: "INTEGER", rang_buoc: "", dien_giai: "Cấp độ NGSL"),
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
  caption: [Bảng diễn giải cho Table NGSL],
)
