

# To-Do List

- Show toàn bộ entry trong từ điển
- Card Browser, đặt tên là Memory
    - Rút db.execute ra từ retire và delete? Nah, có chút xíu vậy mà cũng rút ra chi, mệt vl
    - Rút popup
- Tham khảo sqlite_demo: DB_DIR
- Tương tự các từ mined giờ chỉ cần click, từ nào trong bài đọc giờ cũng có thể click
    - Bỏ các từ trong các ô giải thích ra, vẫn cần phải select
    - Các từ trong ô Wiktionary cũng phải click được → cũng hiện từ đã mined chưa
- View Transition
    - Pagination trong Read, Test Progress, Reading Ease, vào bài đọc: move trái move phải
    - Hiện popup: wipe như Star War từ trên xuống
- Lỗi replace whole word
    - các `data-*` attribute có khả năng bị regex nhận dạng là whole word
    - cần phải đổi thuật toán tìm whole word
- Dark mode switcher
- Thống kê quá trình học tập

# CSDL

- Thêm Indexing cho các truy vấn WHERE
- Gộp các execute vào 1 transaction

# Read

- Progressive load từ điển Wiktionary: `data-ignore-morph`
- Done toggle
- CSV mỗi từ trong nguyên cả cuốn sách
- Bỏ simplemma, dùng lemmatized and stats để kiểm tra
- Chỉ tập trung từng câu: chia bài đọc ra thành từng câu nhỏ để có thể dễ dàng tập trung. Tách văn bản ra thành từng câu. Người đọc muốn đọc tiếp phải bấm nút để hiện câu tiếp theo.
    - Bấm tiếp theo thì thêm câu tiếp theo vào section
    - Load từng câu vào bộ nhớ. Khi người dùng bấm tiếp theo thì pop ở đầu mảng. Hàng đợi.
- Standard Ebooks: tuyển chọn và giới thiệu cho người đọc các tác phẩm văn học đình đám được viết bằng tiếng Anh. Người đọc có thể chủ động tìm đọc ở ngoài hệ thống để không cần phải phụ thuộc vào kết nối mạng, hoặc có thể đọc và thu thập từ vựng ngay thẳng trong hệ thống.
- Khi không có JS, popup là một trang riêng
- Width slider: [Pipulate](https://pipulate.com/)
- Lọc các bài đã đọc và chưa đọc

# Mining

- Phiên âm: Free Dictionary API's `pronunciations`
- Đồng nghĩa, trái nghĩa: Free Dictionary API's `synonyms`, `antonyms`
- Dịch: [Argos Translate](https://www.argosopentech.com/)
- Giọng đọc:
    - [Speech Synthesis](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API#speech_synthesis)
- Cân nhắc [Free Dictionary API](https://dictionaryapi.dev/)
- spaCy: phân tích part of speech của từ bôi đen để lọc ra kết quả Wiktionary Parser
- Show toàn bộ entry trong từ điển
- CSS calc top của inset để popup giữa màn hình
- Popup, bôi một từ trong dictionary, quay trở lại từ trước
-

# SRS

- spaCy: yêu cầu phải tách mỗi câu một dòng trước
- Kiểm tra độ dài khi gửi đến server

# Auth

- Khi không có JS, nút đăng xuất chuyển hướng người dùng đến trang để hỏi muốn đăng xuất không.

# Setting

- Tối ưu thông số
    - Chỉ một optimizer được chạy trong cả hệ thống

# Code

- @timed_cache
- db.get(auth) → db.auth
- Stario `relay.py` → StarHTML `Relay`
- `data-attr:disabled`

# DB

- Migration
    - https://rogerbinns.github.io/apsw/tips.html#managing-and-updating-your-schema
    - https://stackoverflow.com/questions/989558/best-practices-for-in-app-database-migration-for-sqlite
    - fastmigrate
    - apswutils
- Encryption: at rest
- Litestream

# Auth

- Username → Email
    - Lấy email làm khoá chính
- Đặt điều kiện Validation
- Validation trên Client
- Validation trên Server
- Gửi email xác nhận
- Đổi mật khẩu
- Đổi email
- Logout là một trang riêng

# Test

- Quay trở lại câu trước
- Xem lại đáp án
- Trang result, hiện đáp án sai
- Column
    - Bài làm: 12341243
    - Đúng sai: 10010101
- Không hiểu bolded là gì ⇒ chụp hình giải thích
- Giải thích cách làm bài bằng bàn phím nhanh hơn
- Các đáp án nên làm bằng ngôn ngữ mẹ đẻ sẽ dễ hiểu hơn

# UI

- Focus state, viền nên dày hơn
- Giao diện phèn
