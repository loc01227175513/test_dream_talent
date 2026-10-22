---
title: "Product Brief — MOSO.VN"
status: draft
created: 2026-10-22
updated: 2026-10-22
mode: headless · fast path
source: out/corpus.md (llms.txt + 60 trang tĩnh moso.vn, crawl 22/10/2026)
---

# Product Brief: MOSO.VN — Nền tảng PropTech BĐS "3 THẬT"

> Brief phân tích ngược (reverse-engineered) từ corpus crawl, chỉ dùng corpus làm nguồn. Mọi suy luận không có nguyên văn trong corpus được gắn **[ASSUMPTION]**.

## 1. Tóm tắt

MOSO.VN (Công ty TNHH Công nghệ Bất động sản MOSO, công ty mẹ Loan Factory) là sàn giao dịch BĐS ứng dụng AI tại Việt Nam, trọng tâm TP.HCM, mở rộng Bình Dương, Đồng Nai, Long An, Hà Nội, Đà Nẵng. Định vị: không đua số lượng tin mà "tuyên chiến với tin ảo" bằng chuẩn **"3 THẬT" — Nhà Thật, Giá Thật, Địa Chỉ Thật** (dữ liệu chuẩn ARV: Accurate · Real · Verified).

Sản phẩm gồm: marketplace mua bán/cho thuê và dự án sơ cấp; đăng tin bằng AI (~30 giây) trả phí bằng MOSO Points; công nghệ "Ẩn số nhà" chống sao chép tin; hệ sinh thái môi giới/đối tác (MOSO Partner, CTV, khoá chứng chỉ); kênh vay thế chấp với 13+ ngân hàng; bộ ~15 công cụ tài chính – pháp lý – đầu tư miễn phí; báo cáo thị trường; và một lớp API/MCP mở cho AI agent bên thứ ba. Nền tảng có web + app iOS/Android.

Quy mô tự công bố (llms.txt, 22/10/2026): 25.088 tin bán · 26.193 tin cho thuê · 4.791 dự án.

## 2. Vấn đề

- Thị trường tràn lan tin ảo: ảnh không thật, giá mồi (bait pricing), địa chỉ mập mờ. Người mua phải gọi điện mới biết giá/địa chỉ.
- Chủ nhà/môi giới bị sao chép tin, "cướp khách"; ảnh tải lại từ nơi khác dính logo/SĐT.
- Người mua thiếu công cụ tự kiểm chứng: thuế phí, bảng giá đất nhà nước, khả năng vay, nên mua hay chờ.
- Môi giới thiếu nguồn hàng chính chủ, thiếu chứng chỉ hành nghề, thiếu kênh vay cho khách.

## 3. Giải pháp & điểm khác biệt

| Trụ cột | Cách MOSO giải quyết (theo corpus) |
|---|---|
| Nhà Thật | Xác thực chủ sở hữu, pháp lý (sổ đỏ/sổ hồng), ảnh; badge "Xác thực"; tin đã xác thực rẻ hơn (5 vs 8 MP) |
| Giá Thật | Giá niêm yết hiển thị ngay trên danh sách, giá/m² tự tính; trò chơi đoán giá dùng giá tin thật |
| Địa Chỉ Thật | Ghim chính xác trên bản đồ, giá trên từng ghim; "Ẩn số nhà" để chủ tin kiểm soát ai thấy địa chỉ đầy đủ |
| AI | AI viết tin 30 giây, tìm kiếm ngôn ngữ tự nhiên, xoá watermark ảnh, gợi ý khách cho môi giới |
| Tài chính | So sánh lãi suất 13+ ngân hàng, MOSO xử lý hồ sơ vay phí 0đ, kế thừa nền FinTech của Loan Factory |
| Mở cho AI | llms.txt, MCP server, OpenAPI, content negotiation `text/markdown` — hiếm thấy ở sàn BĐS VN [ASSUMPTION] |

Khác biệt thật nằm ở **chính sách phí gắn với xác thực** và **lớp dữ liệu/agent mở**; còn "AI 30 giây" và công cụ tính toán là thứ đối thủ có thể sao chép nhanh [ASSUMPTION].

## 4. Actor / Persona

