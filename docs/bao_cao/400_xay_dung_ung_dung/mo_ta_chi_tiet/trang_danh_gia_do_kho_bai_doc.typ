#set heading(level: 3)

= Trang đánh giá độ khó bài đọc
- *Giao diện*:

#figure(
  image("../images/read.num.ease.png", height: 50%),
  caption: [Trang đánh giá độ khó bài đọc],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Tiêu đề Reading Ease", kieu: "Heading", rang_buoc: "", y_nghia: "Nhận diện trang"),
  (ten: "Bảng đánh giá", kieu: "Table", rang_buoc: "", y_nghia: "Tỉ lệ NGSL và mức độ"),
  (ten: "Kết luận độ khó", kieu: "Paragraph", rang_buoc: "", y_nghia: "Mức độ easy/medium/hard"),
  (ten: "Nút Let's read", kieu: "Button/Link", rang_buoc: "", y_nghia: "Quay về bài đọc"),
  (ten: "Phần tham chiếu", kieu: "Section", rang_buoc: "", y_nghia: "Giải thích bảng tham chiếu"),
  (ten: "Bảng tham chiếu", kieu: "Table", rang_buoc: "", y_nghia: "Ngưỡng % và độ khó"),
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
  caption: [Thành phần của Trang đánh giá độ khó bài đọc],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Mở trang", xu_li: "Chuyển về /read/{num} nếu chưa hoàn thành test"),
  (bien_co: "Nhấn Let's read", xu_li: "Đi đến /read/{num}"),
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
  caption: [Danh sách biến cố Trang đánh giá độ khó bài đọc],
)
