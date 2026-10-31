#figure(
  image("./static/ngslt.png", width: 80%),
  caption: [Trang web của New General Service List Test.],
)
#set heading(offset: 2)

New General Service List Test (NGSLT, Bài kiểm tra danh sách hỗ trợ tổng quát mới) @ngslt là một bài kiểm tra được tạo ra nhằm để chẩn đoán năng lực nhận diện được mặt chữ của các từ trong NGSL. Được phát triển bởi Phil Bennett và Tim Stoeckel, NGSLT chia NGSL thành 5 cấp độ, mỗi cấp độ bao gồm 562 từ. Trong mỗi cấp độ, chọn ra 20 từ để đại diện cho độ khó trung bình của các từ trong cấp độ đấy. Ta dùng kết quả của mỗi cấp độ để đánh giá ngưỡng kiến thức của người học.

Trong đồ án này, NGSLT được sử dụng để kiểm tra vốn từ vựng căn bản của người dùng và sử dụng kết quả để đánh giá độ khó của bài đọc, kèm hướng dẫn người dùng nên tập trung vào việc cải thiện các cấp độ còn yếu.

Để phân tích độ khó của từng bài đọc, ta phân tích % số từ vựng NGSL trong mỗi bài đọc. Sử dụng kết quả bài kiểm tra (% số từ vựng NGSL mà người dùng biết) nhân với % số từ vựng NGSL trong mỗi bài đọc, suy ra được % số từ vựng NGSL trong bài đọc mà người dùng biết.

= Ưu điểm
- *Độ tin cậy cao*: Qua việc tổ chức cho 847 học viên bao gồm học sinh trung học phổ thông và sinh viên đại học làm bài kiểm tra NGSLT @ngslt_doc, thống kê cho thấy độ tin cậy của bài kiểm tra nằm trong khoảng 83-87%, một chỉ số rất đáng để tin cậy.
- *Chia NGSL thành năm cấp độ nhỏ*: thay vì chia danh sách 2809 từ thành 3 cấp độ, mỗi cấp độ 1000 từ, NGSLT chia thành 5 cấp độ, mỗi cấp độ 562 từ. Việc chia nhỏ từng cấp độ như vậy giúp giảm gánh nặng của người học phải học nhiều từ vựng cùng một lúc.
- *Phân tích độ khó bài đọc theo năng lực của người học*: thay vì sử dụng các công thức tính độ khó của bài đọc một cách cứng nhắc, việc sử dụng kết quả của NGSLT để đánh giá độ khó các bài đọc sẽ giúp tuỳ biến trải nghiệm đọc sách đối với mỗi người học.

= Nhược điểm
- *Chưa hỗ trợ được nhiều ngôn ngữ*: NGSLT sử dụng cấu trúc tương tự như Vocabulary Size Test (VST, Bài kiểm tra kích cỡ từ vựng). Thống kê của kiểm thử VST cho thấy rằng khi các câu hỏi bằng tiếng Anh và các câu trả lời bằng tiếng bản địa, kết quả bài kiểm tra vượt trội hơn hẳn 10% so với các bài có các câu trả lời bằng tiếng Anh. Do đó, cần phải cung cấp thêm các phiên bản bằng ngôn ngữ khác của bài kiểm tra để có thể hỗ trợ người học làm bài kiểm tra tốt nhất.