| ID | Actor | Vai trò | Nhu cầu chính | Nguồn |
|---|---|---|---|---|
| A1 | Người mua / người thuê | Khách vãng lai hoặc tài khoản thường | Tìm nhà thật, thấy giá + địa chỉ, tính vay/thuế, đặt lịch xem | /quyen-loi-nguoi-dung |
| A2 | Chủ nhà (FSBO) | Người đăng tin bán/cho thuê không qua môi giới | Đăng tin nhanh, rẻ, bảo vệ tin, ký gửi bán nhanh | /dang-tin |
| A3 | Môi giới cá nhân | Tài khoản môi giới (SĐT + OTP), có thể là MOSO Partner | Nguồn hàng chính chủ, khách thật, MOSO Score cao, chứng chỉ, 100% hoa hồng | /dang-ky-moi-gioi |
| A4 | Doanh nghiệp / Sàn BĐS / Chủ đầu tư | Đối tác doanh nghiệp | Website + quản trị miễn phí, đồng bộ giỏ hàng, nguồn hàng ngân hàng | /doi-tac-doanh-nghiep |
| A5 | Cộng tác viên (CTV) | Bất kỳ ai, không cần chứng chỉ | Giới thiệu nguồn nhà/khách nhận e-voucher | /cong-tac-vien |
| A6 | Nhà đầu tư | Người mua với mục tiêu sinh lời | Công cụ ROI/yield, BĐS đấu giá phát mãi giá thấp hơn 20–60% | /nguon-nha-dac-biet |
| A7 | AI agent bên thứ ba | Client máy (GPTBot, ClaudeBot, agent trình duyệt…) | Đọc tin/dự án/môi giới qua MCP/API, gửi yêu cầu xem nhà thay người dùng | /llms.txt |
| A8 | Chuyên viên / Admin MOSO | Nội bộ | Kiểm duyệt tin, duyệt môi giới, gọi lại xác nhận lịch xem, xử lý hồ sơ vay, biên tập nội dung [ASSUMPTION: không có giao diện backoffice trong corpus] | /tieu-chuan-noi-dung |
| A9 | KOL/KOC | Đối tác nội dung marketing | Hợp tác review MOSO trên TikTok/Facebook | /tuyen-dung-kol |
| A10 | Hệ thống ngoài | Ngân hàng đối tác, IEM (đào tạo), Urbox/Gotit (e-voucher), Cục Thi hành án, App Store/Google Play | Tích hợp/đối tác [ASSUMPTION: hình thức tích hợp kỹ thuật chưa rõ] | /moso-partner |

## 5. Tính năng theo module

### M1 · Tìm kiếm & Khám phá BĐS

| ID | Tính năng | Mô tả | Nguồn |
|---|---|---|---|
| F-01 | Danh sách mua bán nhà đất | Danh sách toàn quốc, lọc theo loại hình (căn hộ, nhà hẻm, nhà mặt tiền, đất); lọc "Tin xác thực", "Tin có video"; xem dạng danh sách/lưới; thẻ tin hiện giá, giá/m², diện tích, tầng, PN/WC, địa chỉ | /mua-ban-nha-dat |
| F-02 | Danh sách cho thuê | 9 nhóm: phòng trọ, căn hộ chung cư, nhà, căn hộ dịch vụ, mặt bằng, văn phòng, kho/nhà xưởng, đất; cùng bộ lọc xác thực/video | /cho-thue-nha-dat |
| F-03 | Trang danh mục SEO theo loại hình & khu vực | Landing page riêng cho từng loại hình (vd. /mua-ban-nha-hem, /cho-thue-phong-tro) và từng quận (vd. /ban-nha-quan-1-thanh-pho-ho-chi-minh) | / |
| F-04 | Bản đồ BĐS | Xem tin trên bản đồ, giá trên từng ghim, vẽ vùng để tìm | /mua-ban-nha-dat?xem=ban-do |
| F-05 | Tìm kiếm AI ngôn ngữ tự nhiên | Tìm bằng câu tự nhiên, gợi ý BĐS tương tự, phát hiện tiện ích/đặc điểm | /services |
| F-06 | Lưu tin & thông báo tìm kiếm | Lưu tin yêu thích, lưu tìm kiếm, nhận thông báo khi có tin mới đúng nhu cầu | /quyen-loi-nguoi-dung |
| F-07 | Video BĐS | Kênh video tin đăng riêng (video.moso.vn) và tab Video trong app | / |
| F-08 | Tra cứu dự án sơ cấp | 4.791 dự án; thẻ dự án có trạng thái bán (nhận booking/mở bán…), số căn, diện tích, chủ đầu tư, pháp lý, giá từ | /tim-kiem-du-an |
| F-09 | So sánh dự án | Thêm nhiều dự án vào bảng phân tích và so sánh | /so-sanh-du-an |
| F-10 | Nguồn nhà đặc biệt (MOSO Signature) | Giỏ hàng BĐS đấu giá/phát mãi từ ngân hàng & Thi hành án; khách để lại tiêu chí (5 tỉnh, 5 phân khúc giá), MOSO kiểm tra pháp lý và đồng hành đến bàn giao | /nguon-nha-dac-biet |

