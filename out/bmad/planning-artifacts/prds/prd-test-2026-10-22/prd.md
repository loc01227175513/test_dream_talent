---
title: "PRD — MOSO.VN: Nền tảng PropTech BĐS \"3 THẬT\""
status: draft
created: 2026-10-22
updated: 2026-10-22
mode: headless · fast path
source: out/brief.md
---

# PRD: MOSO.VN — Nền tảng PropTech BĐS "3 THẬT"

> PRD được dựng ngược từ brief của Analyst (`out/brief.md`), chạy headless/fast path, không hỏi lại người dùng. Mọi suy luận không có trong brief được gắn **[ASSUMPTION]**. Bản đặc tả chi tiết theo IEEE 830 nằm ở `out/SRS.md` và dùng **cùng mã FR/NFR** với tài liệu này.

## 1. Tóm tắt

MOSO.VN là sàn giao dịch BĐS ứng dụng AI, trọng tâm TP.HCM, cạnh tranh bằng **độ tin cậy của dữ liệu** chứ không bằng số lượng tin: chuẩn **"3 THẬT" — Nhà Thật, Giá Thật, Địa Chỉ Thật**. Sản phẩm gồm marketplace mua bán/cho thuê/dự án, đăng tin bằng AI trả phí bằng MOSO Points, cơ chế "Ẩn số nhà" chống sao chép, hệ sinh thái môi giới/đối tác, kênh vay thế chấp với 13+ ngân hàng, bộ công cụ tài chính–pháp lý–đầu tư miễn phí, dữ liệu thị trường và một lớp API/MCP mở cho AI agent.

PRD này mô tả năng lực sản phẩm ở trạng thái mục tiêu, phân theo 11 module của brief. **[ASSUMPTION]** Phần lớn năng lực đã tồn tại trên sản phẩm thật. PRD dùng để chuẩn hoá yêu cầu, tiêu chí nghiệm thu và thứ tự ưu tiên cho các chu kỳ phát triển tiếp theo, không phải để xây từ đầu.

## 2. Vấn đề

| # | Vấn đề | Ai chịu |
|---|---|---|
| P1 | Tin ảo tràn lan: ảnh không thật, giá mồi, địa chỉ mập mờ; phải gọi điện mới biết giá/địa chỉ | Người mua/thuê (A1), nhà đầu tư (A6) |
| P2 | Tin bị sao chép, khách bị "cướp"; ảnh tải lại dính logo/SĐT người khác | Chủ nhà (A2), môi giới (A3) |
| P3 | Thiếu công cụ tự kiểm chứng: thuế phí, giá đất nhà nước, khả năng vay, nên mua hay chờ | A1, A6 |
| P4 | Môi giới thiếu nguồn hàng chính chủ, chứng chỉ hành nghề, kênh vay cho khách | A3, A4, A5 |
| P5 | AI agent khó truy cập dữ liệu BĐS có cấu trúc và đáng tin cậy **[ASSUMPTION]** | A7 |

## 3. Mục tiêu & chỉ số thành công

Mọi baseline và mục tiêu dưới đây đều là **[ASSUMPTION]** cho đến khi PM chốt (xem Q-02).

| Mục tiêu | Chỉ số | Baseline | Mục tiêu 12 tháng |
|---|---|---|---|
| G1 · Nhà Thật | % tin đang hiển thị có badge "Xác thực" | 91% (báo cáo T9/2026) | ≥ 95% |
| G2 · Không trùng lặp | % tin bị phát hiện trùng/sao chép | chưa đo | ≤ 2% |
| G3 · Chuyển đổi liên hệ | % yêu cầu xem nhà được chuyên viên xác nhận trong 2 giờ làm việc | chưa đo | ≥ 80% |
| G4 · Hệ sinh thái môi giới | Số môi giới/Partner hoạt động hằng tháng (≥ 1 tin hoặc 1 lead) | 1.000–2.000 (Q-02) | +50% |
| G5 · Tài chính | Số hồ sơ vay chuyển qua MOSO / tháng; tỷ lệ giải ngân | chưa đo | đặt sau quý đầu |
| G6 · Kênh agent | Số lead hợp lệ từ API/MCP mỗi tháng | chưa đo | đặt sau quý đầu |

