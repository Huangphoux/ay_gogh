#import "@preview/diatypst:0.8.0": *

#show: slides.with(
  title: "Xây dựng trang web hỗ trợ đọc và ghi nhớ từ vựng tiếng Anh bằng AI",
  subtitle: "Đồ án 1 - SE121.Q21",
  date: datetime.today().display(),
  authors: "23521224 Trương Hoàng Phúc",

  ratio: 4 / 3,
  layout: "small",
  title-color: blue,
  toc: true,
  theme: "full",
  count: "number",
)


= Giới thiệu đề tài
= Công nghệ sử dụng

- Python: ngôn ngữ lập trình
- Datastar: thư viện Front-End
- StarHTML: thư viện Back-End
- SQLite: cơ sở dữ liệu
- FSRS: thuật toán lên lịch học tập
- Simple.css: hệ thống giao diện

= Các tính năng được thực hiện trước giữa kỳ
- Trang đăng nhập, đăng kí
- Kiểm tra vốn từ vựng
  - Xử lí PDF của NGSLT sang CSV để sử dụng
  - Có thể làm bài kiểm tra nhiều lần trong một ngày
- Popup
  - Chỉ có 2 cách trả lời để giảm gánh nặng lựa chọn

= Các tính năng được thực hiện sau giữa kỳ
- Đánh giá độ khó bài đọc
  - Cho biết độ khó của mỗi bài đọc
  - Phân tích người học biết được bao nhiêu % từ trong bài đọc
- Popover API
- Cho biết từ có nằm trong danh sách NGSL hay không, và cấp độ của từ.
-

= Các đặc biệt nổi bật của đồ án
- Cơ hội tìm hiểu kiến trúc và công nghệ mới
- MPA thay vì SPA: sử dụng Datastar thay React để làm Front-End ⇒ toàn bộ đồ án được làm bằng Python
- CQRS + Fat Morph: giao diện phản ánh trạng thái của cơ sở dữ liệu.
- Single Tenant:

= Ưu điểm

= Khuyết điểm

= Hướng phát triển đề tài
- Trang thống kê
- Trang quản lí từ điển cá nhân
