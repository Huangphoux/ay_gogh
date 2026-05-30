#set heading(level: 3)

= Trang kết quả kiểm tra
- *Giao diện*:

#figure(
  image("../images/test.index.png", height: 50%),
  caption: [Trang kết quả kiểm tra],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Tiêu đề Test", kieu: "Heading", rang_buoc: "", y_nghia: "Nhận diện trang"),
  (
    ten: "Nút Take a test/Continue",
    kieu: "Button",
    rang_buoc: "",
    y_nghia: "Bắt đầu/tiếp tục bài kiểm tra",
  ),
  (ten: "Bảng lịch sử kết quả kiểm tra", kieu: "Table", rang_buoc: "", y_nghia: "Danh sách các lần kiểm tra"),
  (ten: "Khối phân tích kết quả", kieu: "Section", rang_buoc: "", y_nghia: "Giải thích kết quả"),
  (ten: "Kết quả tổng", kieu: "Paragraph", rang_buoc: "", y_nghia: "Tổng % từ vựng NGSL"),
  (ten: "Thông báo chờ kết quả", kieu: "Notice", rang_buoc: "", y_nghia: "Hiển thị khi chưa xong"),
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
  caption: [Thành phần của Trang kết quả kiểm tra],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Nhấn Take a test/Continue", xu_li: "Đi đến /test/intro"),
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
  caption: [Danh sách biến cố Trang kết quả kiểm tra],
)