**Counter-metrics (không được xấu đi):**
- Thời gian từ lúc gửi tin đến lúc tin hiển thị: xác thực chặt hơn không được làm luồng đăng tin chậm quá NFR-03.
- Tỷ lệ lead rác/spam qua API contact: tăng lưu lượng agent không được kéo theo lead giả (NFR-08).
- Khiếu nại về địa chỉ sai sau khi xem nhà: "Ẩn số nhà" không được làm giảm tính minh bạch với khách đã xác thực.
- Doanh thu points trên mỗi tin: ưu đãi cho tin xác thực (5 thay vì 8 MP) không được làm tổng doanh thu tin giảm quá 10% **[ASSUMPTION]**.

## 4. Người dùng (Actor)

Theo brief §4: **A1** người mua/thuê · **A2** chủ nhà (FSBO) · **A3** môi giới cá nhân · **A4** doanh nghiệp/sàn/CĐT · **A5** cộng tác viên · **A6** nhà đầu tư · **A7** AI agent bên thứ ba · **A8** chuyên viên/admin MOSO · **A9** KOL/KOC · **A10** hệ thống ngoài (ngân hàng, IEM, Urbox/Gotit, Cục THA, app store).

Không có User Journey dạng tường thuật: chạy headless nên không thu thập được phiên thật có nhân vật cụ thể. **[ASSUMPTION]** Nếu cần UJ, hãy chạy `bmad-ux` sau PRD.

A9 (KOL/KOC) chỉ là đối tác marketing, không có yêu cầu chức năng nào trên nền tảng **[ASSUMPTION]**.

## 5. Phạm vi

**Trong phạm vi:** toàn bộ 62 tính năng F-01…F-62 của brief, nhóm thành 45 yêu cầu chức năng (FR-01…FR-45) và 11 epic có ưu tiên MoSCoW.

**MVP / phát hành đầu [ASSUMPTION]:** các epic **Must** (E1, E2, E3, E4, E5, E11). Đây là vòng lõi "tìm → tin thật → liên hệ → đăng tin → trả phí".

**Ngoài phạm vi:**
- Giao diện backoffice chi tiết của A8 (chỉ nêu năng lực cần có, không đặc tả UI).
- Cổng thanh toán cụ thể và chính sách hoàn tiền (Q-08).
- Mô hình AVM thực sự (Q-06). Công cụ định giá giữ ở mức giá rao/m² ±10%.
- Check quy hoạch (F-42) được xếp **Won't** trong đợt này vì brief ghi trạng thái "Sắp ra mắt".

## 6. Yêu cầu chức năng (tóm tắt)

Đặc tả đầy đủ (Actor, tiền điều kiện, luồng chính, Given/When/Then) có tại `out/SRS.md` §3.

### M1 · Tìm kiếm & Khám phá
- **FR-01** Danh sách & lọc tin mua bán/cho thuê. *(F-01, F-02)*
- **FR-02** Trang danh mục SEO theo loại hình & khu vực. *(F-03)*
- **FR-03** Bản đồ BĐS: giá trên ghim, vẽ vùng; tôn trọng Ẩn số nhà. *(F-04, F-22)*
- **FR-04** Tìm kiếm AI bằng ngôn ngữ tự nhiên: tách câu thành bộ lọc, hiển thị và cho sửa bộ lọc đã suy ra. *(F-05, F-58)*
- **FR-05** Lưu tin, lưu tìm kiếm, thông báo tin mới. *(F-06)*
- **FR-06** Video BĐS (web + tab app). *(F-07, F-55)*
- **FR-07** Tra cứu & so sánh dự án sơ cấp. *(F-08, F-09)*
- **FR-08** Nguồn nhà đặc biệt (MOSO Signature): đấu giá/phát mãi, khách để lại tiêu chí. *(F-10)*

