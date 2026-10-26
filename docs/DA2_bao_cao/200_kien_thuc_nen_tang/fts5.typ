#figure(
  image("./static/fts5.png", width: 50%),
  caption: [Trang bìa của quyển sách English by the Nature Method.],
)

#set heading(offset: 2)

Mô-đun FTS5 của SQLite @fts5 là một mô-đun sử dụng bảng ảo để hỗ trợ cơ sở dữ liệu thêm tính năng tìm kiếm trong các văn bản số lượng lớn.

Trong đồ án này, FTS5 được sử dụng để phát triển tính năng cho phép người dùng tìm kiếm từ vựng trong các bài đọc.

= Ưu điểm
- *Tương thích sẵn trong SQLite*: thay vì sử dụng các dịch vụ bên thứ ba như Elasticsearch và phải quản lí thêm cacs dịch vụ đấy, việc SQLite có sẵn các tính năng tiện lợi như FTS5 giúp giảm thời gian phải tìm hiểu thêm công nghệ mới.

= Nhược điểm
- *Ít tính năng*: FTS5 có thể sẽ thiếu nhiều tính năng cần thiết hơn để phân tích dữ liệu so với các dịch vụ chuyên về lĩnh vực này.
