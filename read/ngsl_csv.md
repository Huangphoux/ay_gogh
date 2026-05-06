- lấy nội dung bài đọc
- bỏ phần code block
- bỏ các dấu câu
- chạy qua từng từ
- chuyển sang lowercase

- word → lemma
- lemma → rank
- rank → level: floor(rank/562)
- isNGSL: lemma không có rank

- kết quả mà mình muốn đạt được
- frontmatter có
- lv1: 1809
- lv2: 450
- unique: 450

- có 2 bước
- quét chapter, tạo csv: word, lemma
- quét chapter, đếm số cho lv

# Cách mới
- Với từng chapter.md
- Bỏ frontmatter
- Bỏ các dòng < max len / 5
- Chuyển toàn bộ sang lemma
- Bỏ các lemma lặp lại
- Quét từng cái, cái nào là lv1, lv2
- Cái nào không có thì [0], lv1 thì [1]