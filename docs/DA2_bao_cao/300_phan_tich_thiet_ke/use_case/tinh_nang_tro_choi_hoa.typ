#set heading(level: 4)
= Tính năng trò chơi hoá

#figure(
  image("/out/docs/DA2_bao_cao/300_phan_tich_thiet_ke/use_case/Tính năng trò chơi hoá.png", height: 30%),
  caption: [Sơ đồ Use Case Tính năng trò chơi hoá],
)


#figure(
  table(
    columns: 2,
    align: (left, left),
    [Use Case], [Tính năng trò chơi hoá],
    [Tác nhân chính], [User],
    [Mô tả ngắn gọn], [Hiện các thông tin về quá trình học của người dùng để động viên cố gắng.],
    [Điều kiện tiên quyết], [Đã đăng nhập.],
    [Sự kiện kích hoạt], [Người dùng truy cập trang Thông tin cá nhân.],
    [Điều kiện thực hiện], [Đã đọc một số bài đọc. Đã thu thập một số từ vựng.],
    [Luồng sự kiện chính],
    [
      + Người dùng truy cập trang Thông tin cá nhân.
      + Hiển thị cho người dùng biết về các chương đang đọc dở dang.
      + Hiển thị cho người dùng biết về các từ đang cần được ôn tập vào ngày đó.
      + Hiển thị cho người dùng biết về số ngày đọc liên tục không ngừng nghỉ.
      + Hiển thị cho người dùng biết về các cột mốc quan trọng bằng các huy hiệu.

    ],
  ),
  caption: [Bảng mô tả Use Case Tính năng trò chơi hoá],
)
