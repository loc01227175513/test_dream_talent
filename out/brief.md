# Product Brief — MOSO.vn (BMAD · Analyst)

> Nguồn: 60 trang sitemap-static + llms.txt của moso.vn, đọc qua `/api/markdown` (22/10/2026). Mục đánh dấu *(giả định)* là suy luận, không có trong corpus.

## 1. Vấn đề
Thị trường BĐS Việt Nam tràn lan **tin ảo**: ảnh giả, giá "bait", địa chỉ mập mờ, tin bị sao chép/cướp khách. Người mua mất thời gian gọi điện hỏi giá/địa chỉ; chủ nhà và môi giới mất khách vì bị copy tin.

## 2. Giải pháp & giá trị cốt lõi — "3 THẬT"
- **Nhà Thật** — xác thực ảnh, pháp lý, chính chủ trước khi đăng.
- **Giá Thật** — giá niêm yết là giá thực, không thổi giá.
- **Địa Chỉ Thật** — ghim chính xác trên bản đồ.

4 điểm nhấn: AI đăng tin 30 giây · phí minh bạch (5–8 MOSO Points/30 ngày) · "Ẩn số nhà" chống sao chép · so sánh vay 13+ ngân hàng.

Quy mô: 25.088 tin bán · 26.193 tin thuê · 4.791 dự án; trọng tâm TP.HCM, mở rộng Hà Nội, Đà Nẵng, Hải Phòng, Cần Thơ, Đồng Nai, Bình Dương.

## 3. Actor / Persona
| ID | Actor | Nhu cầu chính |
|---|---|---|
| A1 | Người mua / thuê (Guest & User) | Tìm nhà thật, thấy giá + địa chỉ, tính vay, đặt lịch xem |
| A2 | Chủ nhà (FSBO) | Đăng tin nhanh, bảo vệ tin, bán không qua môi giới |
| A3 | Môi giới cá nhân | Nguồn hàng chính chủ, khách thật, hồ sơ uy tín, 100% hoa hồng |
| A4 | Doanh nghiệp / Sàn BĐS | Website + quản trị miễn phí, đồng bộ giỏ hàng |
| A5 | Cộng tác viên (CTV) | Giới thiệu nguồn nhà/khách nhận e-voucher |
| A6 | AI Agent bên thứ ba | Đọc dữ liệu qua MCP/API, gửi yêu cầu xem nhà |
| A7 | Admin / Chuyên viên MOSO | Xác thực tin, duyệt môi giới, gọi lại khách *(giả định vai trò backoffice)* |
| A8 | Ngân hàng đối tác / IEM / Urbox-Gotit | Hệ thống ngoài |

## 4. Danh sách Feature theo Module

### M1 · Tìm kiếm & Khám phá
| ID | Feature | Mô tả | Nguồn |
|---|---|---|---|
| F-01 | Danh sách mua bán | Lọc theo loại (căn hộ, nhà hẻm, mặt tiền, đất), khu vực, giá; badge "Tin xác thực", "Tin có video"; xem dạng list/lưới | /mua-ban-nha-dat |
| F-02 | Danh sách cho thuê | 9 loại: phòng trọ, căn hộ, nhà, CHDV, mặt bằng, văn phòng, kho xưởng, đất | /cho-thue-nha-dat |
| F-03 | Tìm với AI | Tìm kiếm ngôn ngữ tự nhiên ("Cơ bản" / "Tìm với AI") | / |
| F-04 | Bản đồ BĐS | Giá trên từng ghim, vẽ vùng để tìm | /mua-ban-nha-dat?xem=ban-do |
| F-05 | Trang SEO theo khu vực | Landing page theo tỉnh/quận/phường (`/ban-nha-quan-1-...`) | / |
| F-06 | Chi tiết tin đăng | Ảnh, giá, giá/m², diện tích, tầng, PN/WC, địa chỉ | listing pages |
| F-07 | Tra cứu & so sánh dự án | Lọc theo pháp lý, tiến độ, chủ đầu tư; so sánh dự án | /tim-kiem-du-an, /so-sanh-du-an |
| F-08 | Nguồn nhà đặc biệt (MOSO Signature) | BĐS đấu giá, phát mãi từ ngân hàng & Thi Hành Án, rẻ hơn 20–60% | /nguon-nha-dac-biet |
| F-09 | Yêu cầu xem nhà / tư vấn | Để lại tên + SĐT; chuyên viên gọi lại; chống trùng 24h | llms.txt (contact API) |

