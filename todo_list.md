# To-Do List

- Remove Graceful Degradation
- Hiện badge: ✅NGSL LV1, ❌NGSL
- Show toàn bộ entry trong từ điển

# Refactor
- Remove all Form, use Signal instead

# Read

- Progressive load từ điển Wiktionary: `data-ignore-morph`
- Done toggle
- CSV mỗi từ trong nguyên cả cuốn sách
- Chỉ tập trung từng câu: chia bài đọc ra thành từng câu nhỏ để có thể dễ dàng tập trung. Tách văn bản ra thành từng câu. Người đọc muốn đọc tiếp phải bấm nút để hiện câu tiếp theo.
    - Bấm tiếp theo thì thêm câu tiếp theo vào section
    - Load từng câu vào bộ nhớ. Khi người dùng bấm tiếp theo thì pop ở đầu mảng. Hàng đợi.
- Standard Ebooks: tuyển chọn và giới thiệu cho người đọc các tác phẩm văn học đình đám được viết bằng tiếng Anh. Người đọc có thể chủ động tìm đọc ở ngoài hệ thống để không cần phải phụ thuộc vào kết nối mạng, hoặc có thể đọc và thu thập từ vựng ngay thẳng trong hệ thống.
- Khi không có JS, popup là một trang riêng
- Done toggle

# Mining

- Phiên âm: Free Dictionary API's `pronunciations`
- Đồng nghĩa, trái nghĩa: Free Dictionary API's `synonyms`, `antonyms`
- Dịch: [Argos Translate](https://www.argosopentech.com/)
- Giọng đọc:
    - [Speech Synthesis](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API#speech_synthesis)
- Cân nhắc [Free Dictionary API](https://dictionaryapi.dev/)
- thẻ man, woman, Germany, many. bôi man trước, không bôi toàn bộ woman, Germany, many
- spaCy: phân tích part of speech của từ bôi đen để lọc ra kết quả Wiktionary Parser
- Nếu mà viết hoa không có thì tìm viết thường
- Xoá từ mined
- Show toàn bộ entry trong từ điển

# SRS

- Change word trong popup, wiktionary đổi theo, nhớ debounce
- spaCy: yêu cầu phải tách mỗi câu một dòng trước
- Kiểm tra độ dài khi gửi đến server
- Đánh dấu học thuộc: Anki's `Suspend`

# Auth

- Khi không có JS, nút đăng xuất chuyển hướng người dùng đến trang để hỏi muốn đăng xuất không.

# Setting

- Tối ưu thông số: Background Task

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
