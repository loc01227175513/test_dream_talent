# Software Requirements Specification — MOSO.vn
**Phiên bản:** 1.0 (reverse-engineered) · **Ngày:** 22/10/2026 · **Phương pháp:** BMAD (Analyst → PM → Architect) + Understand-Anything knowledge graph · **Đầu vào:** [brief.md](brief.md)

---

## 1. Giới thiệu
### 1.1 Mục đích
Tài liệu đặc tả yêu cầu phần mềm cho nền tảng AI Proptech MOSO.vn, được dựng ngược từ hệ thống đang vận hành, dùng làm baseline cho giai đoạn Planning (ước lượng, roadmap, kiểm thử chấp nhận).

### 1.2 Phạm vi
MOSO là sàn giao dịch BĐS trực tuyến (web Next.js + app iOS/Android) cho mua bán, cho thuê, dự án, môi giới, vay mua nhà và dữ liệu thị trường, vận hành theo nguyên tắc **"3 THẬT": Nhà Thật – Giá Thật – Địa Chỉ Thật**. Ngoài phạm vi: core banking của ngân hàng đối tác, hệ thống thi chứng chỉ của IEM, nền tảng e-voucher Urbox/Gotit.

### 1.3 Thuật ngữ
| Thuật ngữ | Định nghĩa |
|---|---|
| MP / MOSO Points | Đơn vị thanh toán nội bộ, 1 MP = 1.000đ (đã gồm VAT) |
| Tin xác thực | Tin đã kiểm tra ảnh, pháp lý, chính chủ |
| Ẩn số nhà | Tính năng che số nhà/địa chỉ chi tiết với người xem chưa đủ điều kiện |
| Đẩy tin | Gói ưu tiên hiển thị có thời hạn |
| MOSO Score | Điểm xếp hạng môi giới trong danh bạ |
| MOSO Signature | Giỏ hàng BĐS đấu giá / phát mãi |
| DTI | Debt-to-Income: tỷ lệ nợ trên thu nhập |
| AVM | Automated Valuation Model |
| FSBO | For Sale By Owner — chủ nhà tự bán |
| MCP | Model Context Protocol — giao thức cho AI agent |

### 1.4 Tài liệu tham chiếu
llms.txt, /.well-known/mcp.json, /bang-gia-dang-tin, /chinh-sach-moso-points, /chinh-sach-bao-mat, Luật Đất đai 2024, Luật Nhà ở 2023, Luật KD BĐS, NĐ 103/2024/NĐ-CP, NĐ 13/2023/NĐ-CP (bảo vệ dữ liệu cá nhân).

---

## 2. Mô tả tổng quan
### 2.1 Bối cảnh sản phẩm
```
 Người mua/thuê ─┐                       ┌─ Ngân hàng đối tác (13+)
 Chủ nhà ────────┤                       ├─ IEM (đào tạo chứng chỉ)
 Môi giới ───────┼──► MOSO Web / App ◄──►├─ Urbox / Gotit (e-voucher)
 Doanh nghiệp ───┤      │                ├─ Cổng thanh toán (giả định)
 CTV ────────────┘      │                └─ SMS OTP (giả định)
 AI Agent ───► MCP / Agent API / Markdown
```

### 2.2 Lớp người dùng
| Actor | Mô tả | Quyền |
|---|---|---|
| A1 Khách (Guest) | Chưa đăng nhập | Tìm, xem, dùng công cụ, gửi yêu cầu xem nhà |
| A1' Người dùng | Đã đăng nhập bằng SĐT | + lưu, nhắn tin, chơi game, nhận points |
| A2 Chủ nhà | Người dùng đăng tin | + đăng/quản lý tin, nạp points |
| A3 Môi giới | Tài khoản môi giới | + hồ sơ danh bạ, nhận ký gửi, Partner |
| A4 Doanh nghiệp | Sàn/công ty BĐS | + website, quản trị đội ngũ, đồng bộ tin |
| A5 CTV | Bất kỳ ai | Gửi nguồn nhà/khách, nhận e-voucher |
| A6 AI Agent | Client máy | Đọc dữ liệu công khai, 1 thao tác ghi (contact) |
| A7 Admin/Chuyên viên | Nội bộ | Xác thực tin, duyệt môi giới, xử lý lead, phản ánh |

