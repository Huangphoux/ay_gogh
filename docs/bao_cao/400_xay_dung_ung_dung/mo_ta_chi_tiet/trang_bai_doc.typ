#set heading(level: 3)

= Trang bài đọc
- *Giao diện*:

#figure(
  image("../images/read.num.png", height: 50%),
  caption: [Trang bài đọc],
)

- *Các thành phần của màn hình*:

#let thanh_phan = (
  (ten: "Thông tin chương", kieu: "Section", rang_buoc: "", y_nghia: "Hiển thị số chương và dạng chữ"),
  (ten: "Tiêu đề chương", kieu: "Heading", rang_buoc: "", y_nghia: "Tên chương và trạng thái DONE"),
  (ten: "Popup từ vựng", kieu: "Popup", rang_buoc: "", y_nghia: "Tra từ và thao tác từ"),
  (ten: "Toggles hiển thị", kieu: "Details", rang_buoc: "", y_nghia: "Bật/tắt highlight và aside"),
  (ten: "Nút Toggle popup", kieu: "Button", rang_buoc: "", y_nghia: "Mở/đóng popup"),
  (ten: "Nội dung bài đọc", kieu: "Section", rang_buoc: "", y_nghia: "Hiển thị nội dung chương"),
  (ten: "Danh sách từ đến hạn", kieu: "Section", rang_buoc: "", y_nghia: "Liệt kê từ cần ôn"),
  (ten: "Danh sách từ đã hoãn", kieu: "Section", rang_buoc: "", y_nghia: "Liệt kê từ đã hoãn"),
  (ten: "Nút Mark Complete", kieu: "Button", rang_buoc: "", y_nghia: "Đánh dấu hoàn thành"),
  (ten: "Nút Undo Complete", kieu: "Button", rang_buoc: "", y_nghia: "Hủy hoàn thành"),
  (ten: "Thông báo hoàn thành", kieu: "Notice", rang_buoc: "", y_nghia: "Xác nhận đã hoàn thành"),
  (ten: "Back to List", kieu: "Link", rang_buoc: "", y_nghia: "Quay lại danh sách chương"),
  (ten: "Bảng debug", kieu: "Details", rang_buoc: "", y_nghia: "Chỉ hiện ở debug"),
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
  caption: [Thành phần của Trang bài đọc],
)


- *Danh sách các biến cố của màn hình*:

#let bien_co = (
  (bien_co: "Chọn từ/nhấn từ", xu_li: "Mở popup tra từ"),
  (bien_co: "Nhấn Toggle popup", xu_li: "Mở/đóng popup"),
  (bien_co: "Bật/tắt Show colorful highlights", xu_li: "Lưu toggle hiển thị"),
  (bien_co: "Bật/tắt Show marginal explanations", xu_li: "Lưu toggle hiển thị"),
  (bien_co: "Nhấn Mark Complete", xu_li: "PATCH /read/{num}"),
  (bien_co: "Nhấn Undo Complete", xu_li: "DELETE /read/{num}"),
  (bien_co: "Nhấn từ trong danh sách từ", xu_li: "Mở popup tra từ"),
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
  caption: [Danh sách biến cố Trang bài đọc],
)
