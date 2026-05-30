#set heading(level: 5)


= Bảng User

#let thanh_phan = (
  (thuoc_tinh: "id", kieu_du_lieu: "INTEGER", rang_buoc: "PRIMARY KEY", dien_giai: "Khóa chính"),
  (thuoc_tinh: "name", kieu_du_lieu: "TEXT", rang_buoc: "NOT NULL, UNIQUE", dien_giai: "Tên đăng nhập"),
  (thuoc_tinh: "pwd", kieu_du_lieu: "TEXT", rang_buoc: "NOT NULL", dien_giai: "Mật khẩu đã băm"),
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
  caption: [Bảng diễn giải cho Table User],
)
