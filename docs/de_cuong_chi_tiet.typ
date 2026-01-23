#set page(margin: 1.75in)
#set par(leading: 0.55em, spacing: 0.55em, first-line-indent: 1.8em, justify: true)
#show heading: set block(above: 1.4em, below: 1em)
#set text(font: "New Computer Modern")
// #set text(font: "Times New Roman")
#set text(size: 12pt)

#set page(numbering: "1")
#show link: underline

#align(center)[
  #text(size: 20pt, weight: "bold")[ĐỀ CƯƠNG CHI TIẾT]
]

= Tên đề tài tiếng Việt
Xây dựng website hỗ trợ đọc và ghi nhớ từ vựng tiếng Anh bằng AI

= Tên đề tài tiếng Anh
English Vocabulary and Reading Skills Enrichment Website

= Cán bộ hướng dẫn
ThS. Trần Thị Hồng Yến

= Thời gian thực hiện dự kiến
Từ tháng 03/2026 đến tháng 06/2026

= Sinh viên thực hiện
Trương Hoàng Phúc — 23521224

= Nội dung đề tài
- Mô tả chi tiết về tổng quan đề tài, mục tiêu, phạm vi, đối tượng, phương pháp thực hiện, kết quả mong đợi của đề tài,

= Lí do chọn đề tài
- Các hệ thống hỗ trợ học tiếng Anh hiện nay vẫn chưa chú trọng kĩ năng đọc tiếng Anh, một kĩ năng mà sinh viên các ngành kĩ thuật cần phải có để có thể tham khảo được các tài liệu tiếng Anh thuộc lĩnh vực chuyên ngành.
- Duolingo từ trước đến giờ đã luôn cổ xuý việc học bằng cách dịch các mẫu câu văn độc lập, thay vì cho người học tiếp cận với những đoạn văn hình thành nên một ngữ cảnh; giọng đọc đi kèm không còn là  giọng người bản xứ nữa; kĩ năng nói trọng tâm vào độ phát âm chính xác thay vì kĩ năng giao tiếp tức thời.
- Bản thân nhận thấy các bạn sinh viên xung quanh đều chật vật với các vấn đề sau trong việc học tiếng Anh: không thể đầu tư thời gian trong ngày cho việc học tiếng Anh; không biết nơi để tiếp cận nội dung tiếng Anh; trước khi bắt đầu thì phải dành thời gian tìm hiểu nên học bằng cách nào, thành ra chẳng bao giờ bắt đầu.
- Mong muốn được biến hoá cuốn sách #link("https://archive.org/details/english-by-the-nature-method/")[English by the Nature Method] thành một định dạng khác dễ tiếp cận hơn là PDF.

= Mục tiêu đề tài
- Tạo một hệ thống giới thiệu đại chúng phương pháp học Immersion: chủ động tiếp cận và tập trung tiếp xúc các nội dung tiếng Anh trong thời gian dài.
- Người học có thể tuỳ ý làm bài kiểm tra đầu vào để xác định vốn từ vựng căn bản của bản thân đã đạt đến mức độ nào.
- Những cải tiến so với các hệ thống hiện hành:
  - Đọc số lượng nhiều: người học dành ít nhất 15 phút trong ngày để tập trung cho việc đọc văn bản tiếng Anh.
  - Lặp lại ngắt quãng: người học tích góp những từ bản thân muốn ghi nhớ mỗi ngày và sử dụng thuật toán để lên lịch thời gian ôn tập hiệu quả.
  - Chủ động gợi nhớ: trong quá trình đọc, đến một câu chứa từ cần phải ôn vào ngày đấy, người học sẽ phải trả lời trước khi đọc câu tiếp theo. Tính năng này giúp làm giảm thời gian phải chuyển qua chuyển lại hai màn hình đọc và ôn từ vựng.
  - Cá nhân hoá lộ trình học: sử dụng kết quả bài kiểm tra đầu vào để xác định những chương mà người học có thể bỏ qua được, do chứa từ vựng mà người học đã biết từ trước.
  - Đọc thể loại nhiều: tuyển chọn và giới thiệu cho người đọc các tác phẩm văn học đình đám được viết bằng tiếng Anh. Người đọc có thể chủ động tìm đọc ở ngoài hệ thống để không cần phải phụ thuộc vào kết nối mạng, hoặc có thể đọc và thu thập từ vựng ngay thẳng trong hệ thống.

