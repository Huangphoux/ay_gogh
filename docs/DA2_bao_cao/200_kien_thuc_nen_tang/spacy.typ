#figure(
  image("static/spacy.png", width: 50%),
  caption: [Trang bìa của thư viện spaCy.],
)

#set heading(offset: 2)

spaCy @spacy là một thư viện Python cung cấp các tính năng hỗ trợ cho việc phân tích ngôn ngữ tự nhiên. Khác với Natural Language Toolkit (NLTK) được dùng cho mục đích giảng dạy và nghiên cứu, spaCy tập trung vào việc hỗ trợ phát triển các phần mềm cần các kĩ thuật phân tích ngôn ngữ tự nhiên.

Trong đồ án này, spaCy được sử dụng để phân tích từ loại của từ dựa trên ngữ cảnh, từ đó lọc ra các nghĩa không cần thiết của từ. Ngoài ra, spaCy còn được sử dụng trong việc phân tích số lượng từ NGSL trong một bài đọc.

= Ưu điểm
- *Dễ sử dụng*: spaCy được thiết kế nhằm cung cấp các kĩ thuật phân tích ngôn ngữ tự nhiên cho những người không chuyên. Vì thế, việc cài đặt và sử dụng thư viện trở nên cực kì đơn giản.
- *Hiệu suất nhanh chóng*: Thay vì sử dụng Python thuần để phát triển, spaCy sử dụng Cython để quản lí bộ nhớ trực tiếp giống ngôn ngữ C, từ đó cải thiện hiệu suất đáng kể so với việc chờ hệ thống dọn dẹp các dữ liệu thừa.

= Nhược điểm
- *Không phù hợp cho mục đích nghiên cứu*: spaCy sử dụng các kĩ thuật phân tích tối tân nhất, vì thế không bao gồm các kĩ thuật đã quá lỗi thời. Từ đó, spaCy không phù hợp cho việc nghiên cứu và so sánh các kết quả nghiên cứu.