### M2 · Đăng tin
| F-10 | Đăng tin bán / cho thuê với AI | AI viết tiêu đề + mô tả trong ~30 giây; form riêng cho bán/thuê | /dang-tin, /dang-tin-ban-nha-dat, /dang-tin-cho-thue |
| F-11 | Quản lý "Tin của tôi" | Sửa, cập nhật giá, đánh dấu đã bán/thuê, ẩn tin, gia hạn tự động | /dang-tin-cho-thue, /mine |
| F-12 | Đẩy tin | 8h (5k), 24h + nhãn Hot (10k), 7 ngày (50k); khu vực hoặc toàn tỉnh; tối đa 3 lượt/tin/ngày | /bang-gia-dang-tin |
| F-13 | Xoá watermark ảnh bằng AI | ≤20 ảnh/lần, ≤10MB, PNG/JPG/WEBP; tô để xoá chỗ sót; versioning; tải ZIP | /cong-cu/chinh-anh-bds |
| F-14 | Ký gửi / Nhà cần bán nhanh | Chủ nhà ký gửi, môi giới nhận bán hưởng hoa hồng | /nha-dat-can-ban-nhanh |

### M3 · Xác thực & Bảo vệ ("3 THẬT")
| F-15 | Xác thực tin đăng | Kiểm tra ảnh, pháp lý, chính chủ → badge "xác thực", giảm phí 8→5 MP | llms.txt, /bang-gia-dang-tin |
| F-16 | Ẩn số nhà | Che địa chỉ chi tiết, chỉ hiện cho khách có nhu cầu thật đã xác thực; 5 MP/30 ngày | /dang-tin, /bang-gia-dang-tin |

### M4 · MOSO Points & Thanh toán
| F-17 | Ví MOSO Points | 1 MP = 1.000đ, đã gồm VAT; gói nạp từ 50.000đ; tự trừ khi gia hạn, thiếu points → ẩn số liên hệ | /chinh-sach-moso-points |
| F-18 | Kiếm points miễn phí | Quà chào mừng (+30 / +100 môi giới), điểm danh +1/ngày, nhiệm vụ hồ sơ, mốc tin xác thực, mốc follower | /chinh-sach-moso-points |

### M5 · Môi giới & Đối tác
| F-19 | Đăng ký môi giới | Tạo tài khoản bằng SĐT + OTP; hồ sơ khu vực hoạt động; admin duyệt quyền nâng cao | /register-agent, /dang-ky-moi-gioi |
| F-20 | Danh bạ môi giới & MOSO Score | Xếp hạng theo 6 yếu tố (hồ sơ, tin xác thực, review, Partner +10đ, tương tác, chứng chỉ) | /danh-ba-moi-gioi-bat-dong-san |
| F-21 | MOSO Partner (cá nhân / doanh nghiệp) | Tặng tới 1.000 points, kho hàng ngân hàng, giảm học phí 20/30%; DN được website + quản trị + đồng bộ tin 0đ | /moso-partner, /doi-tac-* |
| F-22 | Khóa học chứng chỉ môi giới | 8 buổi, MOSO × IEM, 1.990K cho Partner | /khoa-hoc-chung-chi-moi-gioi |
| F-23 | Cộng tác viên giới thiệu | E-voucher 100k/nguồn nhà bán hoặc khách, 10k/nguồn thuê; theo dõi realtime | /cong-tac-vien |
| F-24 | Workshop / sự kiện | Đăng ký sự kiện đối tác | /moso-partner-workshop |

### M6 · Tài chính & Vay
| F-25 | Vay thế chấp | So sánh lãi suất 13+ ngân hàng, đăng ký hỗ trợ hồ sơ A-Z | /vay-the-chap |
| F-26 | Bộ tính vay | Khả năng mua tối đa, DTI (ngưỡng 50%), lịch trả góp (dư nợ giảm dần / trả đều) | /cong-cu/vay-mua-nha |
| F-27 | Định giá & cầm cố | Giá trị theo giá/m² khu vực ±10%, hạn mức vay từng ngân hàng | /cong-cu/dinh-gia-cam-co-bat-dong-san |

