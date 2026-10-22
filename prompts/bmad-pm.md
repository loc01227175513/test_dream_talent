/bmad-prd headless: true. Intent: create. Fast path, no questions — do not wait for user input; tag every inference [ASSUMPTION].

Input: `out/brief.md` (product brief from the BMAD Analyst). Output a PRD in Vietnamese to your normal planning-artifacts location, then ALSO write `out/SRS.md`: the PRD restructured as an IEEE 830 SRS with these headings:
`## 1. Giới thiệu`, `## 2. Mô tả tổng quan`, `## 3. Yêu cầu chức năng`, `## 4. Yêu cầu phi chức năng`, `## 5. Epics & User Stories`, `## 6. Ma trận truy vết`, `## 7. Câu hỏi mở`.
Each functional requirement: heading `#### FR-<nn> <title>`, then Actor, preconditions, main flow, acceptance criteria as Given/When/Then, and a line exactly `- **Truy vết:** F-xx, F-yy` citing only feature IDs that exist in out/brief.md.
Non-functional requirements as NFR-<nn> with a measurable target. Epics prioritised with MoSCoW.