### 2.3 Ràng buộc
- C-01: Tuân thủ quy định sàn TMĐT (đã thông báo Bộ Công Thương), phải có quy chế hoạt động, cơ chế giải quyết tranh chấp.
- C-02: Dữ liệu cá nhân theo NĐ 13/2023; người dùng có quyền xoá tài khoản.
- C-03: Địa giới hành chính phải hỗ trợ cả tên trước và sau sáp nhập 2025.
- C-04: Mọi kết quả công cụ tài chính/pháp lý phải gắn nhãn "tham khảo", không phải khuyến nghị đầu tư.
- C-05: Tiếng Việt là ngôn ngữ chính, tiếng Anh phụ.

### 2.4 Giả định & phụ thuộc
- D-01 *(giả định)* OTP gửi qua nhà cung cấp SMS bên thứ ba.
- D-02 *(giả định)* Nạp points qua cổng thanh toán nội địa (VNPay/MoMo…).
- D-03 Lãi suất ngân hàng cập nhật hàng tháng từ đối tác.
- D-04 Bảng giá đất nhập dần theo từng tỉnh từ văn bản gốc UBND.

---

## 3. Yêu cầu chức năng

> Định dạng: **FR-xx** · Actor · Tiền điều kiện · Luồng chính · Acceptance Criteria (AC) · Truy vết.

### 3.1 Module M1 — Tìm kiếm & Khám phá

#### FR-01 Tìm kiếm & lọc tin đăng
- **Actor:** A1 · **Tiền điều kiện:** không
- **Luồng:** chọn Bán/Thuê → chọn loại hình, khu vực (tỉnh/quận/phường), khoảng giá, diện tích, số PN → hệ thống trả danh sách sắp xếp mới nhất, phân trang.
- **AC:**
  - Given khách chọn "Nhà hẻm" + "Quận 1" + giá ≤ 10 tỷ, When bấm Tìm, Then mọi kết quả đều là nhà hẻm tại Quận 1 có giá ≤ 10 tỷ.
  - Given bật bộ lọc "Tin xác thực", Then chỉ hiện tin có badge xác thực.
  - Given khu vực nhập theo tên cũ (trước sáp nhập 2025), Then vẫn trả đúng tin thuộc đơn vị mới.
- **Truy vết:** F-01, F-02, F-05

#### FR-02 Tìm kiếm bằng AI (ngôn ngữ tự nhiên)
- **Actor:** A1 · **Luồng:** nhập câu ("nhà hẻm Bình Thạnh dưới 5 tỷ 3 phòng ngủ") → AI tách thành bộ lọc có cấu trúc → hiển thị bộ lọc đã hiểu + kết quả.
- **AC:**
  - Given câu chứa địa danh, Then địa danh được đưa vào trường `location`, không vào `query` (tránh khớp nhầm Bình Thạnh → Bình Tân).
  - Then người dùng thấy và sửa được bộ lọc AI đã suy ra.
- **Truy vết:** F-03

#### FR-03 Xem trên bản đồ
- **Actor:** A1 · **Luồng:** chuyển `?xem=ban-do` → ghim hiển thị giá → người dùng vẽ đa giác → danh sách lọc theo vùng.
- **AC:** Given vẽ vùng, Then chỉ tin có toạ độ trong đa giác được liệt kê; Given tin bật Ẩn số nhà, Then ghim hiển thị vị trí xấp xỉ, không lộ số nhà.
- **Truy vết:** F-04, F-16

#### FR-04 Chi tiết tin đăng
- **Actor:** A1 · **Luồng:** mở tin → ảnh (gallery), video, giá, giá/m², diện tích, tầng, PN/WC, pháp lý, địa chỉ, người đăng, nút liên hệ/đặt lịch.
- **AC:** giá/m² = giá ÷ diện tích **đất**; số tầng luôn hiển thị cạnh giá/m²; badge "xác thực" khi FR-15 đạt.
- **Truy vết:** F-06

