# Các tính năng còn lại

- Thêm phiên âm, dịch
- Đánh giá độ khó bài đọc
- Văn bản → mỗi câu một dòng
- Standard Ebooks
- spaCy
- Lỗi API từ điển không tìm được England
- Kiểm tra độ dài khi gửi đến server
- sess["name"] → name → auth

# Misc

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

# Test

# Read

- Badge hiện mức độ: xanh dễ, vàng oke, đỏ khó
- Progressive load từ điển Wiktionary
- Done ghi ngày, không dùng 1
- Done toggle

## Not now

- CSV mỗi từ trong nguyên cả cuốn sách
- Chỉ tập trung từng câu: chia bài đọc ra thành từng câu nhỏ để có thể dễ dàng tập trung. Tách văn bản ra thành từng câu. Người đọc muốn đọc tiếp phải bấm nút để hiện câu tiếp theo.
    - Bấm tiếp theo thì thêm câu tiếp theo vào section
- Cá nhân hoá lộ trình học: sử dụng NGSLT và SRS để xác định độ khó của bài đọc.
- Đọc thể loại nhiều: tuyển chọn và giới thiệu cho người đọc các tác phẩm văn học đình đám được viết bằng tiếng Anh. Người đọc có thể chủ động tìm đọc ở ngoài hệ thống để không cần phải phụ thuộc vào kết nối mạng, hoặc có thể đọc và thu thập từ vựng ngay thẳng trong hệ thống. Standard Ebooks.
- Load từng câu vào bộ nhớ. Khi người dùng bấm tiếp theo thì pop ở đầu mảng. Hàng đợi.

# Mining

- Dễ làm: phiên âm, dịch
- thẻ man, woman, Germany, many. bôi man trước, không bôi toàn bộ woman, Germany, many
- spaCy: phân tích part of speech của từ bôi đen để lọc ra kết quả Wiktionary Parser

# SRS

- Change word trong popup, wiktionary đổi theo, nhớ debounce
