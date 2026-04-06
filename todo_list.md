# DB

- Migration
    - https://rogerbinns.github.io/apsw/tips.html#managing-and-updating-your-schema
    - https://stackoverflow.com/questions/989558/best-practices-for-in-app-database-migration-for-sqlite
    - fastmigrate
    - apswutils
- Encryption: at rest
- Litestream

# Auth

- DELETE /logout → DELETE /login

- Username → Email
    - Lấy email làm khoá chính
- Đặt điều kiện Validation
- Validation trên Client
- Validation trên Server
- Gửi email xác nhận
- Đổi mật khẩu
- Đổi email

# Read

- Từ điển Popup: [Selection API](https://developer.mozilla.org/en-US/docs/Web/API/Selection)
- Badge hiện mức độ: xanh dễ, vàng oke, đỏ khó

## Not now

- Kéo thả chú thích: [Freeform Drag](https://starhtml.com/demos/view/16-freeform-drag/)
- CSV mỗi từ trong nguyên cả cuốn sách
- Chỉ tập trung từng câu: chia bài đọc ra thành từng câu nhỏ để có thể dễ dàng tập trung. Tách văn bản ra thành mỗi câu một dòng. Người đọc muốn đọc tiếp phải bấm nút để hiện câu tiếp theo.
- Cá nhân hoá lộ trình học: sử dụng NGSLT và SRS để xác định độ khó của bài đọc.
    - Một trang riêng, giống Anki hiện các deck, bấm vô mới hiện chi tiết trước khi bắt đầu
- Đọc thể loại nhiều: tuyển chọn và giới thiệu cho người đọc các tác phẩm văn học đình đám được viết bằng tiếng Anh. Người đọc có thể chủ động tìm đọc ở ngoài hệ thống để không cần phải phụ thuộc vào kết nối mạng, hoặc có thể đọc và thu thập từ vựng ngay thẳng trong hệ thống. Standard Ebooks.
- Load từng câu vào bộ nhớ. Khi người dùng bấm tiếp theo thì pop ở đầu mảng. Hàng đợi.

# Mining

- Từ điển cá nhân: người học tích góp những từ bản thân muốn ghi nhớ.
- Người đọc bôi đen một từ, hệ thống sẽ hiện một pop-up bao gồm: phiên âm, giọng đọc, và một ô để người đọc tự điền vào nghĩa của từ đấy, sau đó hệ thống sẽ lưu từ đó vào từ điển cá nhân của người học. Nếu người dùng muốn hệ thống tự động điền thì cần phải trả phí, nhằm hạn chế việc phụ thuộc quá nhiều.
- Người đọc có thể bôi đen một cụm từ hoặc một câu để có thể nhờ hệ thống dịch sang ngôn ngữ khác. Đây là một tính năng cần trả phí để hạn chế việc lạm dụng.
- Wiktionary Parser
- spaCy: phân tích part of speech của từ bôi đen để lọc ra kết quả Wiktionary Parser

# SRS

- Py-FSRS
- Chủ động gợi nhớ: trong quá trình đọc, đến một câu chứa từ cần phải ôn vào ngày đấy, người học sẽ phải trả lời trước khi chuyển qua câu tiếp theo. Tính năng này giúp làm giảm thời gian phải chuyển qua chuyển lại hai màn hình đọc và ôn từ vựng.
- Đến một câu chứa từ cần phải ôn, người đọc cần trả lời trước khi tiếp tục đọc. Những từ không xuất hiện trong bài đọc sẽ được chuẩn bị ở cuối bài đọc để người học thực hiện việc ôn tập ngay trong màn hình đó.
- Không có màn hình dành riêng cho việc ôn tập từ vựng, để khuyến khích người học đầu tư vào việc đọc nhiều hơn, thay vì tập trung ghi nhớ từ vựng hơn.

# Draw

- Vẽ hình kèm theo note
    - Lưu hình kiểu gì: Hình→Text
    - [Etch-a-Sketch](https://www.theodinproject.com/lessons/foundations-etch-a-sketch): lưu HTML các div
- Vẽ hình minh hoạ cho những người đọc khác. Like/Dislike để người dùng tự quản lí