#### FR-05 Tra cứu & so sánh dự án
- **Actor:** A1 · **Luồng:** lọc dự án theo loại căn, trạng thái bán (upcoming/booking_open/open/delivered/closed), khoảng giá căn → chọn 2–5 dự án → bảng so sánh cùng tiêu chí (pháp lý, tiến độ, chủ đầu tư, giá).
- **AC:** minUnitPrice/maxUnitPrice lọc theo giá **tổng căn**, không theo m².
- **Truy vết:** F-07

#### FR-06 Nguồn nhà đặc biệt (MOSO Signature)
- **Actor:** A1, A3 · **Luồng:** xem giỏ hàng đấu giá/phát mãi → chi tiết pháp lý đã xác minh → đăng ký tư vấn + vay.
- **AC:** mỗi tin hiển thị nguồn (ngân hàng / Thi Hành Án) và chênh lệch so với giá thị trường.
- **Truy vết:** F-08

#### FR-07 Gửi yêu cầu xem nhà / tư vấn
- **Actor:** A1, A6 · **Luồng:** nhập tên*, SĐT*, (tin, intent=viewing|consult, thời gian mong muốn, email, lời nhắn) → tạo lead trạng thái *chờ xử lý* → chuyên viên gọi lại xác nhận → nhắc lịch tự động.
- **AC:**
  - Given cùng SĐT + cùng tin trong 24h, Then trả lại lead cũ với `duplicated: true`, không tạo bản ghi mới.
  - Then thông báo cho người dùng là "đã gửi yêu cầu", **không** được nói "đã chốt lịch".
  - Given SĐT sai định dạng VN, Then từ chối với thông báo lỗi.
- **Truy vết:** F-09, F-45

### 3.2 Module M2 — Đăng tin

#### FR-08 Đăng tin với AI
- **Actor:** A2, A3 · **Tiền điều kiện:** đã đăng nhập, đủ points
- **Luồng:** chọn Bán/Cho thuê → nhập loại BĐS, địa chỉ, diện tích, giá, pháp lý, PN/WC, ảnh → AI sinh tiêu đề + mô tả → người dùng duyệt/sửa → xác nhận → trừ points → tin hiển thị 30 ngày.
- **AC:**
  - AI trả bản nháp tiêu đề + mô tả trong ≤ 30 giây (P95).
  - Form cho thuê có trường chi phí kèm (điện, nước, phí quản lý), nội thất, điều kiện thuê.
  - Given số dư < phí, Then chặn đăng và gợi ý nạp/kiếm points.
  - Tài khoản mới đủ points đăng tin đầu tiên miễn phí.
- **Truy vết:** F-10, F-17

#### FR-09 Quản lý tin của tôi
- **Actor:** A2, A3 · **Luồng:** danh sách tin → sửa, cập nhật giá, đánh dấu đã bán/đã thuê, ẩn, xem analytics (lượt xem, lượt quan tâm).
- **AC:** Given tin hết 30 ngày, Then hệ thống tự trừ points gia hạn; Given không đủ points, Then tin bị **ẩn số liên hệ** (không xoá).
- **Truy vết:** F-11, F-17

#### FR-10 Đẩy tin
- **Actor:** A2, A3 · **Luồng:** chọn tin → chọn gói (8h 5k · 24h 10k + Hot · 7 ngày 50k + Hot) → chọn phạm vi (khu vực / toàn tỉnh) → thanh toán points.
- **AC:** gói 8h tối đa 3 lượt/tin/ngày; nhãn "Hot" hiển thị đúng thời hạn gói; hết hạn tự gỡ ưu tiên.
- **Truy vết:** F-12

