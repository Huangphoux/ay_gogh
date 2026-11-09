#set heading(level: 5)


= Bảng Medal

#let thanh_phan = (
  (thuoc_tinh: "id", kieu_du_lieu: "INTEGER", rang_buoc: "PRIMARY KEY", dien_giai: "Khóa chính"),
  (thuoc_tinh: "name", kieu_du_lieu: "TEXT", rang_buoc: "UNIQUE, NOT NULL", dien_giai: "Tên huy hiệu"),
  (thuoc_tinh: "description", kieu_du_lieu: "TEXT", rang_buoc: "NOT NULL", dien_giai: "Mô tả huy hiệu"),
  (thuoc_tinh: "icon", kieu_du_lieu: "TEXT", rang_buoc: "NOT NULL", dien_giai: "Biểu tượng emoji cho huy hiệu"),
  (thuoc_tinh: "requirement", kieu_du_lieu: "INTEGER", rang_buoc: "NOT NULL", dien_giai: "Ngưỡng yêu cầu của huy hiệu"),
  (
    thuoc_tinh: "is_fulfilled",
    kieu_du_lieu: "INTEGER",
    rang_buoc: "NOT NULL",
    dien_giai: "Trạng thái đạt được của huy hiệu",
  ),
  (
    thuoc_tinh: "table_name",
    kieu_du_lieu: "TEXT",
    rang_buoc: "NOT NULL",
    dien_giai: "Tên bảng để kiểm tra yêu cầu của huy hiệu",
  ),
  (
    thuoc_tinh: "column_name",
    kieu_du_lieu: "TEXT",
    rang_buoc: "NOT NULL",
    dien_giai: "Tên cột trong bảng để kiểm tra yêu cầu của huy hiệu",
  ),
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
  caption: [Bảng diễn giải cho Table Medal],
)