### M2 · Liên hệ & Giao dịch
- **FR-09** Nhắn tin trong ứng dụng với người đăng/chuyên viên. *(F-11)*
- **FR-10** Đặt lịch/yêu cầu xem nhà: chống trùng 24h, chuyên viên xác nhận, nhắc lịch. *(F-12, F-13)*
- **FR-11** Hỗ trợ giao dịch & pháp lý, gồm dịch vụ nâng cao có phí. *(F-14)*

### M3 · Đăng tin & Quản lý tin
- **FR-12** Đăng tin bán/cho thuê có AI soạn nháp trong khoảng 30 giây. *(F-15, F-16)*
- **FR-13** Tin của tôi: sửa, đổi giá, đánh dấu đã bán/đã thuê, ẩn tin, tự gia hạn 30 ngày. *(F-17, F-24)*
- **FR-14** Đẩy tin theo 3 gói. *(F-18)*
- **FR-15** Xoá watermark ảnh bằng AI. *(F-19)*
- **FR-16** Thống kê lượt xem/quan tâm theo thời gian thực. *(F-20)*

### M4 · Xác thực & Bảo vệ tin
- **FR-17** Xác thực tin theo chuẩn ARV, gắn badge "Xác thực". *(F-21)*
- **FR-18** Ẩn số nhà. *(F-22)*
- **FR-19** Tiêu chuẩn nội dung: AI soạn nháp, biên tập viên duyệt, có kênh đính chính. *(F-23)*

### M5 · MOSO Points & Thanh toán
- **FR-20** Ví MOSO Points, nạp, bảng giá, tự trừ. *(F-24)*
- **FR-21** Kiếm points miễn phí. *(F-25)*
- **FR-22** Trò chơi đoán giá nhà đất. *(F-26)*

### M6 · Môi giới & Đối tác
- **FR-23** Đăng ký tài khoản môi giới (SĐT + OTP, admin duyệt quyền nâng cao). *(F-27, F-53)*
- **FR-24** Danh bạ môi giới & MOSO Score. *(F-28)*
- **FR-25** Nhà đất cần bán nhanh (ký gửi). *(F-29)*
- **FR-26** MOSO Partner cá nhân & doanh nghiệp. *(F-30, F-31)*
- **FR-27** Hoa hồng, theo dõi realtime, Workshop. *(F-32)*
- **FR-28** Cộng tác viên giới thiệu. *(F-33)*
- **FR-29** Khoá học chứng chỉ môi giới. *(F-34)*
- **FR-30** CRM & AI gợi ý khách cho môi giới. *(F-35)*

### M7 · Tài chính & Vay
- **FR-31** Vay thế chấp qua MOSO. *(F-36)*
- **FR-32** Công cụ vay mua nhà & định giá cầm cố. *(F-37, F-38)*

