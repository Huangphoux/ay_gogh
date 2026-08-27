#set heading(level: 3)

#pagebreak()
= Trang danh sách 10 bài đọc đầu tiên
- *Giao diện*:

#figure(
  image("../images/read.index.png", height: 50%),
  caption: [Trang danh sách 10 bài đọc đầu tiên],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Tiêu đề Read, 1-10", kieu: "Heading", rang_buoc: "", y_nghia: "Hiển thị phạm vi chương"),
  (ten: "Thành phần trang", kieu: "Navigation", rang_buoc: "", y_nghia: "Chuyển trang danh sách"),
  (ten: "Liên kết Chapter", kieu: "Link", rang_buoc: "", y_nghia: "Đi đến trang đọc chương"),
  (ten: "Trạng thái DONE", kieu: "Label", rang_buoc: "", y_nghia: "Đánh dấu chương đã hoàn thành"),
  (ten: "Nhãn độ khó", kieu: "Link", rang_buoc: "", y_nghia: "Đi đến đánh giá độ khó"),
  (ten: "Show all", kieu: "Link", rang_buoc: "", y_nghia: "Chuyển sang xem tất cả"),
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
  caption: [Thành phần của Trang danh sách 10 bài đọc đầu tiên],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn Previous/Next", xu_li: "Đi đến trang trước/sau"),
  (bien_co: "Nhấn số trang", xu_li: "Đi đến trang tương ứng"),
  (bien_co: "Nhấn Chapter", xu_li: "Đi đến /read/{num}"),
  (bien_co: "Nhấn độ khó", xu_li: "Đi đến /read/{num}/ease"),
  (bien_co: "Nhấn Show all", xu_li: "Đi đến danh sách tất cả"),
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
  caption: [Danh sách biến cố Trang danh sách 10 bài đọc đầu tiên],
)
