#set heading(level: 3)

= Trang danh sách tất cả các bài đọc
- *Giao diện*:

Do kích cỡ hình ảnh quá khổ, kính mời bạn đọc xem thiết kế của #link("https://raw.githubusercontent.com/Huangphoux/ay_gogh/refs/heads/main/docs/bao_cao/400_xay_dung_ung_dung/images/read.index.all.png")[Trang danh sách tất cả các bài đọc].



- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Tiêu đề Read All", kieu: "Heading", rang_buoc: "", y_nghia: "Hiển thị chế độ xem tất cả"),
  (ten: "Danh sách chương", kieu: "Navigation", rang_buoc: "", y_nghia: "Liệt kê toàn bộ chương"),
  (ten: "Liên kết Chapter", kieu: "Link", rang_buoc: "", y_nghia: "Đi đến trang đọc chương"),
  (ten: "Trạng thái DONE", kieu: "Label", rang_buoc: "", y_nghia: "Đánh dấu chương đã hoàn thành"),
  (ten: "Nhãn độ khó", kieu: "Link", rang_buoc: "", y_nghia: "Đi đến đánh giá độ khó"),
  (ten: "Show less", kieu: "Link", rang_buoc: "", y_nghia: "Quay về danh sách 10"),
)

#figure(
  table(
    table.header([*STT*], [*Tên*], [*Kiểu*], [*Ràng buộc*], [*Ý nghĩa*]),
    align: (center, left, left, left, left),
    columns: 5,
    ..for (i, item) in thanh_phan.enumerate() {
      (str(i + 1), [#item.ten], [#item.kieu], [#item.rang_buoc], [#item.y_nghia])
    },
  ),
  caption: [Thành phần của Trang danh sách tất cả các bài đọc],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn Chapter", xu_li: "Đi đến /read/{num}"),
  (bien_co: "Nhấn độ khó", xu_li: "Đi đến /read/{num}/ease"),
  (bien_co: "Nhấn Show less", xu_li: "Đi đến /read/?all=0"),
)

#figure(
  table(
    table.header([*STT*], [*Biến cố*], [*Xử lí*]),
    align: (center, left, left),
    columns: 3,
    ..for (i, item) in bien_co.enumerate() {
      (str(i + 1), [#item.bien_co], [#item.xu_li])
    },
  ),
  caption: [Danh sách biến cố Trang danh sách tất cả các bài đọc],
)