#### FR-11 Xoá watermark ảnh bằng AI
- **Actor:** A1' (yêu cầu đăng nhập) · **Luồng:** tải ≤ 20 ảnh (PNG/JPG/WEBP, ≤ 10MB/ảnh) → AI xoá logo/chữ/SĐT → người dùng tô vùng còn sót → so sánh trước/sau, quay lại phiên bản cũ → tải từng ảnh hoặc ZIP.
- **AC:** ảnh tải về giữ nguyên kích thước, định dạng, tên file gốc; file > 10MB hoặc > 20 ảnh bị từ chối kèm thông báo; nút xoá watermark có sẵn trong form đăng tin.
- **Truy vết:** F-13

#### FR-12 Ký gửi & nhà cần bán nhanh
- **Actor:** A2 ký gửi, A3 nhận bán · **Luồng:** chủ nhà ký gửi → admin xác thực → tin vào `/nha-dat-can-ban-nhanh` → môi giới trong khu vực nhận bán, hưởng hoa hồng.
- **AC:** chỉ môi giới đã hoàn thiện hồ sơ + khu vực hoạt động phù hợp mới thấy nút "Nhận bán".
- **Truy vết:** F-14, F-19

### 3.3 Module M3 — Xác thực & Bảo vệ

#### FR-13 Xác thực tin "3 THẬT"
- **Actor:** A2 gửi, A7 duyệt · **Luồng:** chủ tin gửi giấy tờ pháp lý + ảnh thật + vị trí ghim → chuyên viên/AI kiểm tra chính chủ, pháp lý, ảnh không trùng → gắn badge.
- **AC:** Given tin được xác thực, Then phí đăng/gia hạn bán giảm 8 → 5 MP; Given ảnh trùng tin khác, Then từ chối với lý do; SLA xác minh ≤ 24h.
- **Truy vết:** F-15

#### FR-14 Ẩn số nhà
- **Actor:** A2, A3 bật; A1 xem · **Luồng:** bật tuỳ chọn (5 MP/30 ngày) → địa chỉ hiển thị dạng "đường, phường" → người xem đủ điều kiện (đăng nhập + xác thực SĐT *(giả định)*) mới thấy số nhà.
- **AC:** số nhà không xuất hiện trong HTML, markdown, API, sitemap hay bản đồ đối với người xem chưa đủ điều kiện; mỗi lần mở địa chỉ được ghi log.
- **Truy vết:** F-16

### 3.4 Module M4 — MOSO Points

#### FR-15 Ví & giao dịch points
- **Actor:** A1'–A4 · **Luồng:** xem số dư, lịch sử cộng/trừ; nạp gói từ 50.000đ.
- **AC:** mọi giao dịch có bút toán đối ứng (không âm số dư); phí khớp bảng giá công bố; giá hiển thị đã gồm VAT.
- **Truy vết:** F-17

#### FR-16 Kiếm points miễn phí
- **Actor:** A1'–A3 · **Luồng:** nhận quà chào mừng (+30, môi giới +100), điểm danh +1/ngày, hoàn thiện hồ sơ +30, nhiệm vụ tin đầu tiên tới +35, mốc follower/tin xác thực tới +100, xác thực chứng chỉ +100.
- **AC:** mỗi phần thưởng một lần cho mỗi tài khoản (trừ điểm danh 1 lần/ngày); chống lạm dụng nhiều tài khoản cùng SĐT/thiết bị.
- **Truy vết:** F-18

### 3.5 Module M5 — Môi giới & Đối tác

#### FR-17 Đăng ký tài khoản môi giới
- **Actor:** A3 · **Luồng:** nhập SĐT → OTP → hồ sơ (thông tin liên hệ, khu vực, thị trường tập trung) → hiển thị danh bạ; quyền nâng cao chờ admin duyệt.
- **AC:** miễn phí; OTP hết hạn sau thời gian giới hạn và giới hạn số lần gửi lại.
- **Truy vết:** F-19, F-41

#### FR-18 Danh bạ & MOSO Score
- **Actor:** A1 · **Luồng:** tìm môi giới theo khu vực, thị trường (secondary_house/apartment/primary_project/rent/industrial), khoảng giá, chỉ đã xác thực → xếp hạng theo MOSO Score.
- **AC:** Score tính từ 6 yếu tố (hồ sơ, tin xác thực, review, Partner +10đ, tương tác, chứng chỉ; 40% trọng số từ đăng tin & hoạt động); phân trang trong top 50.
- **Truy vết:** F-20

