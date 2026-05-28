#figure(
  image("./static/sqlite.svg"),
  caption: [Logo của cơ sở dữ liệu SQLite.],
)

#set heading(offset: 2)

SQLite @sqlite là một hệ thống cơ sở dữ liệu quan hệ được viết bởi Richard Hipp dưới dạng thư viện bằng ngôn ngữ lập trình C. SQLite là hệ thống cơ sở dữ liệu được dùng nhiều nhất trên thế giới, được nhúng vào các trình duyệt web, hệ điều hành, và điện thoại di động.

Trong đồ án này, SQLite được sử dụng để lưu trữ thông tin đăng nhập tài khoản của người dùng, bộ câu hỏi của NGSLT, các chương của quyển sách English by the Nature Method, 2809 từ của NGSL và xếp hạng cấp độ của mỗi từ; và các dữ liệu của riêng mỗi người dùng như kết quả bài kiểm tra, danh sách các chương đã hoàn thành, các từ được lưu lại trong từ điển cá nhân, lịch sử ôn tập từ vựng, và cài đặt hệ thống.

= Ưu điểm
- *Không có thời gian kết nối cơ sở dữ liệU*: do là cơ sở dữ liệu nhúng, các tệp cơ sở dữ liệu được nằm chung với mã nguồn của máy chủ, từ đó loại bỏ thời gian phải kết nối với cơ sở dữ liệu như PostgreSQL.
- *Kiến trúc Single Tenant*: do định dạng lưu trữ của SQLite là một tệp có đuôi *.db*, ta không cần phải gò bó với việc chỉ có một cơ sở dữ liệu. Ta có thể tạo một cơ sở dữ liệu riêng cho mỗi người dùng, giúp đảm bảo tính riêng biệt, không bị rò rỉ dữ liệu của người dùng lẫn nhau.

= Nhược điểm
- *Vận hành thủ công*: các tính năng mới của SQLite mặc định được tắt để không ảnh hưởng đến các cơ sở dữ liệu được tạo ra bởi phiên bản cũ của SQLite.
- *Không thể mở rộng theo chiều ngang*: do cơ sở dữ liệu nằm chung máy chủ, không thể tăng số lượng máy chủ do cơ sở dữ liệu không nằm ở một máy chủ riêng.
