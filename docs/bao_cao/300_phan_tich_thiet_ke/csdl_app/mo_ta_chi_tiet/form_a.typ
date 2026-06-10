#set heading(level: 5)

#pagebreak()
= Bảng Form A

#let thanh_phan = (
  (thuoc_tinh: "number", kieu_du_lieu: "INTEGER", rang_buoc: "PRIMARY KEY", dien_giai: "Số thứ tự câu hỏi"),
  (thuoc_tinh: "lemma", kieu_du_lieu: "TEXT", rang_buoc: "", dien_giai: "Từ mục tiêu"),
  (thuoc_tinh: "question", kieu_du_lieu: "TEXT", rang_buoc: "", dien_giai: "Câu hỏi"),
  (thuoc_tinh: "1", kieu_du_lieu: "TEXT", rang_buoc: "", dien_giai: "Lựa chọn 1"),
  (thuoc_tinh: "2", kieu_du_lieu: "TEXT", rang_buoc: "", dien_giai: "Lựa chọn 2"),
  (thuoc_tinh: "3", kieu_du_lieu: "TEXT", rang_buoc: "", dien_giai: "Lựa chọn 3"),
  (thuoc_tinh: "4", kieu_du_lieu: "TEXT", rang_buoc: "", dien_giai: "Lựa chọn 4"),
  (thuoc_tinh: "answer", kieu_du_lieu: "INTEGER", rang_buoc: "", dien_giai: "Đáp án đúng"),
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
  caption: [Bảng diễn giải cho Table Form A],
)