#### FR-19 MOSO Partner
- **Actor:** A3, A4 · **Luồng:** đăng ký Partner cá nhân hoặc doanh nghiệp → xác minh ≤ 24h → nhận points (tới 1.000), truy cập kho hàng ngân hàng, giảm học phí (20% cá nhân / 30% DN); DN nhận website chuẩn SEO + trang quản trị đội ngũ + đồng bộ giỏ hàng lên MOSO 0đ.
- **AC:** phản hồi đăng ký ≤ 2h làm việc; tin đồng bộ từ hệ thống DN được chuẩn hoá bởi AI và không trùng lặp.
- **Truy vết:** F-21

#### FR-20 Khoá học chứng chỉ môi giới
- **Actor:** A3 · **Luồng:** đăng ký khoá 8 buổi (MOSO × IEM) → tư vấn 1-1 → học → thi → xác thực chứng chỉ trên hồ sơ (+100 points).
- **Truy vết:** F-22, F-18

#### FR-21 Cộng tác viên giới thiệu
- **Actor:** A5 · **Luồng:** gửi nguồn nhà bán/thuê hoặc nguồn khách trên mobile → MOSO xử lý → khi thành công nhận e-voucher (100k bán/khách, 10k thuê) qua Urbox/Gotit.
- **AC:** trạng thái từng nguồn hiển thị realtime; không yêu cầu chứng chỉ môi giới.
- **Truy vết:** F-23

#### FR-22 Đăng ký sự kiện Workshop
- **Actor:** A3 · **AC:** form đăng ký miễn phí, đếm ngược đến giờ sự kiện, xác nhận qua SĐT/email.
- **Truy vết:** F-24

### 3.6 Module M6 — Tài chính & Vay

#### FR-23 So sánh & đăng ký vay thế chấp
- **Actor:** A1 · **Luồng:** xem bảng lãi suất 13+ ngân hàng (cập nhật hàng tháng) → chọn gói → đăng ký hỗ trợ hồ sơ → chuyển lead cho ngân hàng.
- **AC:** hiển thị ngày cập nhật lãi suất; cảnh báo lãi thả nổi sau ưu đãi.
- **Truy vết:** F-25

#### FR-24 Bộ tính vay mua nhà
- **Actor:** A1 · **Luồng:** 3 tab: (a) khả năng mua: thu nhập, nợ, vốn tự có, lãi suất, thời hạn, % trả nợ tối đa → giá nhà tối đa; (b) DTI trước/sau vay; (c) lịch trả góp dư nợ giảm dần / trả đều.
- **AC:** DTI > 50% hiển thị cảnh báo; tổng phải trả = gốc + tổng lãi; nhãn tham khảo (C-04).
- **Truy vết:** F-26

#### FR-25 Định giá & cầm cố
- **Actor:** A1 · **Luồng:** chọn tỉnh, quận, loại hình, diện tích, kỳ hạn → giá trị ước tính (giá/m² khu vực, biên ±10%) + hạn mức vay & trả góp từng ngân hàng.
- **Truy vết:** F-27

