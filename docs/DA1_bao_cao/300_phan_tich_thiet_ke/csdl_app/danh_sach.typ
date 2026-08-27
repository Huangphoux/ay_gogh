#set heading(level: 4)

= Sơ đồ cơ sở dữ liệu
#figure(
  image("diagram.png"),
  caption: [Sơ đồ cơ sở dữ liệu của hệ thống],
)

= Danh sách các bảng dữ liệu

#let thanh_phan = (
  (ten: "user", dien_giai: "Lưu thông tin tài khoản người dùng"),
  (ten: "form_a", dien_giai: "Bộ câu hỏi NGSLT form A"),
  (ten: "form_b", dien_giai: "Bộ câu hỏi NGSLT form B"),
  (ten: "form_c", dien_giai: "Bộ câu hỏi NGSLT form C"),
  (ten: "chapter", dien_giai: "Nội dung chương đọc và metadata"),
  (ten: "ngsl", dien_giai: "Danh sách NGSL và level"),
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