### M8 · Công cụ pháp lý, thuế & đầu tư
- **FR-33** Tính thuế, chi phí giao dịch và chi phí chuyển mục đích. *(F-39, F-41)*
- **FR-34** Bảng giá đất nhà nước. *(F-40)*
- **FR-35** Check quy hoạch (Won't trong đợt này). *(F-42)*
- **FR-36** Bộ công cụ đầu tư: thuê hay mua, lợi nhuận, hiệu quả, mua hay chờ. *(F-43, F-44, F-45, F-46)*
- **FR-37** Tử vi & phong thủy AI. *(F-47)*

### M9 · Nội dung & Dữ liệu thị trường
- **FR-38** Báo cáo & chỉ số thị trường (MPI, Heat Map, thanh khoản). *(F-48, F-49)*
- **FR-39** Tin tức, thuật ngữ, trung tâm trợ giúp. *(F-50, F-51, F-52)*

### M10 · Tài khoản & Ứng dụng
- **FR-40** Đăng nhập, hồ sơ, xoá tài khoản, quyền riêng tư. *(F-53, F-54, F-56)*
- **FR-41** Ứng dụng di động iOS/Android. *(F-55)*

### M11 · Nền tảng AI Agent
- **FR-42** MCP server. *(F-57)*
- **FR-43** API tra cứu/so sánh tin, dự án, môi giới. *(F-58, F-59, F-60)*
- **FR-44** API yêu cầu liên hệ cho agent (thao tác ghi duy nhất). *(F-13, F-57)*
- **FR-45** Đọc trang dạng markdown & các tệp khai báo cho agent. *(F-61, F-62)*

## 7. Yêu cầu phi chức năng

Chi tiết và mục tiêu đo được: `out/SRS.md` §4 (NFR-01…NFR-14). Tóm tắt các mối quan tâm chính:
- **Hiệu năng:** tìm kiếm, bản đồ, AI soạn tin (≤ 30 giây), API agent.
- **Toàn vẹn dữ liệu "3 THẬT":** tỷ lệ xác thực, giá/m² tính đúng, địa chỉ ẩn không bị lộ.
- **Bảo mật & quyền riêng tư:** dữ liệu cá nhân, giấy tờ pháp lý, OTP; tuân thủ C-11.
- **Chống lạm dụng:** rate limit (C-05), chống spam lead.
- **Pháp lý:** công cụ chỉ mang tính tham khảo (C-09); căn cứ văn bản luật (C-10); dữ liệu hành chính sau sáp nhập 2025 (C-08).
- **Khả dụng, đa nền tảng, i18n (vi/en), khả năng tiếp cận.**

## 8. Ràng buộc & tuân thủ

Giữ nguyên C-01…C-13 của brief §7. Các ràng buộc có tác động lớn nhất tới yêu cầu:
- **C-01/C-02:** chu kỳ tin 30 ngày; 1 point = 1.000đ đã gồm VAT; thiếu point thì ẩn số liên hệ.
- **C-05/C-06:** rate limit API; contact là thao tác ghi duy nhất, cần người dùng đồng ý, không được báo "đã chốt lịch".
- **C-08:** sáp nhập hành chính 2025, nên tìm kiếm phải khớp cả tên cũ lẫn tên mới.
- **C-09:** mọi công cụ tính toán phải hiển thị tuyên bố miễn trừ.
- **C-11:** sàn TMĐT đã thông báo Bộ Công Thương.

## 9. Giả định

- [ASSUMPTION] PRD mô tả sản phẩm hiện hữu và trạng thái mục tiêu, không phải greenfield.
- [ASSUMPTION] Web và app dùng chung backend/API; tính năng giống nhau giữa hai nền tảng, trừ khi FR ghi rõ khác.
- [ASSUMPTION] A8 có backoffice (kiểm duyệt, duyệt môi giới, xác nhận lịch, xử lý vay), dù brief không quan sát được.
- [ASSUMPTION] Mục tiêu NFR được đặt theo chuẩn ngành cho marketplace web/mobile tại VN, chưa có số đo thực tế.
- [ASSUMPTION] Tích hợp A10 (ngân hàng, IEM, e-voucher) bước đầu là quy trình bán thủ công/đối tác, chưa phải API.

## 10. Câu hỏi mở

Kế thừa Q-01…Q-12 của brief và bổ sung Q-13…Q-16 (xem `out/SRS.md` §7). Các câu chặn giai đoạn kiến trúc/epic:
- **Q-01** "Xác thực 100%" so với việc vẫn cho đăng tin chưa xác thực → quyết định luồng FR-17.
- **Q-05** Ẩn số nhà là mặc định hay add-on; "khách đã xác thực" được xác thực bằng gì → quyết định FR-18.
- **Q-10** Cơ chế xác thực agent khi MCP "không cần xác thực" → quyết định FR-42/FR-44 và NFR-08.