### 3.7 Module M7 — Công cụ BĐS
| FR | Công cụ | AC chính | Truy vết |
|---|---|---|---|
| FR-26 | Thuế & phí giao dịch | TNCN 2% (bên bán, không thấp hơn bảng giá đất), trước bạ 0,5% (bên mua), công chứng luỹ tiến ~0,1%; tách bên mua/bán; có tiện ích trình duyệt Chrome/Firefox | F-28 |
| FR-27 | Bảng giá đất nhà nước | Tra theo tỉnh/huyện/xã/nhóm đất/tên đường, kèm số quyết định, ngày hiệu lực, link văn bản; tỉnh chưa có dữ liệu → báo "chưa có dữ liệu", **không** ước lượng | F-29 |
| FR-28 | Chuyển mục đích SDĐ | Tiền SDĐ = (giá đất ở − giá đất NN) × diện tích (NĐ 103/2024 Đ8) + trước bạ 0,5% + phí thẩm định, đo đạc, cấp GCN; hiển thị tỷ trọng % | F-30 |
| FR-29 | Thuê hay mua | So sánh chi phí ròng sau N năm gồm lãi vay, tăng giá, chi phí cơ hội → kết luận MUA/THUÊ | F-31 |
| FR-30 | Lợi nhuận đầu tư | Cho thuê: gross/net yield, dòng tiền, hoàn vốn, so với lãi tiết kiệm. Flip: tổng vốn, ROI, ROI quy năm | F-32 |
| FR-31 | Hiệu quả đầu tư | Giá trị sau N năm của BĐS/ngân hàng/chứng khoán/vàng, chỉ ra kênh cao nhất; ROI farmstay | F-33 |
| FR-32 | Nên mua hay chờ | Điểm 0–100 = giá khu vực (40) + lãi suất (40) + DTI (20) → MUA / CÂN NHẮC / CHỜ | F-34 |
| FR-33 | Check quy hoạch | *Backlog — sắp ra mắt* | F-35 |

Mọi công cụ M7: chạy được không cần đăng nhập, cập nhật kết quả ngay khi đổi input, ghi rõ căn cứ pháp lý & ngày cập nhật.

### 3.8 Module M8 — Dữ liệu thị trường & Nội dung
#### FR-34 Báo cáo thị trường
- Báo cáo theo tháng/quý/6 tháng/năm & khu vực; số liệu tổng (tin bán, thuê, xác thực, đã giao dịch) đếm trực tiếp, cập nhật mỗi giờ; bảng lệch cung–cầu (hạng cầu từ MOSO AI vs hạng cung từ tin đăng); tải bản đầy đủ.
- **Truy vết:** F-36
#### FR-35 Tin tức, Wiki, thuật ngữ, video
- Bài viết có tác giả, thời gian đọc, chuyên mục; trang tác giả & tiêu chuẩn biên tập (E-E-A-T); từ điển thuật ngữ theo luật hiện hành; mục video nhà đất.
- **Truy vết:** F-37, F-38

### 3.9 Module M9 — Tương tác
#### FR-36 Trò chơi đoán giá
- 5 câu × 20s; điểm: sai lệch ≤5% → 100, ≤10% → 80, ≤20% → 60, ≤35% → 40, ≤50% → 20, >50% → 0; 5 lượt tính điểm/ngày; Top 3 tháng (≥ 1.000 điểm) nhận 200/100/50 points.
- **AC:** Given top 3 nhưng < 1.000 điểm, Then không nhận thưởng; giá lấy từ tin bán công khai thật.
- **Truy vết:** F-39, F-18
#### FR-37 Tử vi & phong thuỷ AI
- Điểm phong thuỷ theo mệnh trạch & hướng nhà, xem ngày tốt (xem nhà, đặt cọc, ký HĐ, vay, nhập trạch), tarot, cung hoàng đạo, thần số học.
- **Truy vết:** F-40

### 3.10 Module M10 — Tài khoản & Hỗ trợ
| FR | Mô tả | Truy vết |
|---|---|---|
| FR-38 | Đăng nhập bằng SĐT + OTP; callbackUrl quay lại trang trước | F-41 |
| FR-39 | Tin nhắn giữa người mua và người đăng | F-41 |
| FR-40 | Xoá tài khoản tự phục vụ trong app (Tài khoản → Cài đặt tài khoản → Xoá), xoá/ẩn danh dữ liệu cá nhân | F-42 |
| FR-41 | Trung tâm trợ giúp, tiếp nhận phản ánh, cơ chế giải quyết tranh chấp | F-43 |
| FR-42 | App iOS/Android có cùng chức năng cốt lõi (tìm, đăng tin, video, bản đồ, tài khoản) | F-44 |

