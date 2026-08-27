#set heading(level: 5)


= Bảng Chapter

#let thanh_phan = (
  (thuoc_tinh: "number", kieu_du_lieu: "INTEGER", rang_buoc: "PRIMARY KEY", dien_giai: "Số chương"),
  (thuoc_tinh: "number_word", kieu_du_lieu: "TEXT", rang_buoc: "", dien_giai: "Số chương dạng chữ"),
  (thuoc_tinh: "cardinal", kieu_du_lieu: "TEXT", rang_buoc: "", dien_giai: "Số thứ tự"),
  (thuoc_tinh: "cardinal_word", kieu_du_lieu: "TEXT", rang_buoc: "", dien_giai: "Số thứ tự dạng chữ"),
  (thuoc_tinh: "title", kieu_du_lieu: "TEXT", rang_buoc: "", dien_giai: "Tiêu đề chương"),
  (thuoc_tinh: "content", kieu_du_lieu: "TEXT", rang_buoc: "", dien_giai: "Nội dung chương"),
  (thuoc_tinh: "ngsl", kieu_du_lieu: "REAL", rang_buoc: "", dien_giai: "Tỉ lệ bao phủ NGSL"),
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
  caption: [Bảng diễn giải cho Table Chapter],
)
