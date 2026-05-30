#set heading(level: 4)

= Sơ đồ cơ sở dữ liệu
#figure(
  image("diagram.png"),
  caption: [Sơ đồ cơ sở dữ liệu của hệ thống],
)

= Danh sách các bảng dữ liệu

#let thanh_phan = (
  (ten: "test", dien_giai: "Lưu kết quả các lần kiểm tra"),
  (ten: "chapter", dien_giai: "Trạng thái hoàn thành chương"),
  (ten: "deck", dien_giai: "Thẻ từ vựng cho ôn tập"),
  (ten: "review_log", dien_giai: "Lịch sử ôn tập thẻ"),
  (ten: "settings", dien_giai: "Cấu hình người dùng"),
)

#figure(
  table(
    table.header([*STT*], [*Tên bảng dữ liệu*], [*Diễn giải*]),
    align: (center, left, left),
    columns: 3,
    ..for (i, item) in thanh_phan.enumerate() {
      (str(i + 1), [#item.ten], [#item.dien_giai])
    },
  ),
  caption: [Bảng mô tả các bảng dữ liệu của hệ thống],
)

= Mô tả chi tiết các bảng dữ liệu
#include "mo_ta_chi_tiet.typ"
