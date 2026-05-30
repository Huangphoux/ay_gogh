#set heading(level: 5)


= Bảng Test

#let thanh_phan = (
  (thuoc_tinh: "number", kieu_du_lieu: "INTEGER", rang_buoc: "PRIMARY KEY", dien_giai: "Khóa chính"),
  (thuoc_tinh: "day", kieu_du_lieu: "TEXT", rang_buoc: "NOT NULL", dien_giai: "Ngày kiểm tra"),
  (thuoc_tinh: "form", kieu_du_lieu: "TEXT", rang_buoc: "NOT NULL", dien_giai: "Form kiểm tra"),
  (thuoc_tinh: "progress", kieu_du_lieu: "INTEGER", rang_buoc: "NOT NULL", dien_giai: "Tiến độ làm bài"),
  (thuoc_tinh: "lv1", kieu_du_lieu: "INTEGER", rang_buoc: "NOT NULL", dien_giai: "Số câu đúng cấp 1"),
  (thuoc_tinh: "lv2", kieu_du_lieu: "INTEGER", rang_buoc: "NOT NULL", dien_giai: "Số câu đúng cấp 2"),
  (thuoc_tinh: "lv3", kieu_du_lieu: "INTEGER", rang_buoc: "NOT NULL", dien_giai: "Số câu đúng cấp 3"),
  (thuoc_tinh: "lv4", kieu_du_lieu: "INTEGER", rang_buoc: "NOT NULL", dien_giai: "Số câu đúng cấp 4"),
  (thuoc_tinh: "lv5", kieu_du_lieu: "INTEGER", rang_buoc: "NOT NULL", dien_giai: "Số câu đúng cấp 5"),
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
  caption: [Bảng diễn giải cho Table Test],
)
