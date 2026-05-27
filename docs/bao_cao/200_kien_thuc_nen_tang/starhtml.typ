#figure(
  image("./static/starhtml.png"),
  caption: [Trang web của framework StarHTML.],
)

#set heading(offset: 2)

StarHTML là một framework kết hợp Datastar với FastHTML, giúp viết các hàm gửi HTML đến trình duyệt một cách dễ dàng. Lấy cảm hứng từ FastHTML, người dùng có thể viết HTML bằng các hàm trong Python, từ đó loại bỏ lệ thuộc vào các template engine và tận dụng ngôn ngữ lập trình Python. StarHTML hỗ trợ viết các hàm gửi HTML và Server-sent Events bằng cách tận dụng tính năng decorator của Python.

Trong đồ án này, việc StarHTML cũng sử dụng Python, cùng ngôn ngữ với các script xử lí dữ liệu thô, giúp làm giảm gánh nặng phải quản lí nhiều ngôn ngữ trong hệ thống.

= Ưu điểm
- *Mã nguồn ngắn gọn, dễ đọc*: bằng việc tận dụng decorator của Python, ta có thể định nghĩa một hàm gửi cho đường dẫn gì dễ dàng, không cần phải tập trung các định nghĩa đường dẫn vào một chỗ, làm tăng thời gian tìm kiếm.
- *Viết HTML bằng Python*: các tag HTML được đóng gói trong các hàm Python, trước khi gửi đến trình duyệt sẽ được bung ra thành HTML hợp lệ và đúng ngữ nghĩa.
- *Hỗ trợ Server-sent Events không rườm rà*: một hàm khi được thêm decorator `@sse` sẽ có thể gửi HTML đến Front-End vô số lần.

= Nhược điểm
- *Dự án cá nhân*: Datastar được bắt đầU phát triển từ cuối tháng 8/2023, FastHTML từ tháng 6/2024, StarHTML bắt đầu từ tháng 5/2025 và được phát triển bởi chỉ một người duy nhất. Do đó StarHTML không có cộng đồng hỗ trợ và tài liệu hướng dẫn đầy đủ.

= Kiến trúc CQRS

- Đồ án này sử dụng Pub/Sub, Brotli, và Server-sent Events để triển khai kiến trúc CQRS, giúp đơn giản hoá việc cập nhật giao diện.
  - Pub/Sub: sử dụng `relay.py` của framework Stario để hệ thống gửi và nhận các tín hiệu cập nhật giao diện.
  - Server-sent Events: khi gửi kiểu dữ liệu `text/event-stream` thay vì `text/html` đến trình duyệt, máy chủ có thể gửi HTML liên tục trong một luồng dữ liệu đến trình duyệt.
  - Brotli: thuật toán nén dữ liệu ưu việt hơn gzip. Sử dụng Brotli để nén luồng dữ liệu Server-sent Events, ta có thể gửi HTML vô số lần mà không phải lo về việc tốn dữ liệu di động của người dùng.
- Kiến trúc CQRS: CQRS là từ viết tắt của Command Query Responsibility Segregation, tam dịch Tách biệt nghĩa vụ truy vấn và chỉnh sửa dữ liệu.
  - Khi người dùng truy cập vào trang, ngay lập tức gửi yêu cầu khởi tạo luồng dữ liệu Server-sent Events với máy chủ.
  - Một hàm `Query` đảm nhiệm nghĩa vụ nhận yêu cầu khởi tạo luồng dữ liệu cho một trang và gửi HTML vào luồng dữ liệu này, mỗi khi có tín hiệu cập nhật giao diện. Hàm `Query` luôn luôn truy vấn dữ liệu trên máy chủ rồi trình bày các dữ liệu đấy bằng HTML. Kết quả của hàm `Query` là một trang HTML hoàn chỉnh phản ánh dữ liệu trên máy chủ.
  - Khi người dùng tương tác với trang web và chỉnh sửa dữ liệu, gửi yêu cầu đến máy chủ.
  - Các hàm `Command` nhận yêu cầu cập nhật sẽ sửa đổi dữ liệu trên máy chủ, và gửi tín hiệu đến hàm `Query`.
  - Hàm `Query` nhận tín hiệu, truy vấn, rồi gửi kết quả vào luồng dữ liệu.
  - Việc gửi toàn bộ trang nhiều lần như thế này sẽ dẫn đến nhiều sự trùng lặp, do đó ta sử dụng Brotli để nén luồng dữ liệu.
  - Datastar khi nhận được kết quả HTML mới trong luồng dữ liệu sẽ sử dụng thuật toán morph để cập nhật giao diện.