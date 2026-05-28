#figure(
  image("static/python.svg", width: 80%),
  caption: [Logo của ngôn ngữ lập trình Python.],
)

#set heading(offset: 2)

Python @python là một ngôn ngữ lập trình bậc cao đa năng được phát triển bởi Guido van Rossum. Đặc điểm khác biệt của Python so với các ngôn ngữ lập trình khác là các từ khoá hoàn toàn bằng tiếng Anh tự nhiên, giúp tăng tính dễ đọc của mã nguồn. Hệ sinh thái của Python cũng rất rộng mở không kém JavaScript, trừ một đặc điểm rằng Python ít bị tấn công hàng loạt so với JavaScript.

Trong dự án Ay Gogh!, Python được sử dụng để thực hiện những công việc sau:
- Viết các script xử lý các dữ liệu thô của cuốn sách English by the Nature Method. Các script nằm trong thư mục `/read/text_cleaners`. Kết quả sau khi xử lí là các chương trong quyển sách được chia ra thành các tệp Markdown riêng và được lưu trữ trong thư mục `/read/chapter`.
- Viết script xử lí dữ liệu thô của các bài kiểm tra NGSLT. Script có tên `test/make_csv.py`. Kết quả là các tệp CSV trình bày từng câu hỏi thành một dòng dữ liệu.
- Viết code cho server sử dụng framework StarHTML xử lí các yêu cầu từ trình duyệt.

= Ưu điểm
- *Mã nguồn dễ đọc*: Python sử dụng các từ khoá sử dụng tiếng Anh tự nhiên, giúp tăng tính dễ đọc của mã nguồn. Đồng thời tách biệt các block của mã nguồn bằng thụt lề.
- *Thông dịch thay vì biên dịch*: Python sử dụng trình thông dịch giúp dịch và thực thi các câu lệnh ngay tức thì, không cần tốn thời gian biên dịch ra chương trình, giúp rút ngắn thời gian lập trình.
- *Hệ sinh thái đa dạng*: Python có hệ sinh thái đa dạng không kém JavaScript, không những thế còn ít bị tấn công hơn JavaScript.

= Nhược điểm
- *Tốc độ thông dịch*: vì phải vừa thông dịch vừa thực thi câu lệnh, hiệu suất vận hành của Python kém hơn so với các ngôn ngữ biên dịch.
- *Kiểu dữ liệu động*: trình thông dịch của Python không kiểm tra kiểu dữ liệu đầu vào của các hàm. Tính năng type hint của Python chỉ giúp kiểm tra trong quá trình lập trình, không kiểm tra lúc thực thi chương trình. Một biến có thể lưu trữ nhiều kiểu dữ liệu khác nhau. Đặc điểm này của Python dễ gây ra nhiều lỗi ngoài ý muốn.