### M2 · Liên hệ & Giao dịch

| ID | Tính năng | Mô tả | Nguồn |
|---|---|---|---|
| F-11 | Nhắn tin với người đăng tin | Chat trực tiếp với người đăng hoặc chuyên viên tư vấn ngay trong ứng dụng | /tro-giup |
| F-12 | Đặt lịch xem nhà | Đặt lịch xem trực tiếp qua nền tảng, nhắc lịch tự động; chuyên viên gọi lại xác nhận | /tro-giup |
| F-13 | Yêu cầu xem nhà / tư vấn | Để lại tên + SĐT, intent viewing/consult; tạo yêu cầu chờ xử lý, chống trùng cùng SĐT + tin trong 24h | /api/agent/contact |
| F-14 | Hỗ trợ giao dịch & pháp lý | Hướng dẫn giao dịch từng bước, xác minh tài liệu, checklist pháp lý, hợp đồng chuẩn hoá, hỗ trợ đàm phán (dịch vụ nâng cao có phí) | /services |

### M3 · Đăng tin & Quản lý tin

| ID | Tính năng | Mô tả | Nguồn |
|---|---|---|---|
| F-15 | Đăng tin bán bằng AI | Form tin bán; AI gợi ý tiêu đề, mô tả, bố cục trong ~30 giây; người đăng bổ sung ảnh, giá, pháp lý | /dang-tin-ban-nha-dat |
| F-16 | Đăng tin cho thuê bằng AI | Form riêng cho thuê (giá thuê, chi phí kèm, nội thất, điều kiện thuê); AI hỗ trợ ~30 giây | /dang-tin-cho-thue |
| F-17 | Tin của tôi | Sửa tin, cập nhật giá, đánh dấu đã bán/đã cho thuê, ẩn tin; tự gia hạn mỗi 30 ngày bằng points | /dang-tin-cho-thue |
| F-18 | Đẩy tin | 3 gói: 8 giờ (5.000đ, tối đa 3 lượt/tin/ngày), 24 giờ + nhãn Hot (10.000đ), 7 ngày + nhãn Hot (50.000đ); phạm vi khu vực đăng hoặc toàn tỉnh | /bang-gia-dang-tin |
| F-19 | Xoá watermark ảnh bằng AI | AI xoá logo/chữ/SĐT; tô để xoá chỗ sót; ≤20 ảnh/lần, ≤10 MB, PNG/JPG/WEBP; lưu phiên bản, so sánh trước/sau; tải từng ảnh hoặc ZIP; có trong form đăng tin | /cong-cu/chinh-anh-bds |
| F-20 | Thống kê tin đăng | Lượt xem, lượt quan tâm theo thời gian thực cho người bán | /llms.txt |

### M4 · Xác thực & Bảo vệ tin ("3 THẬT")

| ID | Tính năng | Mô tả | Nguồn |
|---|---|---|---|
| F-21 | Xác thực tin đăng | Kiểm duyệt chủ sở hữu, pháp lý (sổ đỏ/sổ hồng), đối chiếu quy hoạch, ảnh thật theo chuẩn ARV; gắn huy hiệu "Xác thực" | /quyen-loi-nguoi-dung |
| F-22 | Ẩn số nhà | Ẩn địa chỉ chi tiết, chỉ hiện đầy đủ cho khách có nhu cầu thật đã xác thực; 5 point mỗi kỳ 30 ngày | /bang-gia-dang-tin |
| F-23 | Tiêu chuẩn nội dung | AI soạn nháp, biên tập viên kiểm tra pháp lý/số liệu/nguồn trước khi xuất bản; kênh đính chính qua email | /tieu-chuan-noi-dung |

### M5 · MOSO Points & Thanh toán