= Phạm vi đề tài
- Hệ thống trang web trực tuyến.

= Phương pháp thực hiện
- Sử dụng #link("https://www.newgeneralservicelist.com/ngslt-nawlt")[New General Service List Test] để kiểm tra vốn từ vựng căn bản.
- Sử dụng #link("https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler")[Free Spaced Repetition Scheduling Algorithm] để lên lịch ôn tập.
- Sử dụng các sách của #link("https://standardebooks.org/")[Standard Ebooks] để giới thiệu văn học tiếng Anh.
- Thống nhất trình bày các bài đọc của English by the Nature Method và Standard Ebooks thành định dạng HTML. Khi truy cập, chỉ cần gửi HTML thẳng đến trình duyệt của người đọc.
- Sử dụng #link("https://github.com/suyashb95/WiktionaryParser")[Wiktionary Parser] để truy vấn một từ ở trang Wiktionary và trích dữ liệu trả về các định nghĩa, ví dụ, phiên âm, và giọng đọc từ đó.
- Sử dụng #link("https://www.argosopentech.com/")[Argos Translate
  ] để cung cấp dịch vụ dịch câu. Số lần lạm dụng dịch vụ này sẽ được ghi lại.


= Công nghệ sử dụng
- Front End:
  - #link("https://simplecss.org/")[Simple.css]: bổ sung thiết kế cơ bản cho HTML, tận dụng các tính năng có sẵn của HTML, tối ưu SEO, hỗ trợ trợ năng có sẵn.
  - #link("https://data-star.dev/")[Datastar]: framework bổ sung các tính năng linh động cho trang web tĩnh, tránh việc phải phát triển toàn bộ giao diện bằng JavaScript.
- Back End:
  - Python 3: đảm bảo tính dễ đọc và dễ bảo trì hệ thống trong tương lai, ít xảy ra rủi ro hệ sinh thái bị tấn công so với JavaScript.
  - #link("https://starhtml.com/")[StarHTML]: một nhánh của #link("FastHTML")[https://fastht.ml/], tích hợp Datastar thay vì #link("https://htmx.org/")[htmx]. Viết các đường dẫn trả về HTML ngay trong Python, và gửi các HTML ấy thẳng đến trình duyệt.
- Cơ sở dữ liệu:
  - SQLite: Không cần tạo một server chỉ dành riêng cho cơ sở dữ liệu, từ đó bỏ hẳn việc phải sử dụng Docker. Đảm bảo tính trường tồn của cơ sở dữ liệu #link("https://sqlite.org/lts.html")[đến năm 2050].
- Triển khai:
  - Docker: tự động hoá quy trình tái tạo môi trường làm việc của hệ thống.
  - Hetzner: làm quen với quy trình tự triển khai trang web lên đám mây.
- Quản lý mã nguồn: GitHub.

= Kế hoạch thực hiện
- Mô tả kế hoạch làm việc và phân công công việc cho từng sinh viên tham gia

= Hạn chế
- Nội dung quyển sách không gây hứng thú cho người đọc.
- Tìm một cách để luyện kĩ năng nghe của người đọc.

người học sẽ đọc toàn bộ cả quyển sách English by the Nature Method. Quyển sách gồm có 60 chương. Cả quyển sách chỉ sử dụng xoay quanh 2300 từ thông dụng nhất. Mỗi văn bản của từng chương trung bình gồm 720 từ, thời gian đọc hết 15 phút. Người học sẽ đọc qua 43200 từ (có lặp lại) và đã đầu tư được 15 giờ học tiếng Anh.
