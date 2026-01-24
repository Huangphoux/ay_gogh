#set page(margin: 1.75in)
#set par(leading: 0.75em, spacing: 0.55em, first-line-indent: 1.8em, justify: true)
#show heading: set block(above: 1.4em, below: 1em)
// #set text(font: "New Computer Modern")
#set text(font: "Times New Roman")
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

= Lí do chọn đề tài
- Các hệ thống hỗ trợ học tiếng Anh hiện nay vẫn chưa chú trọng kĩ năng đọc tiếng Anh, một kĩ năng cần phải có để sinh viên có thể tham khảo được các tài liệu tiếng Anh.
- Duolingo khuyến khích việc học bằng cách dịch các mẫu câu văn độc lập, thay vì cho người học tiếp cận với những đoạn văn hình thành nên một ngữ cảnh; giọng đọc đi kèm không còn là  giọng người bản xứ nữa; kĩ năng nói trọng tâm vào độ phát âm chính xác thay vì kĩ năng giao tiếp tức thời.
- Bản thân nhận thấy các bạn sinh viên xung quanh đều chật vật với các vấn đề sau trong việc học tiếng Anh: không thể đầu tư thời gian trong ngày cho việc học tiếng Anh; không biết nơi để tiếp cận nội dung tiếng Anh; trước khi bắt đầu thì phải dành thời gian tìm hiểu nên học bằng cách nào, thành ra chẳng bao giờ bắt đầu.
- Mong muốn được biến hoá cuốn sách #link("https://archive.org/details/english-by-the-nature-method/")[English by the Nature Method] thành một định dạng khác dễ tiếp cận hơn là PDF.

= Mục tiêu đề tài
- Tạo một hệ thống giới thiệu đại chúng phương pháp học Immersion: chủ động tiếp cận và tập trung tiếp xúc các nội dung tiếng Anh trong thời gian dài.
- Người học có thể tuỳ ý làm bài kiểm tra đầu vào để xác định vốn từ vựng căn bản của bản thân đã đạt đến mức độ nào.
- Những cải tiến so với các hệ thống hiện hành:
  - Đọc số lượng nhiều: người học dành ít nhất 15 phút trong ngày để tập trung cho việc đọc văn bản tiếng Anh.
  - Chỉ tập trung từng câu: chia bài đọc ra thành từng câu nhỏ để có thể dễ dàng tập trung.
  - Từ điển cá nhân: người học tích góp những từ bản thân muốn ghi nhớ.
  - Lặp lại ngắt quãng: sử dụng thuật toán thông minh để lên lịch ôn tập từ vựng mỗi ngày một cách tối ưu nhất.
  - Chủ động gợi nhớ: trong quá trình đọc, đến một câu chứa từ cần phải ôn vào ngày đấy, người học sẽ phải trả lời trước khi chuyển qua câu tiếp theo. Tính năng này giúp làm giảm thời gian phải chuyển qua chuyển lại hai màn hình đọc và ôn từ vựng.
  - Cá nhân hoá lộ trình học: sử dụng các kết quả bài kiểm tra với từ điển cá nhân để xác định độ khó của bài đọc so với kiến thức của người học.
  - Đọc thể loại nhiều: tuyển chọn và giới thiệu cho người đọc các tác phẩm văn học đình đám được viết bằng tiếng Anh. Người đọc có thể chủ động tìm đọc ở ngoài hệ thống để không cần phải phụ thuộc vào kết nối mạng, hoặc có thể đọc và thu thập từ vựng ngay thẳng trong hệ thống.

= Phạm vi đề tài
- Hệ thống trang web trực tuyến để có thể được truy cập bằng mọi thiết bị sử dụng trình duyệt.

