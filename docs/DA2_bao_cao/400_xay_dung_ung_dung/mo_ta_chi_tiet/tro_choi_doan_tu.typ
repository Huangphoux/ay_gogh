#set heading(level: 3)

#pagebreak()
= Popup
- *Giao diện*:

#figure(
  image("../images/wordle.png", height: 50%),
  caption: [Trang trò chơi đoán từ],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Tựa đề", kieu: "Heading 1", rang_buoc: "", y_nghia: "Cho biết tên trò chơi"),
  (
    ten: "Nút New Word",
    kieu: "Button",
    rang_buoc: "Chỉ xuất hiện sau khi hoàn thành màn chơi",
    y_nghia: "Cho phép người dùng đoán từ mới",
  ),
  (
    ten: "Bảng hiện kết quả lượt đoán",
    kieu: "Table",
    rang_buoc: "",
    y_nghia: "Hiện kết quả của mỗi lần đoán từ của người chơi",
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
  caption: [Thành phần của Trang trò chơi đoán từ],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Bấm chữ cái trên bàn phím", xu_li: "Hiện kí từ đó trong bảng."),
  (bien_co: "Nhấn Enter", xu_li: "Hệ thống kiểm tra lượt đoán từ của người dùng."),
  (bien_co: "Nhấn nút New Word", xu_li: "Xoá bảng và cho người dùng đoán từ mới."),
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
  caption: [Danh sách biến cố Trang trò chơi đoán từ],
)
