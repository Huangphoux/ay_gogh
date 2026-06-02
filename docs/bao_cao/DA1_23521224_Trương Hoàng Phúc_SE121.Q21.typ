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

// padding for table
#set table(inset: 10pt)
// table can be split into next page
#show figure: set block(breakable: true)
// figure numbering by chapter
#set figure(numbering: (..num) => numbering("1.1", counter(heading).get().first(), num.pos().first()))
// caption của bảng nằm trên, còn lại nằm dưới
#show figure.where(
  kind: table,
): set figure.caption(position: top)

#let h1 = (
  [TÓM TẮT ĐỒ ÁN],
  [GIỚI THIỆU ĐỀ TÀI],
  [KIẾN THỨC NỀN TẢNG],
  [PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG],
  [XÂY DỰNG ỨNG DỤNG],
  [KẾT LUẬN],
  [TÀI LIỆU THAM KHẢO],
)

#let irregular = ([TÓM TẮT ĐỒ ÁN], [TÀI LIỆU THAM KHẢO])

// thêm chữ Chapter cho Heading 1
#show outline.entry.where(level: 1): it => {
  text(
    weight: if it.element.body in h1 { "bold" } else { "regular" },
    link(
      // in đậm heading 1 trong mục lục
      it.element.location(),
      it.indented(
        if it.element.body in h1 and it.element.body not in irregular {
          "Chương " + it.prefix()
        } else if it.element.body in h1 and it.element.body in irregular {} else { it.prefix() + ":" },
        it.inner(),
      ),
    ),
  )
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

#include "200_kien_thuc_nen_tang/tom_tat_chuong.typ"

== Python
#include "200_kien_thuc_nen_tang/python.typ"
== Datastar
#include "200_kien_thuc_nen_tang/datastar.typ"
== StarHTML
#include "200_kien_thuc_nen_tang/starhtml.typ"
== SQLite
#include "200_kien_thuc_nen_tang/sqlite.typ"
== Simple.css
#include "200_kien_thuc_nen_tang/simplecss.typ"
== Free Spaced Repetition Scheduling Algorithm
#include "200_kien_thuc_nen_tang/fsrs.typ"
== New General Service List
#include "200_kien_thuc_nen_tang/ngsl.typ"
== English by the Nature Method
#include "200_kien_thuc_nen_tang/nature_method.typ"

= PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG

#include "300_phan_tich_thiet_ke/tom_tat_chuong.typ"

== Khảo sát hiện trạng
#include "300_phan_tich_thiet_ke/khao_sat.typ"

== Xác định các chức năng, yêu cầu
=== Yêu cầu chức năng
#include "300_phan_tich_thiet_ke/yeu_cau_chuc_nang.typ"
=== Yêu cầu phi chức năng
#include "300_phan_tich_thiet_ke/yeu_cau_phi_chuc_nang.typ"

== Use Case
=== Danh sách các Actor
#include "300_phan_tich_thiet_ke/danh_sach_actor.typ"
=== Danh sách các Use Case
#include "300_phan_tich_thiet_ke/danh_sach_use_case.typ"

== Sơ đồ Use Case
#include "300_phan_tich_thiet_ke/danh_sach_so_do_use_case.typ"

== Thiết kế cơ sở dữ liệu
=== Cơ sở dữ liệu của hệ thống
#include "300_phan_tich_thiet_ke/csdl_app/danh_sach.typ"
=== Cơ sở dữ liệu của người dùng
#include "300_phan_tich_thiet_ke/csdl_user/danh_sach.typ"

== Kiến trúc hệ thống
#include "300_phan_tich_thiet_ke/kien_truc_he_thong.typ"

= XÂY DỰNG ỨNG DỤNG

#include "400_xay_dung_ung_dung/tom_tat_chuong.typ"

== Danh sách các màn hình
#include "400_xay_dung_ung_dung/danh_sach.typ"
== Mô tả chi tiết các màn hình
#include "400_xay_dung_ung_dung/mo_ta_chi_tiet.typ"

= KẾT LUẬN

#include "500_ket_luan/tom_tat_chuong.typ"

== Kết quả đạt được
#include "500_ket_luan/ket_qua.typ"
== Nhận xét
=== Thuận lợi
#include "500_ket_luan/thuan_loi.typ"
=== Khó khăn
#include "500_ket_luan/kho_khan.typ"
== Ưu điểm
#include "500_ket_luan/uu_diem.typ"
== Nhược điểm
#include "500_ket_luan/nhuoc_diem.typ"
== Hướng phát triển
#include "500_ket_luan/huong_phat_trien.typ"

= TÀI LIỆU THAM KHẢO
#bibliography(title: none, "bib.bib")