### M7 · Công cụ BĐS (calculator)
| F-28 | Thuế & chi phí giao dịch | TNCN 2%, trước bạ 0,5%, công chứng ~0,1%; tách bên mua/bán; tiện ích Chrome/Firefox | /cong-cu/tinh-thue-giao-dich-bds |
| F-29 | Bảng giá đất nhà nước | Tra theo tỉnh/huyện/xã/đường; báo "chưa có dữ liệu" thay vì ước lượng | /cong-cu/bang-gia-dat-nha-nuoc |
| F-30 | Chuyển mục đích sử dụng đất | Theo NĐ 103/2024; tách 5 khoản chi phí | /cong-cu/chuyen-muc-dich-su-dung-dat |
| F-31 | Thuê hay mua | Chi phí ròng N năm, chi phí cơ hội | /cong-cu/thue-hay-mua-nha |
| F-32 | Lợi nhuận đầu tư | Cho thuê (gross/net yield) + flip (ROI quy năm) | /cong-cu/loi-nhuan-dau-tu-bds |
| F-33 | Hiệu quả đầu tư | So sánh BĐS/ngân hàng/chứng khoán/vàng; ROI farmstay | /cong-cu/hieu-qua-dau-tu |
| F-34 | Nên mua hay chờ | Điểm 0–100: giá khu vực 40 + lãi suất 40 + DTI 20 → MUA/CÂN NHẮC/CHỜ | /cong-cu/nen-mua-nha-hay-cho |
| F-35 | Check quy hoạch | *Sắp ra mắt* | /cong-cu |

### M8 · Dữ liệu thị trường & Nội dung
| F-36 | Báo cáo thị trường | Theo tháng/quý/năm; lệch cung–cầu theo khu vực; số liệu cập nhật mỗi giờ | /bao-cao-thi-truong-bds |
| F-37 | Tin tức & Wiki BĐS | Bài viết, thuật ngữ pháp lý (21 thuật ngữ), tiêu chuẩn biên tập, trang tác giả (E-E-A-T) | /tin-tuc-bat-dong-san, /thuat-ngu-bat-dong-san |
| F-38 | Video nhà đất | Mục video trên menu | / |

### M9 · Tương tác & Giải trí
| F-39 | Đoán giá nhà đất | 5 câu × 20s, 5 lượt/ngày, điểm theo sai lệch; Top 3 tháng nhận 200/100/50 points (≥1000 điểm) | /doan-gia-nha-dat |
| F-40 | Tử vi & Phong thủy AI | Phong thuỷ theo mệnh/hướng, xem ngày, tarot, thần số học | /tu-vi-phong-thuy |

### M10 · Tài khoản & Hỗ trợ
| F-41 | Đăng nhập / tài khoản | Đăng nhập SĐT + OTP, hồ sơ, tin nhắn | /register-agent, header |
| F-42 | Xoá tài khoản | 3 bước trong app | /huong-dan-xoa-tai-khoan |
| F-43 | Trợ giúp & phản ánh | Trung tâm trợ giúp, tiếp nhận phản ánh, cơ chế giải quyết tranh chấp | /tro-giup, footer |
| F-44 | Ứng dụng mobile | iOS + Android | /tai-ung-dung |

### M11 · AI Agent Platform (máy đọc được)
| F-45 | MCP server | Streamable HTTP, không cần auth; tools: search_listings, compare_listings, read_page, search_projects, search_agents, request_contact | /.well-known/mcp.json |
| F-46 | Agent REST API | /api/agent/search, compare, projects, agents, contact; JSON/markdown; rate limit theo IP | llms.txt |
| F-47 | Markdown content negotiation | `Accept: text/markdown` trên mọi trang, `/api/markdown?path=` (giảm ~97% token) | llms.txt |
| F-48 | llms.txt / sitemap-ai / OpenAPI 3.1 | Tài liệu cho LLM crawler | /llms.txt |

## 5. Ràng buộc đã biết
- Pháp lý: sàn TMĐT đã thông báo Bộ Công Thương; MST 0318966388; chính sách bảo mật thu thập họ tên, SĐT, email, MST, giấy tờ pháp lý.
- Địa giới hành chính sau sáp nhập 2025: `location` khớp cả tên cũ và mới.
- Giá/m² tính theo **diện tích đất**, phải đọc kèm số tầng.

## 6. Câu hỏi mở (cho PM)
- Thanh toán nạp points qua cổng nào? *(không có trong corpus)*
- Quy trình xác thực "Nhà Thật" do người hay AI thực hiện, SLA bao lâu? (Partner workshop nói "24h xác minh & kích hoạt")
- "Khách có nhu cầu thật" để mở Ẩn số nhà được định nghĩa thế nào (OTP? lịch xem?)
