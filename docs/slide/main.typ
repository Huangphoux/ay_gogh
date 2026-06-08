#import "@preview/diatypst:0.8.0": *

#show: slides.with(
  title: "Xây dựng trang web
hỗ trợ đọc và ghi nhớ từ vựng tiếng Anh bằng AI",
  subtitle: "Đồ án 1 - SE121.Q21",
  date: datetime.today().display(),
  authors: "23521224 Trương Hoàng Phúc",

  ratio: 4 / 3,
  layout: "small",
  title-color: blue,
  toc: true,
  theme: "normal",
  count: "number",
)

= Giới thiệu đề tài
- Ay Gogh! là một trang web hỗ trợ việc đọc sách English by the Nature Method, học từ vựng tiếng Anh bằng NGSL và FSRS.

#image("hero.png")

- English by the Nature Method là một cuốn sách giúp người đọc tự học tiếng Anh bằng tiếng Anh, với các chú thích ngắn gọn và hình ảnh giải thích dễ hiểu.

#figure(
  image("naturemethod.png", height: 70%),
)

- New General Service List (NGSL) là một danh sách gồm 2809 từ tiếng Anh thông dụng nhất. Chỉ cần biết 2809 từ này, người học có thể hiểu được 92% một văn bản tiếng Anh bất kì.

- Free Spaced Repetition Scheduler (FSRS) là một thuật toán lên lịch học tập ngắt quãng, sử dụng mô hình máy học để đáp ứng với thói quen học tập của người học.

= Công nghệ sử dụng

- Python: ngôn ngữ lập trình.
  - Viết các script xử lí dữ liệu OCR thô của English by the Nature Method, chia mỗi chương thành một tệp Markdown riêng
  - Viết script phân tích % các từ NGSL trong mỗi bài đọc

- Datastar: thư viện Front-End
  - Cập nhật giao diện bằng SSE, Brotli, và Fat Morphing

- StarHTML: thư viện Back-End
  - Viết HTML bằng Python, gửi HTML đến trình duyệt

- SQLite: cơ sở dữ liệu
  - Kiến trúc mỗi người dùng một cơ sở dữ liệu riêng

- Simple.css: hệ thống giao diện
  - Giảm thời gian thiết kế trang web

= Công việc trước báo cáo giữa kỳ
- Trang đăng nhập, đăng kí

- Kiểm tra vốn từ vựng
  - Xử lí PDF của NGSLT sang CSV
  - Có thể làm bài kiểm tra nhiều lần trong một ngày

- Popup
  - Tra từ điển trực tuyến: trong bài đọc, trong khung từ điển trực tuyến
  - Thêm, tra cứu, sửa định nghĩa cá nhân

#pagebreak()

- Lên lịch học tập ngắt quãng bằng FSRS
  - Chỉ có 2 cách trả lời, nhớ hoặc không nhớ: giảm gánh nặng lựa chọn
  - Tăng giảm Desired Retention, tối ưu #link("https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm#default-parameters")[thông số mặc định]
  - Từ mới thêm thì ngày mai mới được học

- Đọc sách
  - Đánh dấu hoàn thành bài đọc
  - Đánh dấu trong bài đọc các từ trong từ điển cá nhân


= Công việc sau báo cáo giữa kỳ
- Đánh giá độ khó bài đọc
  - Phân tích người học biết được bao nhiêu % từ NGSL trong bài đọc

- Đọc sách
  - Đánh dấu nguyên từ, thay vì một phần của từ
  - Huỷ đánh dấu hoàn thành bài đọc
  - Chú thích nằm ở 2 bên lề trái phải
  - Bật tắt chú thích và đánh dấu từ và lưu cài đặt vào CSDL
  - Bấm vào từ được đánh dấu, không cần bôi đen


#pagebreak()

- Popup
  - Sử dụng API có sẵn của trình duyệt: Popover API
  - Xoá từ
  - Hoãn ôn tập từ
  - Làm việc bằng lemma, dạng gốc của từ
  - Nút `Review anyway` bỏ qua giới hạn thời gian
  - Cho biết từ có nằm trong danh sách NGSL hay không, nếu có thì hiện cấp độ của từ.

= Ưu điểm
- MPA thay vì SPA: toàn bộ đồ án có thể được làm bằng Python

- Sử dụng Datastar, SSE, Brotli, SQLite, và kiến trúc CQRS để cập nhật giao diện nhanh chóng

- Mỗi người dùng một CSDL: không cần `JOIN`, không sợ bị rò rỉ dữ liệu của người dùng khác

= Khuyết điểm
- Thiết kế trang web quá tối giản

- Trang web chưa tạo được động lực học và sự hứng thú cho người dùng

- Khó unit test

- Chưa có luồng

= Hướng phát triển đề tài
- Trang thống kê quá trình học

- Trang quản lí từ điển cá nhân

- Chuẩn bị trước dữ liệu từ điển
