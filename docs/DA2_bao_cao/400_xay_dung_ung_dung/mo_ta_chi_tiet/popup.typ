#set heading(level: 3)

#pagebreak()
= Popup
- *Giao diện*:

#figure(
  image("../images/read.popup.png", height: 50%),
  caption: [Popup],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Khung popup", kieu: "Details/Popover", rang_buoc: "", y_nghia: "Hiển thị popup tra từ điển"),
  (ten: "Ô điền ngữ cảnh", kieu: "Textarea", rang_buoc: "", y_nghia: "Ô chứa ngữ cảnh của từ đang tìm"),
  (ten: "Nút từ loại", kieu: "Button", rang_buoc: "", y_nghia: "Khi bấm vào sẽ hiện từ loại của từ đang tìm"),
  (
    ten: "Nút chứa thông tin NGSL",
    kieu: "Button",
    rang_buoc: "",
    y_nghia: "Khi bấm vào sẽ hiện thứ hạng phổ biến và cấp độ NGSL của từ đó.",
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
  caption: [Thành phần của Popup thông báo từ chưa cần được ôn],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn nút từ loại", xu_li: "Hiện popup chỉ rõ từ loại của từ trong câu."),
  (bien_co: "Nhấn nút NGSL", xu_li: "Hiện popup chỉ rõ các thông tin NGSL của từ."),
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
  caption: [Danh sách biến cố Popup],
)
