#set page(margin: (top: 3cm, bottom: 3.5cm, left: 3.5cm, right: 2cm))
// leading: giữa các dòng; spacing: giữa các đoạn văn
#set par(leading: 21pt, spacing: 1.5em, first-line-indent: 0pt, justify: true)
#set text(font: "Times New Roman", size: 13pt, lang: "vi")
#set list(marker: [-], indent: 1em)
#show heading: set block(above: 1.4em, below: 1em)

#show heading.where(level: 1): it => {
  pagebreak(weak: false) // Heading 1 nằm trên trang riêng
  let count = counter(heading).get().at(0)
  align(center, if count > 0 and count < 6 {
    // Thêm chữ Chương vào Heading 1 trên trang riêng
    ("Chương " + counter(heading).display("1. ") + it.body)
  } else { it.body })
}

// thêm chữ Chapter cho Heading 1
#show outline.entry.where(level: 1): it => {
  text(weight: "bold", link(
    // in đậm heading 1 trong mục lục
    it.element.location(),
    it.indented(
      if it.element.body.text not in ("TÓM TẮT ĐỒ ÁN", "TÀI LIỆU THAM KHẢO") {
        "Chương " + it.prefix()
      },
      it.inner(),
    ),
  ))
}

#include "000_mo_dau/trang_bia.typ"

#heading(outlined: false, "LỜI CẢM ƠN")
#include "000_mo_dau/loi_cam_on.typ"

#align(center, outline(title: "MỤC LỤC", indent: 2em))
#align(center, outline(title: "DANH MỤC HÌNH", target: figure.where(kind: image)))
#align(center, outline(title: "DANH MỤC BẢNG", target: figure.where(kind: table)))

#set page(numbering: "1")
#counter(page).update(1)

= TÓM TẮT ĐỒ ÁN
#include "000_mo_dau/tom_tat_do_an.typ"

#set heading(numbering: "1.")

= GIỚI THIỆU ĐỀ TÀI

#include "100_gioi_thieu_de_tai/tom_tat_chuong.typ"

== Lí do chọn đề tài
#include "100_gioi_thieu_de_tai/li_do_chon_de_tai.typ"

== Mục tiêu đề tài
#include "100_gioi_thieu_de_tai/muc_tieu_de_tai.typ"

== Phạm vi đề tài
=== Đối tượng người dùng
#include "100_gioi_thieu_de_tai/pham_vi_nguoi_dung.typ"

=== Phạm vi môi trường
#include "100_gioi_thieu_de_tai/pham_vi_moi_truong.typ"

=== Phạm vi chức năng
#include "100_gioi_thieu_de_tai/pham_vi_chuc_nang.typ"

== Phương pháp thực hiện
#include "100_gioi_thieu_de_tai/phuong_phap_thuc_hien.typ"

== Công nghệ sử dụng
#include "100_gioi_thieu_de_tai/cong_nghe_su_dung.typ"

== Kết quả mong đợi
#include "100_gioi_thieu_de_tai/ket_qua_mong_doi.typ"

= KIẾN THỨC NỀN TẢNG



= PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG

==

= XÂY DỰNG ỨNG DỤNG

== Danh sách các màn hình
== Mô tả chi tiết các màn hình

= KẾT LUẬN

== Kết quả đạt được

== Nhận xét
=== Thuận lợi
=== Khó khăn

== Ưu điểm
== Nhược điểm
== Hướng phát triển

= TÀI LIỆU THAM KHẢO
#bibliography(title: none, "bib.bib")