### 3.11 Module M11 — AI Agent Platform
#### FR-43 MCP server
- Streamable HTTP JSON-RPC 2.0 tại `/mcp`, không cần auth; `initialize → tools/list → tools/call`; tools: `search_listings`, `compare_listings`, `read_page`, `search_projects`, `search_agents`, `request_contact`. Discovery qua `/.well-known/mcp.json`, server-card, agent-skills.
- **Truy vết:** F-45
#### FR-44 Agent REST API
| Endpoint | Tham số chính | Rate limit |
|---|---|---|
| GET /api/agent/search | query, location, type, min/maxPrice, min/maxArea, bedrooms, propertyType, limit ≤ 20, offset, format | 60/phút/IP |
| GET /api/agent/compare | urls (2–5) | 30/phút/IP |
| GET /api/agent/projects | query, location, unitType, saleStatus, min/maxUnitPrice | 60/phút/IP |
| GET /api/agent/agents | query, area, focusMarket, verifiedOnly | 60/phút/IP |
| POST /api/agent/contact | name*, phone*, listing, intent, preferredTime, email, message | 10/phút/IP |
| GET /api/markdown | path* | 30/phút/IP |
- **AC:** vượt giới hạn → HTTP 429 + `Retry-After`; phản hồi thành công có `X-RateLimit-Limit`, `RateLimit-Policy`; contact là thao tác ghi duy nhất.
- **Truy vết:** F-46
#### FR-45 Markdown & tài liệu cho LLM
- Mọi trang trả markdown khi `Accept: text/markdown`; xuất bản llms.txt, llms-full.txt, llms-faq.txt, sitemap-ai.xml, openapi.json (3.1), auth.md.
- **Truy vết:** F-47, F-48

---

## 4. Yêu cầu phi chức năng
| ID | Nhóm | Yêu cầu | Đo lường |
|---|---|---|---|
| NFR-01 | Hiệu năng | Trang danh sách & chi tiết SSR, LCP < 2,5s trên 4G | Core Web Vitals P75 |
| NFR-02 | Hiệu năng | Tìm kiếm API P95 < 500ms với 50k+ tin | APM |
| NFR-03 | Hiệu năng | AI sinh tin ≤ 30s P95; xoá watermark ≤ 60s cho lô 20 ảnh | log thời gian |
| NFR-04 | Mở rộng | Hỗ trợ ≥ 100k tin hoạt động và sitemap phân theo tháng | load test |
| NFR-05 | Bảo mật | Ẩn số nhà không rò rỉ qua bất kỳ kênh nào (HTML, JSON, markdown, MCP, ảnh, sitemap) | pentest |
| NFR-06 | Bảo mật | OTP giới hạn tần suất; chống brute-force; HTTPS toàn site | |
| NFR-07 | Bảo mật | Rate limit theo IP trên mọi endpoint agent (FR-44) | |
| NFR-08 | Quyền riêng tư | Tuân thủ NĐ 13/2023; chỉ thu thập dữ liệu trong chính sách bảo mật; xoá tài khoản xoá dữ liệu cá nhân | audit |
| NFR-09 | Toàn vẹn tài chính | Giao dịch points nguyên tử, idempotent, có sổ cái; không âm số dư | đối soát hằng ngày |
| NFR-10 | SEO / GEO | URL thân thiện tiếng Việt không dấu, structured data, sitemap index, robots cho phép bot AI; landing theo đơn vị hành chính | Search Console |
| NFR-11 | Khả dụng | Uptime ≥ 99,5%/tháng | status monitor |
| NFR-12 | Khả năng truy cập | Link "Bỏ qua tới nội dung", WCAG 2.1 AA | axe audit |
| NFR-13 | Độ chính xác nội dung | Công cụ thuế/pháp lý ghi căn cứ & ngày cập nhật; không hiển thị số ước lượng khi thiếu dữ liệu nguồn | review biên tập |
| NFR-14 | Đa nền tảng | Web responsive + app iOS/Android dùng chung backend | |
| NFR-15 | Quan sát | Log & metric cho lead, points, xác thực, API agent | dashboard |

---

