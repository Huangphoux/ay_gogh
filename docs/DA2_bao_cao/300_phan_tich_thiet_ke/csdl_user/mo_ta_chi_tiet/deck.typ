#set heading(level: 5)


= Bảng Deck

#let thanh_phan = (
  (thuoc_tinh: "id", kieu_du_lieu: "INTEGER", rang_buoc: "PRIMARY KEY", dien_giai: "Khóa chính"),
  (thuoc_tinh: "front", kieu_du_lieu: "TEXT", rang_buoc: "NOT NULL, UNIQUE", dien_giai: "Mặt trước thẻ"),
  (thuoc_tinh: "back", kieu_du_lieu: "TEXT", rang_buoc: "NOT NULL", dien_giai: "Mặt sau thẻ"),
  (thuoc_tinh: "state", kieu_du_lieu: "INTEGER", rang_buoc: "NOT NULL", dien_giai: "Trạng thái thẻ"),
  (thuoc_tinh: "step", kieu_du_lieu: "INTEGER", rang_buoc: "NOT NULL", dien_giai: "Bước lặp lại"),
  (thuoc_tinh: "stability", kieu_du_lieu: "REAL", rang_buoc: "", dien_giai: "Độ ổn định"),
  (thuoc_tinh: "difficulty", kieu_du_lieu: "REAL", rang_buoc: "", dien_giai: "Độ khó"),
  (thuoc_tinh: "due", kieu_du_lieu: "TEXT", rang_buoc: "NOT NULL", dien_giai: "Hạn ôn tập"),
  (thuoc_tinh: "last_review", kieu_du_lieu: "TEXT", rang_buoc: "", dien_giai: "Lần ôn tập cuối"),
  (
    thuoc_tinh: "is_retired",
    kieu_du_lieu: "INTEGER",
    rang_buoc: "NOT NULL, CHECK (is_retired = 1 OR is_retired = 0)",
    dien_giai: "Đánh dấu nghỉ hưu",
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
  caption: [Bảng diễn giải cho Table Deck],
)
