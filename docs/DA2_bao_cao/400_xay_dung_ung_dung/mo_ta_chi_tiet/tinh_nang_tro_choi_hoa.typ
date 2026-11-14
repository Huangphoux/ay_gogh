#set heading(level: 3)

#pagebreak()
= Popup
- *Giao diện*:

#figure(
  image("../images/gamification.png", height: 50%),
  caption: [Trang các tính năng trò chơi hoá],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (
    ten: "Ô hiện số ngày đọc liên tục",
    kieu: "Section",
    rang_buoc: "",
    y_nghia: "Cho biết số chuỗi ngày người dùng đọc sách liên tục.",
  ),
  (
    ten: "Ô nhắc nhở các chương đang đọc dở dang",
    kieu: "Details",
    rang_buoc: "",
    y_nghia: "Nhắc nhở người dùng các chương còn đang đọc dở dang.",
  ),
  (
    ten: "Ô nhắc nhở các từ đang cần được ôn tập vào ngày đó",
    kieu: "Section",
    rang_buoc: "",
    y_nghia: "Nhắc nhở người dùng các từ đang cần được ôn tập vào ngày đó.",
  ),
  (
    ten: "Ô hiện các huy hiệu tán dương",
    kieu: "Section",
    rang_buoc: "",
    y_nghia: "Cho biết các huy hiệu tán dương mà người dùng đạt được.",
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
  caption: [Thành phần của Trang các tính năng trò chơi hoá],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Bấm vào ô nhắc nhở các chương đang đọc dở dang", xu_li: "Hiện danh sách các chương đang đọc dở dang."),
  (
    bien_co: "Bấm vào ô nhắc nhở các từ đang cần được ôn tập vào ngày đó",
    xu_li: "Hiện danh sách các từ đang cần được ôn tập vào ngày đó.",
  ),
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
  caption: [Danh sách biến cố Trang các tính năng trò chơi hoá],
)
