#set page(margin: (top: 3cm, bottom: 3.5cm, left: 3.5cm, right: 2cm))
#set par(leading: 21pt, spacing: 1.5em, first-line-indent: 0pt, justify: true)
// leading: giữa các dòng; spacing: giữa các đoạn văn
#show heading: set block(above: 1.4em, below: 1em)

// only first level headings on a new page
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  it
}

#set text(font: "Times New Roman", size: 13pt, lang: "vi")

#include "000_front_matter/trang_bia.typ"

#align(center, [#heading(level: 1, outlined: false)[LỜI CẢM ƠN]])
#include "000_front_matter/loi_cam_on.typ"

// Heading 1 thì nên in đậm chữ
#show outline.entry.where(level: 1): set text(weight: "bold")

// thêm chữ Chapter cho Heading 1
#show outline.entry.where(level: 1): it => {
  link(
    it.element.location(),
    it.indented(
      [Chương #it.prefix()],
      it.inner(),
    ),
  )
}


#align(center, outline(title: "MỤC LỤC"))

#align(center, outline(
  title: "DANH MỤC HÌNH",
  target: figure.where(kind: image),
))

#align(center, outline(
  title: "DANH MỤC BẢNG",
  target: figure.where(kind: table),
))

#align(center, [#heading(level: 1, outlined: true)[TÓM TẮT ĐỒ ÁN]])
#include "000_front_matter/004_abstract.typ"


#set page(numbering: "1")
#counter(page).update(1)

#set heading(numbering: "1.")

#show heading.where(level: 1): it => block("Chương " + counter(heading).display("1. ") + it.body)

#set list(marker: [-], indent: 1em)



= GIỚI THIỆU ĐỀ TÀI

#include "100_introduction/100_introduction.typ"

== Lí do chọn đề tài
#include "100_introduction/101_necessity_of_topic.typ"

== Mục tiêu đề tài
#include "100_introduction/102_system_objectives.typ"

== Phạm vi đề tài
=== Đối tượng người dùng
#include "100_introduction/104_user_scope_and_audience.typ"

=== Phạm vi môi trường
#include "100_introduction/103_environment_scope.typ"

=== Phạm vi chức năng
#include "100_introduction/106_feature_scope.typ"

== Phương pháp thực hiện
#include "100_introduction/105_methodology.typ"

== Công nghệ sử dụng
#include "000_front_matter/008_technologies_used.typ"

== Kết quả mong đợi
#include "000_front_matter/009_achieved_results.typ"

= KIẾN THỨC NỀN TẢNG

== Theoretical Basis
#include "200_theoretical_basis_and_technology/201_theoretical_basis.typ"

== Overview of Related Technologies
#include "200_theoretical_basis_and_technology/202_related_technologies_overview.typ"

== Rationale for Technology Selection
#include "200_theoretical_basis_and_technology/203_technology_selection_rationale.typ"


// = SYSTEM REQUIREMENTS ANALYSIS

// == Problem Description and Business Logic
// #include "300_system_requirements_analysis/301_problem_description_and_business_logic.typ"

// == Stakeholders
// #include "300_system_requirements_analysis/302_stakeholders.typ"

// == Functional Requirements
// #include "300_system_requirements_analysis/303_functional_requirements.typ"

// == Non-Functional Requirements
// #include "300_system_requirements_analysis/304_non_functional_requirements.typ"

// == Use Case Diagram
// #include "300_system_requirements_analysis/305_use_case_diagram.typ"
// #include "300_system_requirements_analysis/306_use_case_specifications.typ"


// = SYSTEM DESIGN

// == Overall Architecture Design
// #include "400_system_design/401_overall_architecture_design.typ"

// == Functional Design
// #include "400_system_design/402_functional_design.typ"

// == Data Design
// #include "400_system_design/403_data_design.typ"






// = IMPLEMENTATION AND DEPLOYMENT

// == Development Environment
// #include "500_implementation_and_deployment/501_development_environment.typ"

// == Source Code Structure
// #include "500_implementation_and_deployment/502_source_code_structure.typ"

// == Implementation of Main Functions
// #include "500_implementation_and_deployment/503_implementation_main_functions.typ"

// == System Deployment
// #include "500_implementation_and_deployment/504_system_deployment.typ"


// = TESTING AND EVALUATION

// == Testing Strategy
// #include "600_testing_and_evaluation/601_testing_strategy.typ"

// == Test Case Construction and Execution
// #include "600_testing_and_evaluation/602_test_case_construction_and_execution.typ"

// // == System Evaluation
// // #include "600_testing_and_evaluation/603_system_evaluation.typ"


// = CONCLUSION AND FUTURE DEVELOPMENT

// == Conclusion
// #include "700_conclusion_and_future_development/701_conclusion.typ"

// == Limitations of the Project
// #include "700_conclusion_and_future_development/702_limitations.typ"

// == Future Development
// #include "700_conclusion_and_future_development/703_future_development.typ"

#align(center, [#heading(level: 1, numbering: none)[TÀI LIỆU THAM KHẢO]])
#bibliography(title: none, "bib.bib")
