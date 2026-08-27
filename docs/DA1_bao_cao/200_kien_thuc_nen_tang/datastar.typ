#figure(
  image("./static/datastar.png"),
  caption: [Trang web của framework Datastar.],
)

#set heading(offset: 2)

Datastar @datastar là một framework được phát triển chủ yếu bởi Delaney Gillilan và Ben Croker, được tạo ra để giúp xây dựng các trang web sử dụng HTML thay vì JSON. Datastar cung cấp các thuộc tính HTML `data-*` và Signal để điều khiển giao diện của mỗi trang và gửi yêu cầu đến Back-End. Sau đó Back-End sẽ gửi HTML đến Front-End, Datastar sẽ sử dụng thuật toán morphing để thay đổi giao diện của trang.

= Ưu điểm
- *Làm việc bằng HTML thay vì JSON*: Datastar là một trong các thư viện hỗ trợ xây dựng trang web bằng HTML. Thay vì phải tốn thời gian xây dựng Front-End và Back-End riêng (nghĩa rằng Back-End phải viết API bằng JSON để gửi dữ liệu đến Front-End, và Front-End phải điềU hướng giao diện trên trình duyệt bằng JavaScript), ta chỉ cần cho máy chủ gửi HTML đến trình duyệt và Datastar sẽ đảm nhiệm công việc thay đổi giao diện.
- *Kích thước nhỏ gọn*: Datastar là một tệp JavaScript đơn lẻ có kích thước khoảng 12 KB giúp người dùng dễ dàng nhúng framework vào trang web. Đồng nghĩa với việc Datastar hoàn toàn không phụ thuộc vào các thư viện khác. Người dùng sẽ không phải lo lắng về việc các thư viện bị tấn công và phải cập nhật hệ thống liên tục.

= Nhược điểm
- *Cộng đồng nhỏ*: do Datastar là một framework mới nên cộng đồng hỗ trợ nhỏ và tập trung trên Discord.
- *Đi ngược xu hướng*: Datastar là một framework chứ không phải là thư viện. Thư viện có thể được nhúng và gỡ khỏi hệ thống được, framework thì không. Datastar giới thiệu nhiều khái niệm đi kèm cần phải biết khi muốn tận dụng hiệu quả Datastar: Server-sent events, Brotli,  kiến trúc CQRS, Back-End gửi HTML, Fat Morph. Những khái niệm này giúp thiết kế một hệ thống đơn giản và dễ hiểu, nhưng đồng thời tạo ra một rào cản đối với những người đã quen với phương pháp phát triển web bằng JSON và các framework JavaScript.