| ID | Tính năng | Mô tả | Nguồn |
|---|---|---|---|
| F-24 | Ví MOSO Points & bảng giá | 1 point = 1.000đ (đã gồm VAT); tin bán 8 point (5 khi xác thực), tin thuê 5; tự trừ khi gia hạn, thiếu point thì ẩn số liên hệ; gói nạp từ 50.000đ | /bang-gia-dang-tin |
| F-25 | Kiếm points miễn phí | Quà chào mừng (+30 thường, +100 môi giới), hoàn thiện hồ sơ, nhiệm vụ tin đầu tiên, mốc tin xác thực, mốc người theo dõi, điểm danh +1/ngày | /chinh-sach-moso-points |
| F-26 | Trò chơi đoán giá nhà đất | 5 câu × 20 giây, chấm điểm theo % sai lệch; 5 lượt tính điểm/ngày; bảng xếp hạng tháng, Top 3 (≥1000 điểm) nhận 200/100/50 points | /doan-gia-nha-dat |

### M6 · Môi giới & Đối tác

| ID | Tính năng | Mô tả | Nguồn |
|---|---|---|---|
| F-27 | Đăng ký tài khoản môi giới | Tạo tài khoản bằng SĐT + OTP, hoàn thiện hồ sơ (liên hệ, khu vực hoạt động); quyền nâng cao cần admin duyệt | /register-agent |
| F-28 | Danh bạ môi giới & MOSO Score | Tra cứu môi giới cá nhân/doanh nghiệp đã xác thực; xếp hạng MOSO Score theo 6 yếu tố (hồ sơ, tin xác thực, review, Partner +10đ, tương tác, chứng chỉ) | /danh-ba-moi-gioi-bat-dong-san |
| F-29 | Nhà đất cần bán nhanh (ký gửi) | Kho tin chính chủ ký gửi (2.648 căn) để môi giới nhận bán hưởng hoa hồng | /nha-dat-can-ban-nhanh |
| F-30 | MOSO Partner cá nhân | Đăng ký đối tác miễn phí: tặng points, nguồn hàng xác thực, kết nối 13+ ngân hàng, giảm học phí chứng chỉ, phản hồi trong 2 giờ | /doi-tac-ca-nhan |
| F-31 | MOSO Partner doanh nghiệp | Website doanh nghiệp chuẩn SEO + trang quản trị nguồn hàng/đội ngũ 0đ; đồng bộ giỏ hàng lên MOSO.vn 0đ | /doi-tac-doanh-nghiep |
| F-32 | Hoa hồng & theo dõi realtime | Chính sách hoa hồng sơ cấp/thứ cấp; theo dõi tiến độ khách và hoa hồng realtime trên app; sự kiện Workshop đăng ký tham dự | /moso-partner-workshop |
| F-33 | Cộng tác viên giới thiệu | Gửi nguồn nhà bán/khách (e-voucher 100.000đ) hoặc nguồn nhà thuê (10.000đ) trên mobile; theo dõi thưởng realtime | /cong-tac-vien |
| F-34 | Khoá học chứng chỉ môi giới | Khoá 8 buổi cùng IEM, 1.990.000đ cho Partner, tặng 2 workshop + gói đăng tin 200K; xác thực chứng chỉ được +100 points | /khoa-hoc-chung-chi-moi-gioi |
| F-35 | CRM & AI gợi ý khách cho môi giới | Quản lý CRM, lịch hẹn, hợp đồng; AI gợi ý khách tiềm năng theo danh mục BĐS đang quản lý | /llms.txt |

### M7 · Tài chính & Vay mua nhà

| ID | Tính năng | Mô tả | Nguồn |
|---|---|---|---|
| F-36 | Vay thế chấp qua MOSO | Partner gửi hồ sơ khách; MOSO match ngân hàng, trình hồ sơ, theo dõi real-time; phí 0đ; tiếp nhận & phân loại <30 phút; bảng lãi suất theo tháng | /vay-the-chap |
| F-37 | Công cụ vay mua nhà | 3 phép tính: khả năng mua tối đa, DTI trước/sau vay (ngưỡng 50%), lịch trả góp (dư nợ giảm dần/trả đều) | /cong-cu/vay-mua-nha |
| F-38 | Định giá & cầm cố BĐS | Ước tính giá trị theo giá rao/m² khu vực (biên ±10%) và hạn mức vay, trả góp theo từng ngân hàng | /cong-cu/dinh-gia-cam-co-bat-dong-san |

### M8 · Công cụ pháp lý, thuế & đầu tư