== Các tính năng chính
- Quản lý tài khoản người học: đăng ký, đăng nhập; lưu trữ các thông tin sau: kết quả các bài kiểm tra, từ điển cá nhân, số lượng chương đã hoàn thành.
- Kiểm tra vốn từ vựng: người học có thể kiểm tra vốn từ vựng cốt lõi của bản thân bất cứ lúc nào.
- Đọc sách:
  - Sử dụng kết quả bài kiểm tra kèm với từ điển cá nhân để đánh giá độ khó của bài đọc so với trình độ của người học.
  - Tách văn bản ra thành mỗi câu một dòng. Người đọc muốn đọc tiếp phải bấm nút để hiện câu tiếp theo.
  - Người đọc bôi đen một từ, hệ thống sẽ hiện một pop-up bao gồm: phiên âm, giọng đọc, và một ô để người đọc tự điền vào nghĩa của từ đấy, sau đó hệ thống sẽ lưu từ đó vào từ điển cá nhân của người học. Nếu người dùng muốn hệ thống tự động điền thì cần phải trả phí.
  - Người đọc có thể bôi đen một cụm từ hoặc một câu để có thể nhờ hệ thống dịch sang ngôn ngữ khác. Đây là một tính năng cần trả phí.
  - Đến một câu chứa từ cần phải ôn, người đọc cần trả lời trước khi tiếp tục đọc. Những từ không xuất hiện trong bài đọc sẽ được chuẩn bị ở cuối để người học thực hiện việc ôn tập ngay trong màn hình đó.
- Không có màn hình dành riêng cho việc ôn tập từ vựng, để khuyến khích người học đầu tư vào việc đọc nhiều hơn, thay vì tập trung ghi nhớ từ vựng hơn.

== Các tính năng cân nhắc mở rộng trong tương lai
- Cung cấp cho người học ngữ cảnh và cách đọc một từ bởi người bản xứ sử dụng dịch vụ #link("https://youglish.com/")[YouGlish]
  - Lý do không triển khai ngay bây giờ: tồn tại giới hạn sử dụng mỗi ngày, không thể phát triển lâu dài nếu không trả phí.
- Triển khai cuốn sách #link("https://archive.org/details/selected-short-stories/")[Selected Short Stories] được viết ra dành cho những người đã học xong English by the Nature Method.
  - Lý do không triển khai ngay bây giờ: không có ranh giới ngăn cách các bài đọc rõ ràng, khó thực hiện việc xử lí dữ liệu sách.
- Triển khai các bộ từ khác của #link("https://www.newgeneralservicelist.com/")[New General Service List Project
  ]
  - #link("https://www.newgeneralservicelist.com/new-general-service-list-1")[New Academic Word List]: dành cho những người làm việc trong giới học thuật hoặc có nhu cầu dự thi chứng chỉ IELTS.
  - #link("https://www.newgeneralservicelist.com/toeic-service-list")[TOEIC Service List]: dành cho những người có nhu cầu dự thi chứng chỉ TOEIC.
  - #link("https://www.newgeneralservicelist.com/business-service-list")[Business Service List]: dành cho những người đi làm trong doanh nghiệp.
  - Lý do không triển khai ngay bây giờ: không khuyến khích việc chú tâm vào việc học các từ vựng đơn lẻ, thay vì đọc nhiều.
- Sử dụng các dữ liệu giọng đọc đã được phiên âm sẵn, như #link("https://keithito.com/LJ-Speech-Dataset/")[LJ Speech], để triển khai tính năng Shadowing.
  - Lý do không triển khai ngay bây giờ: bài tập chú trọng vào việc phát âm, không đặt trọng tâm vào việc lĩnh hội ngữ nghĩa.

= Đối tượng sử dụng
- Tổng quát: các cá nhân có nhu cầu cải thiện vốn kiến thức tiếng Anh căn bản, không chỉ giới hạn ở mỗi Việt Nam.
- Cụ thể: học sinh sinh viên Việt Nam có khả năng sử dụng điện thoại Android.

= Giới hạn của đề tài
- Nội dung quyển sách English by the Nature Method chưa đủ hứng thú cho người đọc.
- Chưa có các chức năng trao dồi kĩ năng nghe, nói, và viết của người học.
- Bộ 2300 từ của quyển sách được phát triển vào năm 1942 đã quá lỗi thời và có thể không tương thích với bộ 2809 từ của #link("https://www.newgeneralservicelist.com/new-general-service-list")[New General Service List] được phát hành vào năm 2023.

