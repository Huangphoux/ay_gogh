#figure(
  image("./static/fsrs.png", width: 80%),
  caption: [Trang web của thư viện Datastar.],
)
#set heading(offset: 2)

Free Spaced Repetition Scheduling Algorithm (FSRS, Thuật toán lên lịch ngắt quãng tự do) là thuật toán lên lịch học tập thông minh được phát triển bởi Jarrett Ye. FSRS sử dụng các phương pháp Máy học để mô hình hoá các yếu tố ảnh hưởng đến trí nhớ và cho phép tối ưu các thông số để đáp ứng với nhu cầu học tập của mỗi người dùng.

Trong đồ án này, FSRS được sử dụng do hiệu suất lên lịch thông minh hơn hẳn thuật toán SM-2.

= Ưu điểm
- *Sử dụng Máy học để lên lịch*: thuật toán SM-2 sử dụng các công thức đơn giản được suy ra từ các số liệu ít ỏi. FSRS sử dụng Máy học và phân tích lịch sử học tập của hơn 20 ngàn người dùng để tính ra được các thông số, từ đó có thể lên lịch học tập tối ưu cho đa số người dùng.

= Nhược điểm
- *Khó nắm rõ được thuật toán*: do thuật toán được suy ra bằng Máy học, người không am hiểu khó có thể nắm rõ được cách vận hành thuật toán để mà tinh chỉnh cho nhu cầu cá nhân, khác với SM-2 sử dụng công thức đơn giản hơn.