| ID | Tính năng | Mô tả | Nguồn |
|---|---|---|---|
| F-39 | Tính thuế & chi phí giao dịch | Thuế TNCN 2%, trước bạ 0,5%, công chứng ~0,1%, đăng bộ; tách phần bên bán/bên mua; có tiện ích Chrome/Firefox | /cong-cu/tinh-thue-giao-dich-bds |
| F-40 | Bảng giá đất nhà nước | Tra đơn giá UBND tỉnh theo tỉnh/huyện/xã/nhóm đất/tên đường, kèm số quyết định, ngày hiệu lực, link văn bản gốc; báo rõ tỉnh chưa có dữ liệu | /cong-cu/bang-gia-dat-nha-nuoc |
| F-41 | Chi phí chuyển mục đích sử dụng đất | Ước tính tiền sử dụng đất, trước bạ, phí thẩm định/đo đạc/cấp giấy theo NĐ 103/2024 | /cong-cu/chuyen-muc-dich-su-dung-dat |
| F-42 | Check quy hoạch | Kiểm tra quy hoạch sử dụng đất trước khi mua — trạng thái "Sắp ra mắt" | /cong-cu |
| F-43 | Thuê hay mua nhà | So sánh chi phí ròng thuê vs mua theo số năm, tính tăng giá và chi phí cơ hội vốn | /cong-cu/thue-hay-mua-nha |
| F-44 | Lợi nhuận đầu tư BĐS | Cho thuê (gross/net yield, dòng tiền, hoàn vốn) và flip mua–sửa–bán (ROI, ROI quy năm) | /cong-cu/loi-nhuan-dau-tu-bds |
| F-45 | Hiệu quả đầu tư | So sánh chi phí cơ hội BĐS/ngân hàng/chứng khoán/vàng; ROI farmstay/nghỉ dưỡng | /cong-cu/hieu-qua-dau-tu |
| F-46 | Nên mua nhà hay chờ | Chấm điểm 0–100 (đà tăng giá 40, lãi vay 40, DTI 20) → MUA / CÂN NHẮC / CHỜ | /cong-cu/nen-mua-nha-hay-cho |
| F-47 | Tử vi & phong thủy AI | Phong thủy mua nhà theo mệnh/hướng, xem ngày, tử vi, Tarot, phong thủy SĐT/biển số | /tu-vi-phong-thuy |

### M9 · Nội dung & Dữ liệu thị trường

| ID | Tính năng | Mô tả | Nguồn |
|---|---|---|---|
| F-48 | Báo cáo thị trường | Báo cáo tháng/quý/6 tháng/năm theo khu vực từ tin đăng thật; số liệu cập nhật mỗi giờ; bảng lệch cung–cầu theo khu vực; tải bản đầy đủ | /bao-cao-thi-truong-bds |
| F-49 | Chỉ số thị trường (MPI, Heat Map, thanh khoản) | MOSO Price Index, bản đồ nhiệt khu vực, chỉ số thanh khoản, báo giá theo quận/phường | /tin-tuc-bat-dong-san |
| F-50 | Tin tức BĐS | Tin tức, phân tích thị trường, pháp lý, phong thủy theo chuyên mục; trang tác giả (E-E-A-T) | /tin-tuc-bat-dong-san |
| F-51 | Thuật ngữ BĐS | Từ điển 21 thuật ngữ theo Luật Đất đai 2024, Luật Nhà ở 2023, Luật KD BĐS 2023 | /thuat-ngu-bat-dong-san |
| F-52 | Trung tâm trợ giúp | Bài hướng dẫn theo chủ đề (tài khoản & bảo mật, đăng tin, tìm kiếm & lưu tin); hotline 1900 252 307 | /tro-giup |

### M10 · Tài khoản & Ứng dụng

| ID | Tính năng | Mô tả | Nguồn |
|---|---|---|---|
| F-53 | Đăng nhập & tài khoản | Đăng nhập bắt buộc cho đăng tin, đăng ký môi giới, tải ảnh lên công cụ; hồ sơ (ảnh, email, Facebook), người theo dõi | /register-agent |
| F-54 | Xoá tài khoản trong app | Tài khoản → Cài đặt tài khoản → xoá, 3 bước, dưới 1 phút | /huong-dan-xoa-tai-khoan |
| F-55 | Ứng dụng di động iOS/Android | App với các tab Tìm nhà, Video, Bản đồ, Đăng tin, Tài khoản; tải qua QR | /tai-ung-dung |
| F-56 | Chính sách bảo mật | Thu thập họ tên, SĐT, email, MST, giấy tờ pháp lý (người đăng) và họ tên, SĐT (người mua); cung cấp cho cơ quan tư pháp khi luật yêu cầu | /chinh-sach-bao-mat |

