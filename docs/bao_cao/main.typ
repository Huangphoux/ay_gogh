#set text(font: "Times New Roman", size: 13pt)

// only first level headings on a new page
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  it
}

#include "000_front_matter/001_cover_page.typ"

#set page(margin: (top: 3cm, bottom: 3.5cm, left: 3.5cm, right: 2cm))
#set par(leading: 21pt, spacing: 1.5em, first-line-indent: 0pt, justify: true)
// leading: giữa các dòng; spacing: giữa các đoạn văn
#show heading: set block(above: 1.4em, below: 1em)
#set text(font: "Times New Roman", size: 13pt)

#align(center, [#heading(level: 1, outlined: false)[LỜI CẢM ƠN]])
#include "000_front_matter/003_acknowledgments.typ"

#outline(title: "Table of Contents")

#outline(
  title: "List of Figures",
  target: figure.where(kind: image),
)

#align(center, [#heading(level: 1, outlined: true)[TÓM TẮT ĐỒ ÁN]])
#include "000_front_matter/004_abstract.typ"


#set page(numbering: "1")
#counter(page).update(1)

#set heading(numbering: "1.")

#show heading.where(level: 1): it => block("Chương " + counter(heading).display("1. ") + it.body)

= GIỚI THIỆU ĐỀ TÀI

_Chương này trình bày về lý do chọn đề tài xây dựng trang web hỗ trợ đọc và ghi nhớ từ vựng tiếng Anh bằng AI nhằm cải thiện sự thiếu hụt về kĩ năng đọc của các bạn học sinh sinh viên hiện nay; xác định mục tiêu phát triển một trang web thân thiện, sử dụng thuật toàn AI để lên lịch học tập từ vựng một cách thông minh; giới hạn phạm vi trên nền tảng trang web; sử dụng công nghệ Python, SQLite, StarHTML, Simple.css, và Datastar; áp dụng các phương pháp học tập ngôn ngữ hiệu quả; hướng đến kết quả là một sản phẩm hỗ trợ hiệu quả, bảo mật và có trải nghiệm người dùng tốt._

== Lí do chọn đề tài
#include "100_introduction/101_necessity_of_topic.typ"

== Mục tiêu đề tài
#include "100_introduction/102_system_objectives.typ"

== Phạm vi đề tài
=== Đối tượng người dùng
=== Phạm vi môi trường
=== Phạm vi chức năng
#include "100_introduction/103_research_scope_and_limitations.typ"

== User Scope and Audience
#include "100_introduction/104_user_scope_and_audience.typ"

== Phương pháp thực hiện
#include "100_introduction/105_methodology.typ"

== Công nghệ sử dụng
#include "000_front_matter/008_technologies_used.typ"

== Kết quả mong đợi
#include "000_front_matter/009_achieved_results.typ"

= Kiến thức nền tảng

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

// = REFERENCES
// #include "800_references_appendix/801_references.typ"

// // = APPENDIX
// // #include "800_references_appendix/802_appendix.typ"

#bibliography("bib.bib")
