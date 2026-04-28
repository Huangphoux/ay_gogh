# Read

- Badge hiện mức độ: xanh dễ, vàng oke, đỏ khó
    - Cá nhân hoá lộ trình học: sử dụng NGSLT và SRS để xác định độ khó của bài đọc.
- Progressive load từ điển Wiktionary: `data-ignore-morph`
- Done ghi ngày, không dùng 1
- Done toggle
- CSV mỗi từ trong nguyên cả cuốn sách
- Chỉ tập trung từng câu: chia bài đọc ra thành từng câu nhỏ để có thể dễ dàng tập trung. Tách văn bản ra thành từng câu. Người đọc muốn đọc tiếp phải bấm nút để hiện câu tiếp theo.
    - Bấm tiếp theo thì thêm câu tiếp theo vào section
    - Load từng câu vào bộ nhớ. Khi người dùng bấm tiếp theo thì pop ở đầu mảng. Hàng đợi.
- Standard Ebooks: tuyển chọn và giới thiệu cho người đọc các tác phẩm văn học đình đám được viết bằng tiếng Anh. Người đọc có thể chủ động tìm đọc ở ngoài hệ thống để không cần phải phụ thuộc vào kết nối mạng, hoặc có thể đọc và thu thập từ vựng ngay thẳng trong hệ thống.

# Mining

- Phiên âm: Free Dictionary API's `pronunciations`
- Đồng nghĩa, trái nghĩa: Free Dictionary API's `synonyms`, `antonyms`
- Dịch: [Argos Translate](https://www.argosopentech.com/)
- Giọng đọc:
    - [Speech Synthesis](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API#speech_synthesis)
- Cân nhắc [Free Dictionary API](https://dictionaryapi.dev/)
- thẻ man, woman, Germany, many. bôi man trước, không bôi toàn bộ woman, Germany, many
    - Cái tính năng bôi này bug vl
- spaCy: phân tích part of speech của từ bôi đen để lọc ra kết quả Wiktionary Parser

# SRS

- Change word trong popup, wiktionary đổi theo, nhớ debounce
- spaCy: yêu cầu phải tách mỗi câu một dòng trước
- Kiểm tra độ dài khi gửi đến server
- Đánh dấu học thuộc: Anki's `Suspend`

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