### M11 · Nền tảng cho AI Agent (API/MCP)

| ID | Tính năng | Mô tả | Nguồn |
|---|---|---|---|
| F-57 | MCP server | MCP Streamable HTTP (JSON-RPC 2.0), không cần xác thực; tool search_listings, compare_listings, read_page, search_projects, search_agents, request_contact | /mcp |
| F-58 | API tra cứu tin đăng | GET; lọc query, location (theo cấp hành chính, khớp cả tên trước/sau sáp nhập 2025), type, giá, diện tích, phòng ngủ, propertyType; limit ≤20; JSON/markdown | /api/agent/search |
| F-59 | API so sánh tin đăng | So sánh 2–5 tin theo cùng bộ tiêu chí + giá/m² đất tự tính | /api/agent/compare |
| F-60 | API tra cứu dự án & môi giới | Dự án theo unitType/saleStatus/giá tổng căn; môi giới theo khu vực/focusMarket/verifiedOnly, xếp theo MOSO Score (top 50) | /api/agent/projects |
| F-61 | Đọc trang dạng markdown | /api/markdown?path=… và header `Accept: text/markdown` trên mọi trang (giảm ~97% token) | /api/markdown |
| F-62 | Khai báo cho agent | llms.txt, llms-full.txt, llms-faq.txt, agent-skills index, WebMCP tools manifest, OpenAPI 3.1, auth.md, sitemap-ai.xml | /.well-known/agent-skills/index.json |

## 6. Phạm vi

- **Trong phạm vi brief:** toàn bộ bề mặt công khai đã crawl (web + mô tả app + API agent).
- **Ngoài phạm vi / không quan sát được:** backoffice kiểm duyệt, quy trình nội bộ xử lý vay, cổng thanh toán nạp points, trang chi tiết tin/dự án, nội dung llms-full.txt, openapi.json, auth.md (chỉ được nhắc tới, không crawl) [ASSUMPTION: phạm vi crawl = 60 trang tĩnh + llms.txt].

## 7. Ràng buộc

| # | Ràng buộc | Nguồn |
|---|---|---|
| C-01 | Chu kỳ hiển thị tin 30 ngày; tự trừ point khi gia hạn; thiếu point → ẩn số liên hệ | /bang-gia-dang-tin |
| C-02 | Giá niêm yết đã gồm VAT; 1 point = 1.000đ | /bang-gia-dang-tin |
| C-03 | Đẩy tin 8h tối đa 3 lượt/tin/ngày | /bang-gia-dang-tin |
| C-04 | Xoá watermark: ≤20 ảnh/lần, ≤10 MB/ảnh, PNG/JPG/WEBP, phải đăng nhập | /cong-cu/chinh-anh-bds |
| C-05 | Rate limit API: search/projects/agents 60 req/phút/IP; compare, markdown 30; contact 10; vượt → HTTP 429 + Retry-After | /llms.txt |
| C-06 | API contact là thao tác ghi duy nhất; chỉ gọi khi người dùng đồng ý để lại tên + SĐT thật; không được báo "đã chốt lịch"; trùng trong 24h trả `duplicated: true` | /llms.txt |
| C-07 | Địa danh phải nằm trong `location`, không trong `query`; minUnitPrice/maxUnitPrice là giá tổng căn; giá/m² compare tính theo diện tích đất | /llms.txt |
| C-08 | Sáp nhập hành chính 2025: "Hồ Chí Minh" gồm cả Bình Dương và Bà Rịa–Vũng Tàu cũ; địa chỉ kết quả có thể vẫn ghi tên cũ; báo cáo cung đếm theo địa chỉ cũ | /llms.txt |
| C-09 | Mọi công cụ tính toán/định giá chỉ mang tính tham khảo, không phải khuyến nghị đầu tư hay định giá chính thức | /cong-cu |
| C-10 | Căn cứ pháp lý: Luật Đất đai 2024, Luật Nhà ở 2023, Luật KD BĐS 2023, NĐ 103/2024, NĐ 10/2022, TT 85/2019 | /thuat-ngu-bat-dong-san |
| C-11 | Sàn TMĐT đã thông báo Bộ Công Thương; dữ liệu cá nhân cung cấp cho cơ quan tư pháp khi có yêu cầu | /chinh-sach-bao-mat |
| C-12 | Ngôn ngữ chính vi-VN, phụ en; cho phép mọi AI crawler | /llms.txt |
| C-13 | Trò chơi đoán giá: chỉ 5 lượt/ngày được tính điểm; thưởng cần Top 3 và ≥1000 điểm/tháng | /doan-gia-nha-dat |

