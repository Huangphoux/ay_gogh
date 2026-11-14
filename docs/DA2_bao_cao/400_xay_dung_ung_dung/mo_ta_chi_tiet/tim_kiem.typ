#set heading(level: 3)

#pagebreak()
= Popup
- *Giao diện*:

#figure(
  image("../images/read.search.png", height: 50%),
  caption: [Trang tìm từ trong các bài đọc],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (
    ten: "Tiêu đề trang tìm từ",
    kieu: "Heading 1",
    rang_buoc: "",
    y_nghia: "Cho biết trang mà người dùng đang truy cập.",
  ),
  (
    ten: "Ô nhập từ cần tìm",
    kieu: "Input",
    rang_buoc: "",
    y_nghia: "Cho phép người dùng gõ từ cần tìm.",
  ),
  (
    ten: "Nút Search",
    kieu: "Button",
    rang_buoc: "",
    y_nghia: "Gửi yêu cầu đến hệ thống để tìm từ đó trong bài đọc.",
  ),
  (
    ten: "Bảng kết quả tìm từ",
    kieu: "Heading 1",
    rang_buoc: "",
    y_nghia: "Hiện kết quả tìm từ cho người dùng",
  ),
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
  caption: [Thành phần của Trang tìm từ trong các bài đọc],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Bấm vào nút Search", xu_li: "Gửi yêu cầu tìm từ đến hệ thống."),
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
  caption: [Danh sách biến cố Trang tìm từ trong các bài đọc],
)