= Phương pháp thực hiện
- Sử dụng #link("https://www.newgeneralservicelist.com/ngslt-nawlt")[New General Service List Test] để kiểm tra vốn từ vựng căn bản.
- Sử dụng #link("https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler")[Free Spaced Repetition Scheduling Algorithm] để lên lịch ôn tập.
- Sử dụng các sách của #link("https://standardebooks.org/")[Standard Ebooks] để giới thiệu văn học tiếng Anh.
- Thống nhất trình bày các bài đọc của English by the Nature Method và Standard Ebooks thành định dạng HTML. Khi truy cập, chỉ cần gửi HTML thẳng đến trình duyệt của người đọc.
- Sử dụng #link("https://github.com/suyashb95/WiktionaryParser")[Wiktionary Parser] để truy vấn từ vựng bằng Wiktionary và trích dữ liệu trả về các định nghĩa, ví dụ, phiên âm, và giọng đọc từ đó.
- Sử dụng #link("https://www.argosopentech.com/")[Argos Translate
  ] để cung cấp dịch vụ dịch câu.

= Công nghệ sử dụng
- Front End:
  - #link("https://simplecss.org/")[Simple.css]: bổ sung thiết kế cơ bản cho HTML, tận dụng các tính năng có sẵn của HTML, tối ưu SEO, hỗ trợ trợ năng có sẵn.
  - #link("https://data-star.dev/")[Datastar]: framework bổ sung các tính năng linh động cho trang web tĩnh, tránh việc phải phát triển toàn bộ giao diện bằng JavaScript.
- Back End:
  - Python 3: đảm bảo tính dễ đọc và dễ bảo trì hệ thống trong tương lai, ít xảy ra rủi ro hệ sinh thái bị tấn công so với JavaScript.
  - #link("https://starhtml.com/")[StarHTML]: một nhánh của #link("https://fastht.ml/")[FastHTML], tích hợp Datastar thay vì #link("https://htmx.org/")[htmx]. Viết các đường dẫn trả về HTML ngay trong Python, và gửi các HTML ấy thẳng đến trình duyệt.
- Cơ sở dữ liệu:
  - SQLite: Không cần tạo một server chỉ dành riêng cho cơ sở dữ liệu, từ đó bỏ hẳn việc phải sử dụng Docker. Đảm bảo tính trường tồn #link("https://sqlite.org/lts.html")[đến năm 2050].
- Triển khai:
  - Docker: tự động hoá quy trình tái tạo môi trường làm việc của hệ thống.
  - Hetzner: làm quen với quy trình tự triển khai trang web lên đám mây.
- Quản lý mã nguồn: GitHub.

= Kết quả mong đợi
- Hệ thống vận hành ổn định trên nhiều thiết bị. Chú trọng vào việc sử dụng trang web trên điện thoại Android truy cập bằng mạng 3G.

= Hướng phát triển đề tài
- Bổ sung tính năng PWA cho trang web
  - Không cần triển khai ứng dụng mobile native
  - Tham khảo cách triển khai của #link("https://github.com/Faststrap-org/Faststrap/commit/fafd8685da8560713a8eb0ec82795558d4284941#diff-bfe2b02319a1c2b5521cebb77390f1a94253f2016f2737aae0ff33e3ed1e471e")[FastStrap]

= Kế hoạch thực hiện
- 26/01/2026 → 01/02/2026: viết mô tả tính năng cho ba phạm vi chính của hệ thống (kiểm tra đầu vào, đọc sách, từ điển cá nhân).
- 02/02/2026 → 08/02/2026: triển khai tính năng kiểm tra đầu vào cơ bản.
- 23/02/2026 → 01/03/2026: triển khai tính năng đọc sách cơ bản.
- 02/03/2026 → 08/03/2026: triển khai tính năng từ điển cá nhân cơ bản.
- 09/03/2026 → 15/03/2026: trình bày MVP cho giảng viên hướng dẫn nhằm thu thập đóng góp.
- 16/03/2026 → 31/03/2026: viết báo cáo.
- 01/04/2026 → 30/05/2026: chỉnh chu hệ thống theo đóng góp.
- 01/05/2026 → 31/05/2026: hoàn thiện báo cáo.
- 01/06/2026 → 30/06/2026: chuẩn bị vấn đáp.

#v(1cm)

#table(
  columns: (1.5fr, 2fr),
  align: (center, center),
  rows: 5cm,
  [*Xác nhận của CBHD* \ (Ký tên và ghi rõ họ tên)],
  [*TP.HCM, ngày … tháng … năm … \ Sinh viên* \ (Ký tên và ghi rõ họ tên)],
)
