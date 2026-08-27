#set heading(level: 5)


= Bảng Review Log

#let thanh_phan = (
  (thuoc_tinh: "id", kieu_du_lieu: "INTEGER", rang_buoc: "PRIMARY KEY", dien_giai: "Khóa chính"),
  (
    thuoc_tinh: "card_id",
    kieu_du_lieu: "INTEGER",
    rang_buoc: "NOT NULL, REFERENCES deck(id) ON DELETE CASCADE",
    dien_giai: "Tham chiếu thẻ",
  ),
  (thuoc_tinh: "rating", kieu_du_lieu: "INTEGER", rang_buoc: "NOT NULL", dien_giai: "Mức đánh giá"),
  (thuoc_tinh: "review_datetime", kieu_du_lieu: "TEXT", rang_buoc: "NOT NULL", dien_giai: "Thời điểm ôn tập"),
  (thuoc_tinh: "review_duration", kieu_du_lieu: "INTEGER", rang_buoc: "", dien_giai: "Thời gian ôn tập"),
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
  caption: [Bảng diễn giải cho Table Review Log],
)