## 5. Epics & User Stories (MoSCoW)
| Epic | User story | MoSCoW |
|---|---|---|
| E1 Tìm nhà thật | Là người mua, tôi muốn lọc tin xác thực theo khu vực & giá để không mất thời gian với tin ảo | Must |
| | Là người mua, tôi muốn vẽ vùng trên bản đồ để tìm nhà quanh nơi làm việc | Should |
| | Là người mua, tôi muốn gõ câu tự nhiên để AI hiểu nhu cầu | Should |
| E2 Đăng tin nhanh | Là chủ nhà, tôi muốn AI viết tin trong 30 giây | Must |
| | Là chủ nhà, tôi muốn xoá watermark ảnh cũ trước khi đăng | Could |
| | Là chủ nhà, tôi muốn đẩy tin 7 ngày để bán nhanh | Should |
| E3 Niềm tin "3 THẬT" | Là chủ nhà, tôi muốn xác thực tin để được badge và giảm phí | Must |
| | Là môi giới, tôi muốn ẩn số nhà để không bị cướp khách | Must |
| E4 Kinh tế points | Là người dùng, tôi muốn kiếm points miễn phí qua điểm danh/nhiệm vụ | Should |
| | Là người đăng, tôi muốn tin tự gia hạn khi hết 30 ngày | Must |
| E5 Hệ sinh thái môi giới | Là môi giới, tôi muốn có hồ sơ xếp hạng trong danh bạ | Must |
| | Là môi giới, tôi muốn nhận nguồn ký gửi chính chủ trong khu vực | Should |
| | Là DN, tôi muốn đồng bộ giỏ hàng có sẵn lên MOSO miễn phí | Should |
| | Là CTV, tôi muốn giới thiệu nguồn và nhận e-voucher | Could |
| E6 Tài chính mua nhà | Là người mua, tôi muốn biết giá nhà tối đa mình mua được và so sánh lãi suất | Must |
| E7 Công cụ & dữ liệu | Là nhà đầu tư, tôi muốn tính thuế phí, ROI và đọc báo cáo thị trường | Should |
| | Là người mua, tôi muốn check quy hoạch | Won't (now) |
| E8 Engagement | Là người dùng, tôi muốn chơi đoán giá để luyện cảm giác giá thị trường | Could |
| E9 AI-native | Là AI agent, tôi muốn tìm & so sánh tin qua MCP để trả lời người dùng | Should |

---

## 6. Ma trận truy vết
| Module | Feature | FR | NFR | Epic |
|---|---|---|---|---|
| M1 Tìm kiếm | F-01..F-09 | FR-01..FR-07 | NFR-01,02,10 | E1 |
| M2 Đăng tin | F-10..F-14 | FR-08..FR-12 | NFR-03 | E2 |
| M3 Xác thực | F-15, F-16 | FR-13, FR-14 | NFR-05 | E3 |
| M4 Points | F-17, F-18 | FR-15, FR-16 | NFR-09 | E4 |
| M5 Môi giới | F-19..F-24 | FR-17..FR-22 | NFR-06 | E5 |
| M6 Tài chính | F-25..F-27 | FR-23..FR-25 | NFR-13 | E6 |
| M7 Công cụ | F-28..F-35 | FR-26..FR-33 | NFR-13 | E7 |
| M8 Nội dung | F-36..F-38 | FR-34, FR-35 | NFR-10 | E7 |
| M9 Tương tác | F-39, F-40 | FR-36, FR-37 | — | E8 |
| M10 Tài khoản | F-41..F-44 | FR-38..FR-42 | NFR-06,08,12,14 | — |
| M11 Agent | F-45..F-48 | FR-43..FR-45 | NFR-07 | E9 |

## 7. Câu hỏi mở
1. Cổng thanh toán nạp points (D-02)?
2. Điều kiện "khách có nhu cầu thật" để mở Ẩn số nhà (FR-14)?
3. Xác thực tin do người hay AI, tỷ lệ tự động hoá? (FR-13)
4. Mô hình doanh thu từ lead vay ngân hàng & hoa hồng Partner — có cần module đối soát hoa hồng?
