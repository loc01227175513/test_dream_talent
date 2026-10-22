# Software Requirements Specification — MOSO.VN

> Theo IEEE 830. Nguồn: `out/brief.md` (Analyst) → PRD `out/bmad/planning-artifacts/prds/prd-test-2026-10-22/prd.md` (PM, headless/fast path). Mọi suy luận không có trong brief được gắn **[ASSUMPTION]**. Mã F-xx, A-x, C-xx, Q-xx là mã của brief.

## 1. Giới thiệu

### 1.1 Mục đích
Đặc tả yêu cầu phần mềm cho nền tảng PropTech BĐS MOSO.VN (web, app iOS/Android, API/MCP cho AI agent). Tài liệu là đầu vào cho các bước kiến trúc, UX, tách epic/story và kiểm thử.

### 1.2 Phạm vi
Sàn giao dịch BĐS theo chuẩn "3 THẬT" (Nhà Thật, Giá Thật, Địa Chỉ Thật), gồm: tìm kiếm & khám phá, liên hệ & lịch xem, đăng tin bằng AI, xác thực & bảo vệ tin, MOSO Points, hệ sinh thái môi giới/đối tác, vay thế chấp, công cụ pháp lý–thuế–đầu tư, dữ liệu thị trường, tài khoản/app và lớp API/MCP cho agent. Ngoài phạm vi: UI backoffice chi tiết, cổng thanh toán cụ thể, AVM thực sự, Check quy hoạch (Won't).

### 1.3 Thuật ngữ
| Thuật ngữ | Nghĩa |
|---|---|
| 3 THẬT | Nhà Thật · Giá Thật · Địa Chỉ Thật |
| ARV | Accurate · Real · Verified — chuẩn dữ liệu tin đăng |
| MP / point | MOSO Point, 1 point = 1.000đ (đã gồm VAT) |
| Ẩn số nhà | Ẩn địa chỉ chi tiết, chỉ hiện cho khách có nhu cầu thật đã xác thực |
| MOSO Score | Điểm xếp hạng môi giới theo 6 yếu tố |
| Partner | Đối tác MOSO (cá nhân/doanh nghiệp) |
| CTV | Cộng tác viên giới thiệu |
| MCP | Model Context Protocol, giao thức tool cho AI agent |
| Lead | Yêu cầu xem nhà/tư vấn ở trạng thái chờ xử lý |
| DTI | Tỷ lệ nợ trên thu nhập |

### 1.4 Tài liệu tham chiếu
- `out/brief.md` — Product Brief MOSO.VN (22/10/2026).
- PRD — `out/bmad/planning-artifacts/prds/prd-test-2026-10-22/prd.md`.
- Luật Đất đai 2024, Luật Nhà ở 2023, Luật KD BĐS 2023, NĐ 103/2024, NĐ 10/2022, TT 85/2019 (C-10).
- IEEE Std 830-1998.

## 2. Mô tả tổng quan

### 2.1 Bối cảnh sản phẩm
MOSO.VN thuộc Công ty TNHH Công nghệ BĐS MOSO (mẹ: Loan Factory), trọng tâm TP.HCM, mở rộng ra Bình Dương, Đồng Nai, Long An, Hà Nội, Đà Nẵng. Quy mô tự công bố: 25.088 tin bán · 26.193 tin cho thuê · 4.791 dự án (số liệu chưa thống nhất, xem Q-02). Hệ thống gồm 11 module (M1–M11) và tương tác với ngân hàng đối tác, IEM, Urbox/Gotit, Cục Thi hành án, App Store/Google Play.

### 2.2 Chức năng chính
Tìm kiếm có xác thực; liên hệ và đặt lịch xem; đăng tin bằng AI; xác thực ARV và Ẩn số nhà; ví points; mạng lưới môi giới/Partner/CTV; vay thế chấp; công cụ tính toán; báo cáo thị trường; API/MCP mở.

### 2.3 Lớp người dùng
| ID | Actor | Đặc điểm |
|---|---|---|
| A1 | Người mua / người thuê | Khách vãng lai hoặc tài khoản thường |
| A2 | Chủ nhà (FSBO) | Đăng tin không qua môi giới, cần đăng nhập |
| A3 | Môi giới cá nhân | Tài khoản SĐT + OTP, có thể là Partner |
| A4 | Doanh nghiệp / Sàn / CĐT | Partner doanh nghiệp |
| A5 | Cộng tác viên | Không cần chứng chỉ |
| A6 | Nhà đầu tư | Quan tâm ROI, BĐS đấu giá |
| A7 | AI agent bên thứ ba | Client máy qua MCP/API |
| A8 | Chuyên viên / Admin MOSO | Nội bộ, có backoffice [ASSUMPTION] |
| A10 | Hệ thống ngoài | Ngân hàng, IEM, e-voucher, THA, app store |

### 2.4 Ràng buộc
C-01…C-13 của brief áp dụng toàn bộ. Quan trọng nhất: chu kỳ tin 30 ngày (C-01); point gồm VAT (C-02); rate limit API (C-05); quy tắc API contact (C-06); location/giá tổng căn (C-07); sáp nhập hành chính 2025 (C-08); công cụ chỉ để tham khảo (C-09); thông báo Bộ Công Thương và cung cấp dữ liệu cho cơ quan tư pháp (C-11); vi-VN là ngôn ngữ chính (C-12).

### 2.5 Giả định & phụ thuộc
- [ASSUMPTION] Sản phẩm đang vận hành; SRS chuẩn hoá trạng thái mục tiêu.
- [ASSUMPTION] Web và app dùng chung backend/API.
- [ASSUMPTION] Có backoffice cho A8 (kiểm duyệt, duyệt môi giới, xác nhận lịch, xử lý vay).
- [ASSUMPTION] Tích hợp ngân hàng/IEM/e-voucher ban đầu là quy trình vận hành, chưa phải API.
- Phụ thuộc dịch vụ bản đồ, SMS OTP, cổng thanh toán, mô hình AI (sinh nội dung, xử lý ảnh) [ASSUMPTION: chưa xác định nhà cung cấp].

## 3. Yêu cầu chức năng

### 3.1 M1 — Tìm kiếm & Khám phá

#### FR-01 Danh sách & lọc tin mua bán/cho thuê
- **Actor:** A1, A6
- **Tiền điều kiện:** không (khách vãng lai được dùng).
- **Luồng chính:** chọn Mua bán/Cho thuê → chọn loại hình (bán: căn hộ, nhà hẻm, nhà mặt tiền, đất; thuê: 9 nhóm), khu vực, khoảng giá, diện tích, PN → tuỳ chọn bật "Tin xác thực"/"Tin có video" → chọn dạng danh sách/lưới → hệ thống trả kết quả phân trang.
- **Tiêu chí chấp nhận:**
  - Given khách chọn "Nhà hẻm" + "Quận 1" + giá ≤ 10 tỷ, When bấm Tìm, Then mọi kết quả đều là nhà hẻm tại Quận 1 có giá ≤ 10 tỷ.
  - Given bật lọc "Tin xác thực", When kết quả hiển thị, Then 100% thẻ tin có badge "Xác thực".
  - Given một thẻ tin, When hiển thị, Then thẻ có giá, giá/m² (tự tính), diện tích, tầng, PN/WC, địa chỉ (theo quyền Ẩn số nhà).
  - Given khu vực nhập theo tên trước sáp nhập 2025, When tìm, Then vẫn trả tin của đơn vị hành chính tương ứng (C-08).
- **Truy vết:** F-01, F-02

#### FR-02 Trang danh mục SEO theo loại hình & khu vực
- **Actor:** A1, công cụ tìm kiếm
- **Tiền điều kiện:** loại hình/khu vực có ít nhất 1 tin đang hiển thị [ASSUMPTION].
- **Luồng chính:** người dùng/crawler mở URL slug (vd. `/mua-ban-nha-hem`, `/ban-nha-quan-1-thanh-pho-ho-chi-minh`) → hệ thống render danh sách đã lọc sẵn kèm tiêu đề/mô tả riêng.
- **Tiêu chí chấp nhận:**
  - Given URL `/cho-thue-phong-tro`, When mở, Then danh sách chỉ gồm tin cho thuê phòng trọ và có thẻ title/meta riêng.
  - Given slug không tồn tại, When mở, Then trả HTTP 404, không trả trang trống mã 200.
- **Truy vết:** F-03

#### FR-03 Bản đồ BĐS
- **Actor:** A1, A6
- **Tiền điều kiện:** tin có toạ độ.
- **Luồng chính:** chuyển sang chế độ bản đồ (`?xem=ban-do`) → ghim hiển thị giá → người dùng vẽ vùng → danh sách lọc theo vùng.
- **Tiêu chí chấp nhận:**
  - Given người dùng vẽ một đa giác, When thả chuột, Then chỉ những tin có toạ độ nằm trong đa giác được liệt kê.
  - Given tin bật Ẩn số nhà và người xem chưa đủ quyền, When hiển thị ghim, Then ghim ở vị trí xấp xỉ [ASSUMPTION: bán kính ≥ 200 m], không lộ số nhà.
- **Truy vết:** F-04, F-22

#### FR-04 Tìm kiếm AI bằng ngôn ngữ tự nhiên
- **Actor:** A1
- **Tiền điều kiện:** không.
- **Luồng chính:** nhập câu (vd. "nhà hẻm Bình Thạnh dưới 5 tỷ 3 phòng ngủ") → AI tách thành bộ lọc có cấu trúc → hiển thị bộ lọc đã suy ra + kết quả + gợi ý BĐS tương tự.
- **Tiêu chí chấp nhận:**
  - Given câu có địa danh, When AI phân tích, Then địa danh được đưa vào `location`, không vào `query` (C-07).
  - Given AI đã suy ra bộ lọc, When kết quả hiển thị, Then người dùng thấy từng bộ lọc dưới dạng chip và xoá/sửa được.
  - Given câu không suy ra được bộ lọc nào, When tìm, Then hệ thống quay về tìm theo từ khoá và báo cho người dùng.
- **Truy vết:** F-05, F-58

#### FR-05 Lưu tin & thông báo tìm kiếm
- **Actor:** A1
- **Tiền điều kiện:** đã đăng nhập.
- **Luồng chính:** bấm lưu tin hoặc lưu bộ tìm kiếm → khi có tin mới khớp bộ lọc, hệ thống gửi thông báo (push/email) [ASSUMPTION: kênh].
- **Tiêu chí chấp nhận:**
  - Given khách chưa đăng nhập bấm "Lưu", When thao tác, Then được chuyển sang đăng nhập và hành động được giữ lại sau khi đăng nhập.
  - Given đã lưu tìm kiếm, When có tin mới khớp được duyệt, Then thông báo gửi trong ≤ 15 phút [ASSUMPTION].
- **Truy vết:** F-06

#### FR-06 Video BĐS
- **Actor:** A1
- **Tiền điều kiện:** tin có video.
- **Luồng chính:** mở video.moso.vn hoặc tab Video trong app → xem dạng feed → bấm sang tin gốc.
- **Tiêu chí chấp nhận:**
  - Given một video, When bấm "Xem tin", Then mở đúng tin gốc.
  - Given tin gốc đã ẩn/đã bán, When video đang trong feed, Then video bị gỡ khỏi feed.
- **Truy vết:** F-07, F-55

#### FR-07 Tra cứu & so sánh dự án sơ cấp
- **Actor:** A1, A6
- **Tiền điều kiện:** không.
- **Luồng chính:** lọc dự án theo loại căn, trạng thái bán, khoảng giá → mở thẻ dự án (trạng thái, số căn, diện tích, CĐT, pháp lý, giá từ) → thêm 2+ dự án vào bảng so sánh.
- **Tiêu chí chấp nhận:**
  - Given lọc giá 2–4 tỷ, When tìm, Then lọc theo giá **tổng căn**, không theo giá/m² (C-07).
  - Given đã thêm ≥ 2 dự án, When mở bảng so sánh, Then mọi dự án được so trên cùng bộ tiêu chí; ô thiếu dữ liệu ghi "Chưa có", không để trống.
- **Truy vết:** F-08, F-09

#### FR-08 Nguồn nhà đặc biệt (MOSO Signature)
- **Actor:** A1, A6, A8
- **Tiền điều kiện:** không.
- **Luồng chính:** xem giỏ hàng đấu giá/phát mãi → khách để lại tiêu chí (tối đa 5 tỉnh, 5 phân khúc giá) + liên hệ → A8 kiểm tra pháp lý và đồng hành đến bàn giao.
- **Tiêu chí chấp nhận:**
  - Given một tin Signature, When hiển thị, Then ghi rõ nguồn (ngân hàng/Thi hành án) và mức chênh so với giá thị trường.
  - Given khách chọn hơn 5 tỉnh, When gửi, Then hệ thống chặn và báo giới hạn.
- **Truy vết:** F-10

### 3.2 M2 — Liên hệ & Giao dịch

#### FR-09 Nhắn tin với người đăng tin
- **Actor:** A1, A2, A3, A8
- **Tiền điều kiện:** đã đăng nhập.
- **Luồng chính:** từ trang tin bấm "Nhắn tin" → mở hội thoại gắn với tin → hai bên trao đổi; chuyên viên có thể tham gia.
- **Tiêu chí chấp nhận:**
  - Given người mua gửi tin nhắn, When người đăng đang online, Then tin nhắn đến trong ≤ 2 giây (NFR-02).
  - Given hội thoại, When mở, Then luôn hiện thẻ tin liên quan ở đầu.
- **Truy vết:** F-11

#### FR-10 Đặt lịch / yêu cầu xem nhà
- **Actor:** A1, A8
- **Tiền điều kiện:** tin đang hiển thị.
- **Luồng chính:** nhập họ tên*, SĐT*, intent (viewing/consult), thời gian mong muốn, lời nhắn → tạo lead "chờ xử lý" → A8 gọi lại xác nhận → nhắc lịch tự động trước giờ hẹn.
- **Tiêu chí chấp nhận:**
  - Given cùng SĐT + cùng tin trong 24h, When gửi lại, Then không tạo lead mới và trả về lead cũ.
  - Given gửi thành công, When hiển thị phản hồi, Then thông báo là "đã gửi yêu cầu", **không** phải "đã chốt lịch".
  - Given SĐT sai định dạng VN, When gửi, Then bị từ chối kèm thông báo lỗi.
  - Given lịch đã xác nhận, When còn 2 giờ trước giờ hẹn [ASSUMPTION], Then gửi nhắc lịch cho người mua.
- **Truy vết:** F-12, F-13

#### FR-11 Hỗ trợ giao dịch & pháp lý
- **Actor:** A1, A2, A8
- **Tiền điều kiện:** đã có lead hoặc đã đăng nhập.
- **Luồng chính:** xem hướng dẫn giao dịch từng bước + checklist pháp lý + mẫu hợp đồng → tuỳ chọn đăng ký dịch vụ nâng cao có phí (xác minh tài liệu, đàm phán).
- **Tiêu chí chấp nhận:**
  - Given khách chọn dịch vụ có phí, When xác nhận, Then hiển thị giá trước khi đặt (Q-11).
  - Given checklist pháp lý, When hiển thị, Then mỗi mục dẫn căn cứ văn bản luật (C-10).
- **Truy vết:** F-14

### 3.3 M3 — Đăng tin & Quản lý tin

#### FR-12 Đăng tin bán/cho thuê bằng AI
- **Actor:** A2, A3
- **Tiền điều kiện:** đã đăng nhập; ví đủ point hoặc có thể nạp.
- **Luồng chính:** chọn Bán/Cho thuê → nhập thông tin cơ bản (loại hình, địa chỉ, diện tích, giá; thuê: giá thuê, chi phí kèm, nội thất, điều kiện) → AI gợi ý tiêu đề, mô tả, bố cục → người đăng sửa, thêm ảnh/pháp lý → gửi duyệt → trừ point theo bảng giá.
- **Tiêu chí chấp nhận:**
  - Given đủ trường bắt buộc, When bấm "AI viết tin", Then bản nháp hiện trong ≤ 30 giây (NFR-03).
  - Given người đăng sửa bản nháp AI, When lưu, Then giữ nguyên nội dung người đăng đã sửa, không bị AI ghi đè.
  - Given tin bán đã xác thực, When đăng, Then trừ 5 point; chưa xác thực thì trừ 8; tin thuê trừ 5 (F-24).
- **Truy vết:** F-15, F-16

#### FR-13 Tin của tôi & gia hạn
- **Actor:** A2, A3
- **Tiền điều kiện:** đã đăng nhập, có ít nhất 1 tin.
- **Luồng chính:** xem danh sách tin → sửa, cập nhật giá, đánh dấu đã bán/đã cho thuê, ẩn tin → hết chu kỳ 30 ngày hệ thống tự gia hạn và trừ point.
- **Tiêu chí chấp nhận:**
  - Given tin đến hạn 30 ngày và ví đủ point, When đến hạn, Then tự gia hạn và ghi giao dịch trừ point.
  - Given ví không đủ point, When đến hạn, Then tin vẫn hiển thị nhưng ẩn số liên hệ (C-01) và chủ tin nhận thông báo.
  - Given đánh dấu "đã bán", When lưu, Then tin rời khỏi kết quả tìm kiếm trong ≤ 5 phút.
- **Truy vết:** F-17, F-24

#### FR-14 Đẩy tin
- **Actor:** A2, A3
- **Tiền điều kiện:** tin đang hiển thị; ví đủ point.
- **Luồng chính:** chọn gói (8 giờ 5.000đ; 24 giờ + Hot 10.000đ; 7 ngày + Hot 50.000đ) → chọn phạm vi (khu vực đăng/toàn tỉnh) → xác nhận → trừ point → tin được ưu tiên trong thời hạn gói.
- **Tiêu chí chấp nhận:**
  - Given tin đã đẩy gói 8 giờ 3 lượt trong ngày, When đẩy lượt thứ 4, Then bị từ chối (C-03).
  - Given gói 24 giờ hoặc 7 ngày, When kích hoạt, Then tin có nhãn "Hot" đến hết hạn gói.
- **Truy vết:** F-18

#### FR-15 Xoá watermark ảnh bằng AI
- **Actor:** A2, A3
- **Tiền điều kiện:** đã đăng nhập.
- **Luồng chính:** tải ảnh lên → AI xoá logo/chữ/SĐT → người dùng tô vùng sót để xoá thêm → so sánh trước/sau → tải từng ảnh hoặc ZIP, hoặc chèn thẳng vào form đăng tin.
- **Tiêu chí chấp nhận:**
  - Given 21 ảnh, ảnh > 10 MB hoặc định dạng khác PNG/JPG/WEBP, When tải lên, Then bị từ chối kèm lý do (C-04).
  - Given ảnh đã xử lý, When mở lịch sử, Then xem và khôi phục được các phiên bản trước.
- **Truy vết:** F-19

#### FR-16 Thống kê tin đăng
- **Actor:** A2, A3
- **Tiền điều kiện:** có tin đang hiển thị.
- **Luồng chính:** mở thống kê tin → xem lượt xem, lượt quan tâm (lưu, nhắn tin, yêu cầu xem) theo thời gian.
- **Tiêu chí chấp nhận:**
  - Given một lượt xem mới, When chủ tin mở thống kê, Then số liệu cập nhật với độ trễ ≤ 60 giây [ASSUMPTION].
- **Truy vết:** F-20

### 3.4 M4 — Xác thực & Bảo vệ tin

#### FR-17 Xác thực tin đăng (ARV)
- **Actor:** A2, A3, A8
- **Tiền điều kiện:** tin đã gửi; người đăng tải giấy tờ chủ sở hữu/pháp lý.
- **Luồng chính:** người đăng gửi giấy tờ (sổ đỏ/sổ hồng) + ảnh thật → A8 kiểm tra chủ sở hữu, pháp lý, đối chiếu quy hoạch, ảnh → đạt thì gắn badge "Xác thực", không đạt thì trả lý do.
- **Tiêu chí chấp nhận:**
  - Given tin đạt cả 3 tiêu chí, When A8 duyệt, Then hiển thị badge "Xác thực" và áp giá 5 point.
  - Given tin bị từ chối, When người đăng mở tin, Then thấy lý do cụ thể và gửi bổ sung được.
  - Given tin chưa xác thực, When hiển thị [ASSUMPTION: vẫn cho đăng, chờ Q-01], Then không có badge và lọc "Tin xác thực" loại bỏ tin đó.
- **Truy vết:** F-21

#### FR-18 Ẩn số nhà
- **Actor:** A2, A3, A1
- **Tiền điều kiện:** chủ tin bật tính năng; ví đủ 5 point/kỳ 30 ngày.
- **Luồng chính:** chủ tin bật Ẩn số nhà → địa chỉ công khai chỉ còn đường/phường → khách có nhu cầu thật đã xác thực [ASSUMPTION: đã xác minh SĐT bằng OTP và có lead với tin] mới thấy địa chỉ đầy đủ.
- **Tiêu chí chấp nhận:**
  - Given khách chưa xác thực, When xem tin, trang SEO, bản đồ hoặc API/MCP, Then không kênh nào trả về số nhà.
  - Given khách đủ điều kiện, When xem tin, Then thấy địa chỉ đầy đủ và lượt mở được ghi log cho chủ tin.
  - Given hết kỳ 30 ngày và ví thiếu point, When gia hạn thất bại, Then chủ tin được thông báo trước khi tính năng tắt [ASSUMPTION].
- **Truy vết:** F-22

#### FR-19 Tiêu chuẩn nội dung & đính chính
- **Actor:** A8
- **Tiền điều kiện:** nội dung biên tập (tin tức, báo cáo) do AI soạn nháp.
- **Luồng chính:** AI soạn nháp → biên tập viên kiểm tra pháp lý/số liệu/nguồn → xuất bản; người đọc gửi đính chính qua email → biên tập viên xử lý.
- **Tiêu chí chấp nhận:**
  - Given bản nháp AI, When chưa có biên tập viên duyệt, Then không thể xuất bản.
  - Given yêu cầu đính chính được chấp nhận, When cập nhật, Then bài hiển thị ghi chú đính chính kèm ngày.
- **Truy vết:** F-23

### 3.5 M5 — MOSO Points & Thanh toán

#### FR-20 Ví MOSO Points & bảng giá
- **Actor:** A2, A3, A4
- **Tiền điều kiện:** đã đăng nhập.
- **Luồng chính:** xem số dư và lịch sử giao dịch → nạp gói (từ 50.000đ) qua cổng thanh toán [ASSUMPTION: Q-08] → point được cộng → hệ thống tự trừ khi đăng/gia hạn/đẩy tin/Ẩn số nhà.
- **Tiêu chí chấp nhận:**
  - Given nạp 50.000đ thành công, When cổng trả callback thành công, Then ví cộng đúng 50 point (C-02) trong ≤ 1 phút.
  - Given bất kỳ giao dịch trừ point nào, When hoàn tất, Then lịch sử ghi lý do, tin liên quan, số dư trước/sau.
  - Given callback thanh toán bị gửi lặp, When xử lý, Then chỉ cộng point một lần (idempotent).
- **Truy vết:** F-24

#### FR-21 Kiếm points miễn phí
- **Actor:** A1, A2, A3
- **Tiền điều kiện:** đã đăng nhập.
- **Luồng chính:** hệ thống cộng point theo sự kiện: quà chào mừng (+30 thường, +100 môi giới), hoàn thiện hồ sơ, tin đầu tiên, mốc tin xác thực, mốc người theo dõi, điểm danh +1/ngày.
- **Tiêu chí chấp nhận:**
  - Given đã điểm danh hôm nay, When điểm danh lần nữa trong cùng ngày, Then không cộng thêm.
  - Given mỗi phần thưởng một lần, When điều kiện đạt lại, Then không cộng lặp.
- **Truy vết:** F-25

#### FR-22 Trò chơi đoán giá nhà đất
- **Actor:** A1
- **Tiền điều kiện:** đã đăng nhập (để tính điểm).
- **Luồng chính:** chơi 5 câu × 20 giây, mỗi câu dùng giá của tin thật → chấm điểm theo % sai lệch → bảng xếp hạng tháng → Top 3 có ≥ 1000 điểm nhận 200/100/50 point.
- **Tiêu chí chấp nhận:**
  - Given đã chơi 5 lượt tính điểm trong ngày, When chơi lượt thứ 6, Then được chơi nhưng không tính điểm (C-13).
  - Given hết tháng, When chốt bảng, Then chỉ người Top 3 có ≥ 1000 điểm được thưởng.
  - Given hết 20 giây, When chưa trả lời, Then câu đó được 0 điểm.
- **Truy vết:** F-26

### 3.6 M6 — Môi giới & Đối tác

#### FR-23 Đăng ký tài khoản môi giới
- **Actor:** A3, A8
- **Tiền điều kiện:** có SĐT VN.
- **Luồng chính:** nhập SĐT → xác thực OTP → hoàn thiện hồ sơ (liên hệ, khu vực hoạt động) → nhận quà chào mừng → yêu cầu quyền nâng cao → A8 duyệt.
- **Tiêu chí chấp nhận:**
  - Given nhập sai OTP 5 lần [ASSUMPTION], When thử lại, Then khoá xác thực 15 phút.
  - Given chưa được A8 duyệt, When truy cập tính năng nâng cao, Then bị chặn kèm trạng thái "Chờ duyệt".
- **Truy vết:** F-27, F-53

#### FR-24 Danh bạ môi giới & MOSO Score
- **Actor:** A1, A3, A7
- **Tiền điều kiện:** không.
- **Luồng chính:** lọc môi giới theo khu vực/thị trường/chỉ đã xác thực → sắp xếp theo MOSO Score (6 yếu tố: hồ sơ, tin xác thực, review, Partner +10đ, tương tác, chứng chỉ).
- **Tiêu chí chấp nhận:**
  - Given bật "Chỉ đã xác thực", When tìm, Then chỉ trả môi giới đã xác thực.
  - Given môi giới mở hồ sơ của mình, When xem MOSO Score, Then thấy điểm từng yếu tố (Q-09).
- **Truy vết:** F-28

#### FR-25 Nhà đất cần bán nhanh (ký gửi)
- **Actor:** A2, A3
- **Tiền điều kiện:** A3 đã đăng nhập.
- **Luồng chính:** chủ nhà ký gửi tin → tin vào kho ký gửi → môi giới duyệt kho, nhận bán → hưởng hoa hồng khi giao dịch thành công.
- **Tiêu chí chấp nhận:**
  - Given môi giới nhận bán một tin, When xác nhận, Then chủ nhà được thông báo và thấy môi giới nào đang phụ trách.
- **Truy vết:** F-29

#### FR-26 MOSO Partner cá nhân & doanh nghiệp
- **Actor:** A3, A4, A8
- **Tiền điều kiện:** có tài khoản môi giới (cá nhân) hoặc thông tin doanh nghiệp.
- **Luồng chính:** đăng ký Partner miễn phí → A8 phản hồi → cá nhân nhận point, nguồn hàng xác thực, kết nối ngân hàng, ưu đãi học phí; doanh nghiệp nhận website chuẩn SEO + trang quản trị nguồn hàng/đội ngũ + đồng bộ giỏ hàng lên MOSO.vn.
- **Tiêu chí chấp nhận:**
  - Given đơn đăng ký Partner gửi trong giờ làm việc, When đến hạn, Then A8 phản hồi trong ≤ 2 giờ.
  - Given doanh nghiệp cập nhật giỏ hàng trên website của mình, When đồng bộ, Then tin xuất hiện trên MOSO.vn trong ≤ 15 phút [ASSUMPTION].
- **Truy vết:** F-30, F-31

#### FR-27 Hoa hồng, theo dõi realtime & Workshop
- **Actor:** A3, A4
- **Tiền điều kiện:** là Partner.
- **Luồng chính:** xem chính sách hoa hồng sơ cấp/thứ cấp → theo dõi tiến độ khách và hoa hồng trên app → đăng ký tham dự Workshop.
- **Tiêu chí chấp nhận:**
  - Given trạng thái giao dịch của khách thay đổi, When A8 cập nhật, Then Partner thấy trạng thái mới trên app trong ≤ 60 giây.
  - Given Workshop đã đủ chỗ, When đăng ký, Then bị từ chối hoặc vào danh sách chờ.
- **Truy vết:** F-32

#### FR-28 Cộng tác viên giới thiệu
- **Actor:** A5, A10
- **Tiền điều kiện:** đã đăng nhập trên mobile.
- **Luồng chính:** gửi nguồn nhà bán/khách hoặc nguồn nhà thuê → A8 xác minh → hợp lệ thì phát e-voucher (100.000đ bán / 10.000đ thuê) qua Urbox/Gotit → CTV theo dõi thưởng realtime.
- **Tiêu chí chấp nhận:**
  - Given nguồn trùng với nguồn đã có trên hệ thống, When gửi, Then bị đánh dấu trùng và không thưởng.
  - Given nguồn được duyệt hợp lệ, When phát thưởng, Then e-voucher đúng mệnh giá hiện trong ví thưởng của CTV.
- **Truy vết:** F-33

#### FR-29 Khoá học chứng chỉ môi giới
- **Actor:** A3, A10 (IEM)
- **Tiền điều kiện:** đã đăng nhập.
- **Luồng chính:** xem khoá 8 buổi → đăng ký (1.990.000đ cho Partner, kèm 2 workshop + gói đăng tin 200K) → hoàn thành → tải chứng chỉ lên → A8 xác thực → +100 point và cộng vào MOSO Score.
- **Tiêu chí chấp nhận:**
  - Given chứng chỉ được xác thực, When duyệt, Then cộng đúng 100 point một lần và yếu tố "chứng chỉ" của MOSO Score được cập nhật.
- **Truy vết:** F-34

#### FR-30 CRM & AI gợi ý khách cho môi giới
- **Actor:** A3
- **Tiền điều kiện:** tài khoản môi giới; có tin đang quản lý. [ASSUMPTION: tính năng đã có trong app, chờ Q-07]
- **Luồng chính:** quản lý danh sách khách, lịch hẹn, hợp đồng → AI gợi ý khách tiềm năng theo danh mục BĐS đang quản lý.
- **Tiêu chí chấp nhận:**
  - Given lead mới gắn với tin của môi giới, When tạo lead, Then lead tự xuất hiện trong CRM của môi giới đó.
  - Given gợi ý AI, When hiển thị, Then mỗi gợi ý ghi lý do khớp (khu vực, giá, loại hình).
- **Truy vết:** F-35

### 3.7 M7 — Tài chính & Vay

#### FR-31 Vay thế chấp qua MOSO
- **Actor:** A3, A1, A8, A10 (ngân hàng)
- **Tiền điều kiện:** Partner đăng nhập [ASSUMPTION: người mua cuối gửi qua Partner, chờ Q-04].
- **Luồng chính:** xem bảng lãi suất 13+ ngân hàng theo tháng → gửi hồ sơ khách → A8 tiếp nhận, phân loại, match ngân hàng, trình hồ sơ → theo dõi trạng thái real-time; phí 0đ.
- **Tiêu chí chấp nhận:**
  - Given hồ sơ gửi trong giờ làm việc, When đến hạn, Then được tiếp nhận và phân loại trong < 30 phút.
  - Given bảng lãi suất, When hiển thị, Then mỗi dòng ghi tháng áp dụng và ngày cập nhật.
  - Given hồ sơ đổi trạng thái, When A8 cập nhật, Then Partner nhận thông báo.
- **Truy vết:** F-36

#### FR-32 Công cụ vay mua nhà & định giá cầm cố
- **Actor:** A1, A6
- **Tiền điều kiện:** không.
- **Luồng chính:** nhập thu nhập, nợ hiện có, lãi suất, kỳ hạn → hệ thống tính khả năng mua tối đa, DTI trước/sau vay, lịch trả góp (dư nợ giảm dần/trả đều); định giá: nhập vị trí, diện tích → ước tính giá trị theo giá rao/m² khu vực ±10% và hạn mức vay theo ngân hàng.
- **Tiêu chí chấp nhận:**
  - Given DTI sau vay > 50%, When tính xong, Then kết quả được đánh dấu cảnh báo.
  - Given vay 1 tỷ, lãi 10%/năm, 12 tháng, trả đều, When tính, Then tổng gốc trong lịch trả bằng đúng 1 tỷ (sai số làm tròn ≤ 1.000đ).
  - Given mọi kết quả, When hiển thị, Then kèm tuyên bố "chỉ mang tính tham khảo" (C-09).
- **Truy vết:** F-37, F-38

### 3.8 M8 — Công cụ pháp lý, thuế & đầu tư

#### FR-33 Tính thuế, chi phí giao dịch & chuyển mục đích
- **Actor:** A1, A2, A6
- **Tiền điều kiện:** không.
- **Luồng chính:** nhập giá giao dịch → tính TNCN 2%, trước bạ 0,5%, công chứng ~0,1%, đăng bộ, tách phần bên bán/bên mua; hoặc nhập thông số thửa đất → ước tính tiền sử dụng đất, trước bạ, phí thẩm định/đo đạc/cấp giấy theo NĐ 103/2024. Có tiện ích Chrome/Firefox.
- **Tiêu chí chấp nhận:**
  - Given giá 5 tỷ, When tính, Then TNCN = 100 triệu (bên bán) và trước bạ = 25 triệu (bên mua).
  - Given mọi kết quả, When hiển thị, Then ghi căn cứ văn bản (C-10) và tuyên bố tham khảo (C-09).
- **Truy vết:** F-39, F-41

#### FR-34 Bảng giá đất nhà nước
- **Actor:** A1, A6
- **Tiền điều kiện:** không.
- **Luồng chính:** chọn tỉnh → huyện → xã → nhóm đất → tên đường → hiển thị đơn giá UBND kèm số quyết định, ngày hiệu lực, link văn bản gốc.
- **Tiêu chí chấp nhận:**
  - Given tỉnh chưa có dữ liệu, When chọn, Then hiện rõ "chưa có dữ liệu", không hiện 0đ.
  - Given một đơn giá, When hiển thị, Then luôn kèm số quyết định và ngày hiệu lực.
- **Truy vết:** F-40

#### FR-35 Check quy hoạch (Won't trong đợt này)
- **Actor:** A1, A6
- **Tiền điều kiện:** —
- **Luồng chính:** giữ trạng thái "Sắp ra mắt"; người dùng đăng ký nhận thông báo khi ra mắt [ASSUMPTION].
- **Tiêu chí chấp nhận:**
  - Given người dùng mở công cụ, When trang hiển thị, Then thấy nhãn "Sắp ra mắt" và không có kết quả quy hoạch giả lập.
- **Truy vết:** F-42

#### FR-36 Bộ công cụ đầu tư
- **Actor:** A1, A6
- **Tiền điều kiện:** không.
- **Luồng chính:** chọn công cụ → nhập tham số → nhận kết quả: thuê hay mua (chi phí ròng theo số năm, tăng giá, chi phí cơ hội); lợi nhuận (gross/net yield, dòng tiền, hoàn vốn; flip ROI, ROI quy năm); hiệu quả đầu tư (BĐS/ngân hàng/chứng khoán/vàng; farmstay); mua hay chờ (điểm 0–100: đà tăng giá 40, lãi vay 40, DTI 20).
- **Tiêu chí chấp nhận:**
  - Given công cụ "mua hay chờ", When tổng điểm được tính, Then nhãn kết quả là MUA, CÂN NHẮC hoặc CHỜ theo ngưỡng [ASSUMPTION: ≥ 70 / 40–69 / < 40].
  - Given giá mua 2 tỷ, tiền thuê 10 triệu/tháng, When tính gross yield, Then kết quả = 6,0%.
  - Given mọi kết quả, When hiển thị, Then kèm tuyên bố tham khảo (C-09).
- **Truy vết:** F-43, F-44, F-45, F-46

#### FR-37 Tử vi & phong thủy AI
- **Actor:** A1
- **Tiền điều kiện:** không.
- **Luồng chính:** nhập năm sinh/mệnh/hướng nhà, SĐT hoặc biển số → AI trả luận giải phong thủy, xem ngày, tử vi, Tarot.
- **Tiêu chí chấp nhận:**
  - Given bất kỳ kết quả nào, When hiển thị, Then ghi rõ "mang tính giải trí/tham khảo".
  - Given SĐT người dùng nhập để xem phong thủy, When xử lý xong, Then không lưu SĐT đó làm lead [ASSUMPTION].
- **Truy vết:** F-47

### 3.9 M9 — Nội dung & Dữ liệu thị trường

#### FR-38 Báo cáo & chỉ số thị trường
- **Actor:** A1, A3, A6, A7
- **Tiền điều kiện:** không (tải bản đầy đủ có thể cần đăng nhập [ASSUMPTION]).
- **Luồng chính:** chọn kỳ (tháng/quý/6 tháng/năm) và khu vực → xem báo cáo từ tin đăng thật, bảng lệch cung–cầu, MOSO Price Index, Heat Map, chỉ số thanh khoản, báo giá theo quận/phường → tải bản đầy đủ.
- **Tiêu chí chấp nhận:**
  - Given số liệu thị trường, When hiển thị, Then ghi thời điểm cập nhật và độ trễ ≤ 1 giờ.
  - Given khu vực sau sáp nhập 2025, When hiển thị cung, Then ghi chú rằng số cung được đếm theo địa chỉ cũ (C-08).
- **Truy vết:** F-48, F-49

#### FR-39 Tin tức, thuật ngữ & trung tâm trợ giúp
- **Actor:** A1, A2, A3
- **Tiền điều kiện:** không.
- **Luồng chính:** đọc tin theo chuyên mục kèm trang tác giả; tra từ điển thuật ngữ theo luật 2023–2024; tìm bài trợ giúp theo chủ đề hoặc gọi hotline 1900 252 307.
- **Tiêu chí chấp nhận:**
  - Given một bài viết, When hiển thị, Then có tác giả, ngày đăng/cập nhật (E-E-A-T).
  - Given một thuật ngữ, When hiển thị, Then dẫn điều luật nguồn.
- **Truy vết:** F-50, F-51, F-52

### 3.10 M10 — Tài khoản & Ứng dụng

#### FR-40 Đăng nhập, hồ sơ, xoá tài khoản & quyền riêng tư
- **Actor:** A1–A5
- **Tiền điều kiện:** —
- **Luồng chính:** đăng nhập (bắt buộc cho đăng tin, đăng ký môi giới, tải ảnh lên công cụ) → quản lý hồ sơ (ảnh, email, Facebook), người theo dõi → xoá tài khoản: Tài khoản → Cài đặt tài khoản → Xoá (3 bước).
- **Tiêu chí chấp nhận:**
  - Given người dùng xoá tài khoản, When xác nhận bước 3, Then hoàn tất trong < 1 phút; tin đang hiển thị bị gỡ; dữ liệu cá nhân xử lý theo NFR-07.
  - Given khách chưa đăng nhập bấm "Đăng tin", When thao tác, Then được chuyển tới đăng nhập.
  - Given thu thập dữ liệu (họ tên, SĐT, email, MST, giấy tờ), When người dùng nhập, Then có liên kết tới chính sách bảo mật.
- **Truy vết:** F-53, F-54, F-56

#### FR-41 Ứng dụng di động iOS/Android
- **Actor:** A1–A5
- **Tiền điều kiện:** cài từ App Store/Google Play (có QR trên web).
- **Luồng chính:** điều hướng qua 5 tab: Tìm nhà, Video, Bản đồ, Đăng tin, Tài khoản.
- **Tiêu chí chấp nhận:**
  - Given người dùng đăng nhập trên app, When mở web cùng tài khoản, Then thấy cùng tin đã lưu, ví point, tin của tôi.
  - Given trang /tai-ung-dung mở trên mobile, When bấm tải, Then chuyển đúng store theo hệ điều hành.
- **Truy vết:** F-55

### 3.11 M11 — Nền tảng AI Agent

#### FR-42 MCP server
- **Actor:** A7
- **Tiền điều kiện:** không cần xác thực (chờ Q-10).
- **Luồng chính:** agent kết nối `/mcp` (Streamable HTTP, JSON-RPC 2.0) → liệt kê tool → gọi search_listings, compare_listings, read_page, search_projects, search_agents, request_contact.
- **Tiêu chí chấp nhận:**
  - Given agent gửi `tools/list`, When server trả lời, Then đủ 6 tool kèm JSON schema tham số.
  - Given tool gọi tới tin bật Ẩn số nhà, When trả kết quả, Then không có số nhà (FR-18).
  - Given vượt rate limit, When gọi tiếp, Then trả lỗi kèm thời gian thử lại (C-05).
- **Truy vết:** F-57

#### FR-43 API tra cứu & so sánh tin, dự án, môi giới
- **Actor:** A7
- **Tiền điều kiện:** không.
- **Luồng chính:** GET `/api/agent/search` (query, location, type, giá, diện tích, PN, propertyType; limit ≤ 20) · `/api/agent/compare` (2–5 tin) · `/api/agent/projects` (unitType, saleStatus, giá tổng căn) · tra môi giới (khu vực, focusMarket, verifiedOnly; top 50 theo MOSO Score); trả JSON hoặc markdown.
- **Tiêu chí chấp nhận:**
  - Given `limit=50`, When gọi search, Then kết quả trả tối đa 20 bản ghi.
  - Given compare với 1 hoặc 6 tin, When gọi, Then trả HTTP 400 kèm thông báo.
  - Given location dùng tên cũ hoặc mới (sáp nhập 2025), When gọi, Then cả hai đều khớp (C-08).
  - Given compare, When tính giá/m², Then chia theo diện tích **đất** (C-07).
  - Given vượt 60 req/phút/IP (search/projects/agents) hoặc 30 (compare), When gọi tiếp, Then trả HTTP 429 + `Retry-After`.
- **Truy vết:** F-58, F-59, F-60

#### FR-44 API yêu cầu liên hệ cho agent
- **Actor:** A7, A8
- **Tiền điều kiện:** người dùng thật đồng ý để lại tên + SĐT (C-06).
- **Luồng chính:** agent gọi `request_contact` / `/api/agent/contact` với tên, SĐT, tin, intent → tạo lead chờ xử lý (như FR-10) → trả mã lead.
- **Tiêu chí chấp nhận:**
  - Given cùng SĐT + tin trong 24h, When gọi lại, Then trả `duplicated: true` và không tạo lead mới.
  - Given gọi thành công, When phản hồi, Then thông điệp không chứa ngữ nghĩa "đã chốt lịch".
  - Given vượt 10 req/phút/IP, When gọi tiếp, Then trả HTTP 429 + `Retry-After`.
- **Truy vết:** F-13, F-57

#### FR-45 Đọc trang dạng markdown & khai báo cho agent
- **Actor:** A7
- **Tiền điều kiện:** không.
- **Luồng chính:** agent gọi `/api/markdown?path=…` hoặc gửi `Accept: text/markdown` tới bất kỳ trang nào → nhận markdown; đọc llms.txt, llms-full.txt, llms-faq.txt, agent-skills index, WebMCP manifest, OpenAPI 3.1, auth.md, sitemap-ai.xml.
- **Tiêu chí chấp nhận:**
  - Given `Accept: text/markdown`, When gọi một trang danh sách, Then trả `Content-Type: text/markdown` và kích thước ≤ 10% bản HTML.
  - Given OpenAPI 3.1, When kiểm bằng trình validator chuẩn, Then hợp lệ và mô tả mọi endpoint của FR-43/FR-44.
- **Truy vết:** F-61, F-62

## 4. Yêu cầu phi chức năng

Mọi mục tiêu đều là **[ASSUMPTION]** cho đến khi có đo đạc thực tế, trừ các mục trích ràng buộc của brief.

| ID | Nhóm | Yêu cầu | Mục tiêu đo được | Áp dụng |
|---|---|---|---|---|
| NFR-01 | Hiệu năng | Thời gian phản hồi tìm kiếm/danh sách/bản đồ | p95 ≤ 800 ms phía server; LCP trang danh sách ≤ 2,5 s trên 4G | FR-01–FR-07 |
| NFR-02 | Hiệu năng | Độ trễ tin nhắn trong ứng dụng | p95 ≤ 2 s đầu-cuối | FR-09 |
| NFR-03 | Hiệu năng | AI soạn tin | p95 ≤ 30 s; tỷ lệ lỗi ≤ 2% | FR-12 |
| NFR-04 | Hiệu năng | API agent | p95 ≤ 1 s với limit=20; markdown ≤ 10% kích thước HTML | FR-42–FR-45 |
| NFR-05 | Khả dụng | Uptime web, app API, API agent | ≥ 99,5%/tháng; RPO ≤ 1 h, RTO ≤ 4 h | Toàn hệ thống |
| NFR-06 | Toàn vẹn dữ liệu | Tính đúng giá/m² và công thức công cụ | 100% test vectors đạt; giá/m² = giá ÷ diện tích đất | FR-01, FR-32, FR-33, FR-36, FR-43 |
| NFR-07 | Bảo mật & riêng tư | Dữ liệu cá nhân, giấy tờ pháp lý | TLS 1.2+; mã hoá khi lưu trữ (AES-256) giấy tờ pháp lý; xoá/ẩn danh dữ liệu cá nhân ≤ 30 ngày sau khi xoá tài khoản, trừ dữ liệu luật yêu cầu lưu (C-11) | FR-17, FR-23, FR-40 |
| NFR-08 | Chống lạm dụng | Rate limit & spam lead | Đúng C-05 (60/30/10 req/phút/IP, HTTP 429 + Retry-After); lead trùng 24h = 0; lead spam ≤ 5% tổng lead qua API | FR-10, FR-42–FR-44 |
| NFR-09 | Bảo vệ "Địa Chỉ Thật" | Không lộ số nhà khi bật Ẩn số nhà | 0 rò rỉ qua mọi kênh (web, app, SEO, bản đồ, API, MCP, markdown), kiểm bằng test tự động mỗi bản phát hành | FR-03, FR-18, FR-42–FR-45 |
| NFR-10 | Chất lượng dữ liệu | Tỷ lệ tin xác thực & trùng lặp | ≥ 95% tin hiển thị có badge; tin trùng ≤ 2%; SLA duyệt xác thực ≤ 24 h làm việc | FR-17 |
| NFR-11 | Tài chính | Tính đúng giao dịch point | 0 sai lệch số dư khi đối soát ngày; callback idempotent | FR-13, FR-14, FR-20–FR-22 |
| NFR-12 | Pháp lý | Tuyên bố miễn trừ & căn cứ | 100% màn hình kết quả công cụ có tuyên bố C-09; 100% đơn giá đất có số quyết định | FR-32–FR-37 |
| NFR-13 | Khả năng tiếp cận & i18n | WCAG, ngôn ngữ | WCAG 2.1 AA cho luồng tìm, xem, liên hệ, đăng tin; vi-VN đầy đủ, en cho trang chính (C-12) | Web, app |
| NFR-14 | Tương thích | Nền tảng hỗ trợ | 2 phiên bản mới nhất của Chrome/Safari/Firefox/Edge; iOS ≥ 16, Android ≥ 10 | FR-41 |

## 5. Epics & User Stories

Ưu tiên MoSCoW. **[ASSUMPTION]** MVP/phát hành đầu = toàn bộ Must.

| Epic | Tên | MoSCoW | FR |
|---|---|---|---|
| E1 | Tìm kiếm & khám phá có xác thực | **Must** | FR-01–FR-08 |
| E2 | Liên hệ, lịch xem & hỗ trợ giao dịch | **Must** | FR-09–FR-11 |
| E3 | Đăng tin & quản lý tin | **Must** | FR-12–FR-16 |
| E4 | Xác thực "3 THẬT" & bảo vệ tin | **Must** | FR-17–FR-19 |
| E5 | MOSO Points & thanh toán | **Must** | FR-20, FR-21 |
| E11 | Tài khoản & ứng dụng di động | **Must** | FR-40, FR-41 |
| E6 | Hệ sinh thái môi giới & đối tác | **Should** | FR-23–FR-30 |
| E7 | Tài chính & vay mua nhà | **Should** | FR-31, FR-32 |
| E10 | Nền tảng AI Agent (API/MCP) | **Should** | FR-42–FR-45 |
| E8 | Công cụ pháp lý, thuế & đầu tư | **Could** | FR-33, FR-34, FR-36, FR-37 |
| E9 | Nội dung, dữ liệu thị trường & tương tác | **Could** | FR-22, FR-38, FR-39 |
| — | Check quy hoạch | **Won't** (đợt này) | FR-35 |

Lưu ý: E7 và E10 xếp Should dù là điểm khác biệt chiến lược (brief §3). Lý do: vòng lõi marketplace phải chạy trước. **[ASSUMPTION]** PM có thể nâng E10 lên Must nếu kênh agent là mục tiêu tăng trưởng chính (Q-12).

### E1 — Tìm kiếm & khám phá có xác thực (Must)
- **US-1.1** Là người mua, tôi muốn lọc theo loại hình, khu vực, giá và chỉ xem tin xác thực để không mất thời gian với tin ảo. *(FR-01)*
- **US-1.2** Là người mua, tôi muốn gõ một câu tự nhiên và thấy bộ lọc AI đã hiểu để tìm nhanh hơn. *(FR-04)*
- **US-1.3** Là người mua, tôi muốn xem giá trên bản đồ và vẽ vùng để tìm quanh nơi làm việc. *(FR-03)*
- **US-1.4** Là người mua, tôi muốn lưu tìm kiếm và nhận thông báo để không bỏ lỡ tin mới. *(FR-05)*
- **US-1.5** Là nhà đầu tư, tôi muốn so sánh dự án và xem nguồn nhà đấu giá để chọn cơ hội tốt. *(FR-07, FR-08)*
- **US-1.6** Là người mua, tôi muốn xem video tin đăng để đánh giá nhà trước khi đi xem. *(FR-06)*
- **US-1.7** Là MOSO, tôi muốn có trang danh mục SEO theo loại hình/khu vực để thu hút lưu lượng tự nhiên. *(FR-02)*

### E2 — Liên hệ, lịch xem & hỗ trợ giao dịch (Must)
- **US-2.1** Là người mua, tôi muốn đặt lịch xem nhà và được chuyên viên gọi xác nhận. *(FR-10)*
- **US-2.2** Là người mua, tôi muốn nhắn tin với người đăng ngay trong app. *(FR-09)*
- **US-2.3** Là người mua, tôi muốn có checklist pháp lý và mẫu hợp đồng để giao dịch an toàn. *(FR-11)*

### E3 — Đăng tin & quản lý tin (Must)
- **US-3.1** Là chủ nhà, tôi muốn AI viết tin trong 30 giây để đăng nhanh. *(FR-12)*
- **US-3.2** Là chủ nhà, tôi muốn sửa giá, đánh dấu đã bán và để tin tự gia hạn. *(FR-13)*
- **US-3.3** Là môi giới, tôi muốn đẩy tin để tăng hiển thị. *(FR-14)*
- **US-3.4** Là môi giới, tôi muốn xoá watermark ảnh để đăng ảnh sạch. *(FR-15)*
- **US-3.5** Là chủ nhà, tôi muốn xem lượt xem và lượt quan tâm của tin. *(FR-16)*

### E4 — Xác thực "3 THẬT" & bảo vệ tin (Must)
- **US-4.1** Là chủ nhà, tôi muốn được xác thực tin để có badge và trả ít point hơn. *(FR-17)*
- **US-4.2** Là chủ nhà, tôi muốn ẩn số nhà để tránh bị sao chép và cướp khách. *(FR-18)*
- **US-4.3** Là biên tập viên, tôi muốn mọi nội dung AI soạn được duyệt trước khi xuất bản. *(FR-19)*

### E5 — MOSO Points & thanh toán (Must)
- **US-5.1** Là môi giới, tôi muốn nạp point và xem lịch sử trừ point minh bạch. *(FR-20)*
- **US-5.2** Là người dùng, tôi muốn kiếm point miễn phí qua nhiệm vụ và điểm danh. *(FR-21)*

### E11 — Tài khoản & ứng dụng di động (Must)
- **US-11.1** Là người dùng, tôi muốn đăng nhập và quản lý hồ sơ; xoá tài khoản trong dưới 1 phút. *(FR-40)*
- **US-11.2** Là người dùng, tôi muốn dùng app với dữ liệu đồng bộ cùng web. *(FR-41)*

### E6 — Hệ sinh thái môi giới & đối tác (Should)
- **US-6.1** Là môi giới, tôi muốn đăng ký bằng SĐT + OTP và được duyệt quyền nâng cao. *(FR-23)*
- **US-6.2** Là người mua, tôi muốn tìm môi giới đã xác thực theo MOSO Score. *(FR-24)*
- **US-6.3** Là môi giới, tôi muốn nhận bán tin ký gửi chính chủ. *(FR-25)*
- **US-6.4** Là doanh nghiệp, tôi muốn có website miễn phí và đồng bộ giỏ hàng lên MOSO. *(FR-26)*
- **US-6.5** Là Partner, tôi muốn theo dõi hoa hồng realtime và đăng ký Workshop. *(FR-27)*
- **US-6.6** Là CTV, tôi muốn gửi nguồn và nhận e-voucher. *(FR-28)*
- **US-6.7** Là môi giới, tôi muốn học và xác thực chứng chỉ để tăng điểm. *(FR-29)*
- **US-6.8** Là môi giới, tôi muốn CRM và AI gợi ý khách tiềm năng. *(FR-30)*

### E7 — Tài chính & vay mua nhà (Should)
- **US-7.1** Là Partner, tôi muốn gửi hồ sơ vay cho khách và theo dõi real-time, phí 0đ. *(FR-31)*
- **US-7.2** Là người mua, tôi muốn biết khả năng vay, DTI và lịch trả góp. *(FR-32)*

### E10 — Nền tảng AI Agent (Should)
- **US-10.1** Là AI agent, tôi muốn tìm và so sánh tin qua MCP/API có schema rõ ràng. *(FR-42, FR-43)*
- **US-10.2** Là AI agent, tôi muốn gửi yêu cầu xem nhà thay người dùng khi họ đồng ý. *(FR-44)*
- **US-10.3** Là AI agent, tôi muốn đọc trang dạng markdown để tiết kiệm token. *(FR-45)*

### E8 — Công cụ pháp lý, thuế & đầu tư (Could)
- **US-8.1** Là người bán/mua, tôi muốn biết thuế phí từng bên. *(FR-33)*
- **US-8.2** Là người mua, tôi muốn tra bảng giá đất nhà nước kèm văn bản gốc. *(FR-34)*
- **US-8.3** Là nhà đầu tư, tôi muốn tính yield, ROI và có gợi ý mua hay chờ. *(FR-36)*
- **US-8.4** Là người mua, tôi muốn xem phong thủy nhà theo mệnh. *(FR-37)*

### E9 — Nội dung, dữ liệu thị trường & tương tác (Could)
- **US-9.1** Là nhà đầu tư, tôi muốn xem báo cáo, MPI và Heat Map theo khu vực. *(FR-38)*
- **US-9.2** Là người dùng, tôi muốn đọc tin tức, tra thuật ngữ, tìm trợ giúp. *(FR-39)*
- **US-9.3** Là người dùng, tôi muốn chơi đoán giá để học giá thị trường và nhận point. *(FR-22)*

## 6. Ma trận truy vết

| Feature (brief) | FR | Epic |
|---|---|---|
| F-01, F-02 | FR-01 | E1 |
| F-03 | FR-02 | E1 |
| F-04 | FR-03 | E1 |
| F-05 | FR-04 | E1 |
| F-06 | FR-05 | E1 |
| F-07 | FR-06 | E1 |
| F-08, F-09 | FR-07 | E1 |
| F-10 | FR-08 | E1 |
| F-11 | FR-09 | E2 |
| F-12 | FR-10 | E2 |
| F-13 | FR-10, FR-44 | E2, E10 |
| F-14 | FR-11 | E2 |
| F-15, F-16 | FR-12 | E3 |
| F-17 | FR-13 | E3 |
| F-18 | FR-14 | E3 |
| F-19 | FR-15 | E3 |
| F-20 | FR-16 | E3 |
| F-21 | FR-17 | E4 |
| F-22 | FR-18, FR-03 | E4, E1 |
| F-23 | FR-19 | E4 |
| F-24 | FR-20, FR-13 | E5, E3 |
| F-25 | FR-21 | E5 |
| F-26 | FR-22 | E9 |
| F-27 | FR-23 | E6 |
| F-28 | FR-24 | E6 |
| F-29 | FR-25 | E6 |
| F-30, F-31 | FR-26 | E6 |
| F-32 | FR-27 | E6 |
| F-33 | FR-28 | E6 |
| F-34 | FR-29 | E6 |
| F-35 | FR-30 | E6 |
| F-36 | FR-31 | E7 |
| F-37, F-38 | FR-32 | E7 |
| F-39, F-41 | FR-33 | E8 |
| F-40 | FR-34 | E8 |
| F-42 | FR-35 | Won't |
| F-43, F-44, F-45, F-46 | FR-36 | E8 |
| F-47 | FR-37 | E8 |
| F-48, F-49 | FR-38 | E9 |
| F-50, F-51, F-52 | FR-39 | E9 |
| F-53 | FR-40, FR-23 | E11, E6 |
| F-54, F-56 | FR-40 | E11 |
| F-55 | FR-41, FR-06 | E11, E1 |
| F-57 | FR-42, FR-44 | E10 |
| F-58 | FR-43, FR-04 | E10, E1 |
| F-59, F-60 | FR-43 | E10 |
| F-61, F-62 | FR-45 | E10 |

Độ phủ: 62/62 feature của brief được ít nhất 1 FR truy vết; 45/45 FR truy vết về ít nhất 1 feature.

## 7. Câu hỏi mở

| # | Câu hỏi | Ảnh hưởng | Chặn giai đoạn? |
|---|---|---|---|
| Q-01 | "Xác thực 100%" so với việc vẫn đăng được tin chưa xác thực (8 MP); báo cáo ghi 91% | FR-17, NFR-10 | **Có** — kiến trúc luồng kiểm duyệt |
| Q-02 | Số liệu quy mô không thống nhất (tin, môi giới, người dùng) | Baseline chỉ số PRD §3 | Không |
| Q-03 | Quà point cho môi giới/Partner: +100, 200 hay tới 1.000? | FR-21, FR-26 | Không |
| Q-04 | Vay thế chấp dành cho Partner hay cả người mua cuối; 1 hay 13+ ngân hàng? | FR-31 | Không |
| Q-05 | Ẩn số nhà mặc định hay add-on 5 point; "khách đã xác thực" được xác thực bằng gì? | FR-18, NFR-09 | **Có** — UX & kiến trúc quyền xem |
| Q-06 | Có AVM thực sự hay chỉ giá rao/m² ±10%? | FR-32 | Không |
| Q-07 | CRM, AI gợi ý khách, analytics, nhắc lịch đã có trên sản phẩm chưa? | FR-16, FR-30, FR-10 | Không |
| Q-08 | Cổng thanh toán nạp point là gì; có hoàn tiền không? | FR-20, NFR-11 | Không (chặn khi triển khai E5) |
| Q-09 | Công thức đầy đủ của MOSO Score | FR-24 | Không |
| Q-10 | Xác thực agent qua auth.md so với MCP "không cần xác thực" | FR-42, FR-44, NFR-08 | **Có** — kiến trúc bảo mật lớp agent |
| Q-11 | Bảng giá dịch vụ nâng cao có phí | FR-11 | Không |
| Q-12 | Mô hình doanh thu chính (phí tin, hoa hồng, hoa hồng vay, Signature) | MoSCoW E7/E10 | Không |
| Q-13 | Ngưỡng điểm MUA/CÂN NHẮC/CHỜ của công cụ "mua hay chờ" [ASSUMPTION ≥70/40–69/<40] | FR-36 | Không |
| Q-14 | Bán kính làm mờ vị trí ghim khi bật Ẩn số nhà [ASSUMPTION ≥ 200 m] | FR-03, FR-18 | Không |
| Q-15 | Thời hạn lưu trữ dữ liệu cá nhân sau khi xoá tài khoản theo luật VN [ASSUMPTION 30 ngày] | NFR-07 | Không |
| Q-16 | Kênh thông báo cho lưu tìm kiếm/nhắc lịch (push, SMS, email, Zalo?) | FR-05, FR-10 | Không |
