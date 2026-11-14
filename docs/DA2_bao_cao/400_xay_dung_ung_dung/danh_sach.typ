

#let dict = (
  (
    id: 1,
    name: "Popup",
    note: "Popup chắt lọc nghĩa của từ, hiện các thông tin bổ ích, và chừa chỗ để lưu lại ngữ cảnh của từ.",
  ),
  (
    id: 2,
    name: "Trang trò chơi đoán từ",
    note: "Trang trò chơi đoán các từ trong danh sách NGSL.",
  ),
  (
    id: 3,
    name: "Trang các tính năng trò chơi hoá",
    note: "Trang các tính năng trò chơi hoá: Nhắc nhở các chương đang đọc dở dang, Nhắc nhở các từ đang cần được ôn tập vào ngày đó, Chuỗi ngày đọc liên tục, Huy hiệu tán dương",
  ),
  (
    id: 4,
    name: "Trang tìm kiếm",
    note: "Trang tìm từ trong các bài đọc.",
  ),
)

#figure(
  table(
    table.header([*STT*], [*Tên màn hình*], [*Diễn giải*]),
    align: (center, left, left),
    columns: 3,
    ..for item in dict {
      ([#item.id], [#item.name], [#item.note])
    },
  ),
  caption: [Danh sách các màn hình],
)