## 8. Câu hỏi mở

| # | Câu hỏi | Vì sao quan trọng |
|---|---|---|
| Q-01 | Tin "chưa xác thực" vẫn được đăng (8 MP) — vậy "mọi BĐS xác thực trước khi đăng" và "xác thực 100%" nghĩa là gì? Báo cáo T9/2026 ghi 91% tin đã xác thực. | Mâu thuẫn trực tiếp với lời hứa "Nhà Thật"; ảnh hưởng thiết kế luồng kiểm duyệt |
| Q-02 | Số liệu quy mô không thống nhất: tin bán 25.088 (llms.txt) vs 18.961 (báo cáo); tin xác thực 10.000+ / 15K+ / 16.000+ / 21.694; môi giới 1.000+ / 1.200+ / 2.000+; người dùng 5.000+ / 100.000+ / 150K+/ngày. Số nào là chuẩn? | Cần baseline cho chỉ số thành công |
| Q-03 | Quà points cho môi giới/Partner: +100, 200, "tới 1.000" hay 100 MP? | Ảnh hưởng chính sách points và chi phí khuyến mãi |
| Q-04 | /vay-the-chap hiển thị "1 ngân hàng đối tác" trong khi mọi nơi ghi 13+; trang này dành cho Partner hay cả người mua cuối? | Phạm vi module vay |
| Q-05 | "Ẩn số nhà" là tính năng mặc định hay add-on trả phí 5 point/kỳ? "Khách có nhu cầu thật đã xác thực" được xác thực bằng gì (OTP, đặt lịch)? | Luồng hiển thị địa chỉ — cốt lõi của "Địa Chỉ Thật" |
| Q-06 | AVM được quảng bá, nhưng công cụ định giá chỉ dùng giá rao/m² khu vực ±10%. Có mô hình AVM thực sự không? | Tránh hứa quá mức |
| Q-07 | CRM, AI gợi ý khách, analytics lượt xem, nhắc lịch tự động chỉ xuất hiện trong llms.txt — đã có trên sản phẩm chưa? [ASSUMPTION: có trong app, không lộ ra trang tĩnh] | Xác định tính năng hiện có vs roadmap |
| Q-08 | Cổng thanh toán nạp points (gói từ 50.000đ) là gì? Có hoàn tiền không? | Ràng buộc thanh toán/pháp lý |
| Q-09 | Công thức MOSO Score (trọng số 40% từ đăng tin & hoạt động, Partner +10đ) đầy đủ ra sao? | Tính minh bạch xếp hạng môi giới |
| Q-10 | Xác thực tài khoản/agent qua auth.md dùng cơ chế gì, khi MCP lại "không cần xác thực"? | Bảo mật lớp agent, chống spam lead qua API |
| Q-11 | Dịch vụ nâng cao có phí (thẩm định chuyên sâu, đàm phán hợp đồng) có bảng giá không? | Mô hình doanh thu ngoài phí đăng tin |
| Q-12 | Mô hình doanh thu chính: phí đăng/đẩy tin, hoa hồng sơ cấp/thứ cấp, hoa hồng giới thiệu vay, hay dịch vụ Signature? [ASSUMPTION: kết hợp cả bốn] | Định hướng ưu tiên PRD |

## 9. Chỉ số thành công đề xuất [ASSUMPTION]

- Tỷ lệ tin đã xác thực trên tổng tin đang hiển thị (baseline 91% theo báo cáo T9/2026).
- Tỷ lệ yêu cầu xem nhà được chuyên viên xác nhận; thời gian phản hồi.
- Số hồ sơ vay chuyển qua MOSO và tỷ lệ giải ngân.
- Số môi giới hoạt động / Partner kích hoạt; tỷ lệ tin trùng lặp (định vị "TOP 2 tin xác thực & không trùng lặp").
- Lưu lượng từ AI agent (MCP/API) và tỷ lệ chuyển thành lead.
