MẪU KẾ HOẠCH THỰC HIỆN DỰ ÁN (BÀI TẬP LỚN)
(Dành cho học phần: [Tên môn học] - Học kỳ: ... - Năm học: ...)
Tên đề tài/dự án: [Ghi rõ tên dự án của nhóm]
Lớp học phần: ........................................ Mã nhóm: ........................................
Thông tin nhân sự nhóm:
| STT | Họ và tên | Mã sinh viên | Vai trò trong nhóm (Nhóm trưởng/Thành viên) | Nhiệm vụ chính phụ trách |
| :---: | :--- | :--- | :--- | :--- |
| 1 | [SV Nguyễn Văn A] | [MSV001] | Nhóm trưởng | Điều phối chung, Tổng hợp báo cáo, Task X |
| 2 | [SV Trần Thị B] | [MSV002] | Thành viên | Nghiên cứu tài liệu, Task Y |
| 3 | ... | ... | ... | ... |

---

# MỤC LỤC

- [MỤC LỤC](#mục-lục)
- [I. TỔNG QUAN DỰ ÁN (PROJECT OVERVIEW)](#i-tổng-quan-dự-án-project-overview)
  - [1. Lý do thực hiện dự án](#1-lý-do-thực-hiện-dự-án)
    - [1.1. Ý tưởng xuất phát từ bối cảnh thực tế](#11-ý-tưởng-xuất-phát-từ-bối-cảnh-thực-tế)
    - [1.2. Các bài toán thực tế dự án AgriSense giải quyết](#12-các-bài-toán-thực-tế-dự-án-agrisense-giải-quyết)
    - [1.3. Đối tượng khách hàng mục tiêu và đối tượng hưởng lợi](#13-đối-tượng-khách-hàng-mục-tiêu-và-đối-tượng-hưởng-lợi)
  - [2. Mục tiêu dự án theo tiêu chí SMART](#2-mục-tiêu-dự-án-theo-tiêu-chí-smart)
    - [2.1. S (Specific - Cụ thể)](#21-s-specific---cụ-thể)
    - [2.2. M (Measurable - Đo lường được)](#22-m-measurable---đo-lường-được)
    - [2.3. A (Achievable - Khả thi)](#23-a-achievable---khả-thi)
    - [2.4. R (Relevant - Thực tế)](#24-r-relevant---thực-tế)
    - [2.5. T (Time-bound - Thời hạn)](#25-t-time-bound---thời-hạn)
  - [3. Phạm vi triển khai dự án (Project Scope)](#3-phạm-vi-triển-khai-dự-án-project-scope)
    - [3.1. Các phân hệ và chức năng nằm trong phạm vi (In-Scope)](#31-các-phân-hệ-và-chức-năng-nằm-trong-phạm-vi-in-scope)
    - [3.2. Các giới hạn nằm ngoài phạm vi (Out-of-Scope)](#32-các-giới-hạn-nằm-ngoài-phạm-vi-out-of-scope)
  - [4. Yêu cầu kỹ thuật & Kiến trúc hệ thống AgriSense](#4-yêu-cầu-kỹ-thuật--kiến-trúc-hệ-thống-agrisense)
    - [4.1. Thông số môi trường công nghệ và công cụ phát triển](#41-thông-số-môi-trường-công-nghệ-và-công-cụ-phát-triển)
    - [4.2. Kiến trúc phần mềm MVT & Thiết kế 12 Model CSDL MySQL](#42-kiến-trúc-phần-mềm-mvt--thiết-kế-12-model-csdl-mysql)
- [II. KẾ HOẠCH TRIỂN KHAI VÀ PHÂN CHIA CÔNG VIỆC (WBS)](#ii-kế-hoạch-triển-khai-và-phân-chia-công-việc-wbs)
  - [1. Phân rã công việc theo 6 giai đoạn phát triển (8 tuần)](#1-phân-rã-công-việc-theo-6-giai-đoạn-phát-triển-8-tuần)
    - [1.1. Giai đoạn 1: Khởi động & Thiết lập môi trường (Tuần 1: 14/10 – 20/10/2026)](#11-giai-đoạn-1-khởi-động--thiết-lập-môi-trường-tuần-1-1410--20102026)
    - [1.2. Giai đoạn 2: Phân tích, Thiết kế hệ thống & CSDL (Tuần 2: 21/10 – 28/10/2026)](#12-giai-đoạn-2-phân-tích-thiết-kế-hệ-thống--csdl-tuần-2-2110--28102026)
    - [1.3. Giai đoạn 3: Thực thi - Xây dựng phân hệ cốt lõi (Tuần 3 - 5: 29/10 – 18/11/2026)](#13-giai-đoạn-3-thực-thi---xây-dựng-phân-hệ-cốt-lõi-tuần-3---5-2910--18112026)
    - [1.4. Giai đoạn 4: Thực thi - Tích hợp AI, QR & Dashboard (Tuần 6 - 7: 19/11 – 02/12/2026)](#14-giai-đoạn-4-thực-thi---tích-hợp-ai-qr--dashboard-tuần-6---7-1911--02122026)
    - [1.5. Giai đoạn 5: Hoàn thiện, Kiểm thử & Đóng gói sản phẩm (Tuần 8: 03/12 – 07/12/2026)](#15-giai-đoạn-5-hoàn-thiện-kiểm-thử--đóng-gói-sản-phẩm-tuần-8-0312--07122026)
    - [1.6. Giai đoạn 6: Nghiệm thu & Báo cáo trước Giảng viên (Sau Tuần 8)](#16-giai-đoạn-6-nghiệm-thu--báo-cáo-trước-giảng-viên-sau-tuần-8)
  - [2. Bảng phân rã cấu trúc công việc WBS chi tiết](#2-bảng-phân-rã-cấu-trúc-công-việc-wbs-chi-tiết)
- [III. CÁC MỐC KIỂM TRA TIẾN ĐỘ QUAN TRỌNG (MILESTONES)](#iii-các-mốc-kiểm-tra-tiến-độ-quan-trọng-milestones)
  - [Mốc 1 (Tuần 1: 14/10 – 20/10/2026): Giảng viên duyệt Tên đề tài và Bản kế hoạch](#mốc-1-tuần-1-1410--20102026-giảng-viên-duyệt-tên-đề-tài-và-bản-kế-hoạch)
  - [Mốc 2 (Tuần 4: 05/11 – 11/11/2026): Giảng viên kiểm tra tiến độ phân thô (Đạt ≥ 50%)](#mốc-2-tuần-4-0511--11112026-giảng-viên-kiểm-tra-tiến-độ-phân-thô-đạt--50)
  - [Mốc 3 (Tuần 6: 19/11 – 25/11/2026): Kiểm tra tiến độ phân hệ AI & gợi ý thông minh](#mốc-3-tuần-6-1911--25112026-kiểm-tra-tiến-độ-phân-hệ-ai--gợi-ý-thông-minh)
  - [Mốc 4 (Tuần 8: 03/12 – 07/12/2026): Hạn chót nộp toàn bộ sản phẩm và báo cáo](#mốc-4-tuần-8-0312--07122026-hạn-chót-nộp-toàn-bộ-sản-phẩm-và-báo-cáo)
- [IV. QUẢN LÝ RỦI RO (RISK MANAGEMENT)](#iv-quản-lý-rủi-ro-risk-management)
  - [1. Ma trận nhận diện và phân tích rủi ro dự án](#1-ma-trận-nhận-diện-và-phân-tích-rủi-ro-dự-án)
  - [2. Kịch bản ứng phó sự cố và phương án dự phòng an toàn](#2-kịch-bản-ứng-phó-sự-cố-và-phương-án-dự-phòng-an-toàn)
- [V. TIÊU CHÍ ĐÁNH GIÁ ĐÓNG GÓP (KPI & PEER REVIEW)](#v-tiêu-chí-đánh-giá-đóng-góp-kpi--peer-review)
  - [1. Thang đánh giá mức độ hoàn thành nhiệm vụ cá nhân (A, B, C, D)](#1-thang-đánh-giá-mức-độ-hoàn-thành-nhiệm-vụ-cá-nhân-a-b-c-d)
  - [2. Cơ chế giám sát, đánh giá chéo và công thức tính điểm cá nhân](#2-cơ-chế-giám-sát-đánh-giá-chéo-và-công-thức-tính-điểm-cá-nhân)

---

# I. TỔNG QUAN DỰ ÁN (PROJECT OVERVIEW)

## 1. Lý do thực hiện dự án

### 1.1. Ý tưởng xuất phát từ bối cảnh thực tế
Tại Việt Nam, vấn đề an toàn thực phẩm và nhu cầu sử dụng nông sản sạch, nông sản hữu cơ đạt chuẩn (VietGAP, GlobalGAP, Organic) đang trở thành mối quan tâm hàng đầu của người tiêu dùng. Tuy nhiên, thị trường phân phối nông sản trực tuyến hiện nay vẫn tồn tại nhiều rào cản và bất cập lớn:
- **Thiếu tính minh bạch về nguồn gốc xuất xứ**: Phần lớn nông sản bày bán trên các sàn thương mại điện tử tổng hợp chỉ dừng lại ở mô tả văn bản chung chung, thiếu công cụ tra cứu thông tin nhật ký canh tác, ngày thu hoạch và chứng nhận kiểm định theo từng lô hàng cụ thể.
- **Trải nghiệm mua sắm trực tuyến chưa được cá nhân hóa**: Khách hàng mua nông sản thường có nhu cầu tư vấn chuyên sâu về công dụng dinh dưỡng, cách chế biến, hướng dẫn bảo quản thực phẩm tươi sống nhưng nhân viên hỗ trợ trực tuyến không thể túc trực 24/7.
- **Kênh phân phối của nhà vườn, hợp tác xã còn manh mún**: Các hộ nông dân sản xuất nông sản an toàn gặp khó khăn trong việc xây dựng kênh bán lẻ kỹ thuật số độc lập, thiếu công cụ phân tích dữ liệu khách hàng để dự báo sản lượng và định hình chiến lược tiêu thụ bền vững.

Từ thực trạng đó, dự án **Nền tảng thương mại điện tử Nông sản tích hợp Trí tuệ nhân tạo (AgriSense Platform)** được xây dựng nhằm cung cấp giải pháp mua bán nông sản trực tuyến toàn diện, ứng dụng công nghệ Trí tuệ nhân tạo (AI), mã QR truy xuất nguồn gốc chuẩn hóa và cổng thanh toán tự động VietQR Napas 247 để tái định hình trải nghiệm tiêu dùng nông sản số.

### 1.2. Các bài toán thực tế dự án AgriSense giải quyết
1. **Minh bạch hóa chuỗi cung ứng bằng mã QR**: Mỗi lô hàng thu hoạch (`ProductBatch`) được hệ thống tự động sinh một mã QR động chuẩn ISO. Khách hàng chỉ cần quét mã bằng camera điện thoại thông minh để xem toàn bộ thông tin nông trại, vùng trồng, ngày thu hoạch, hạn dùng và chứng nhận an toàn thực phẩm mà không bắt buộc phải tải ứng dụng hay đăng nhập.
2. **Cá nhân hóa trải nghiệm thông qua AI theo dõi hành vi**: Hệ thống tự động ghi nhận nhật ký tương tác (`view`, `search`, `add_to_cart`, `purchase`, `review`) để phân nhóm khách hàng theo mô hình RFM (`new`, `interested`, `loyal`, `at_risk`, `normal`) và áp dụng thuật toán Content-based Filtering nhằm đề xuất nông sản phù hợp với khẩu vị của từng cá nhân.
3. **Thương mại đàm thoại 24/7 (Conversational Commerce)**: Chatbot AI (kết hợp mô hình ngôn ngữ lớn Gemini 1.5 Flash / Groq LLM cùng bộ luật Fallback Regex tiếng Việt chuyên sâu) giải đáp mọi thắc mắc về nông sản và đặc biệt là khả năng nhận diện ý định đặt hàng trực tiếp bằng câu lệnh tự nhiên, tự động trừ kho an toàn và sinh mã VietQR thanh toán ngay trong cửa sổ chat.
4. **Thanh toán không tiền mặt tiện lợi qua VietQR Napas 247**: Tích hợp chuẩn VietQR động với mã ngân hàng MBBank, tự động điền chính xác số tiền đơn hàng và nội dung chuyển khoản là mã định danh đơn hàng (`ORDxxxxxxxx`), triệt tiêu hoàn toàn rủi ro sai sót thông tin chuyển khoản.
5. **Tối ưu hóa năng lực quản trị kinh doanh**: Cung cấp Dashboard trực quan hóa dữ liệu theo thời gian thực với biểu đồ đường xu hướng doanh thu 30 ngày, biểu đồ tròn cơ cấu nhóm khách hàng AI, biểu đồ cột nông sản bán chạy và tính năng xuất file Excel báo cáo doanh thu (`.xlsx`) chuyên nghiệp.

### 1.3. Đối tượng khách hàng mục tiêu và đối tượng hưởng lợi
- **Người tiêu dùng thông thái (End Customers)**: Các cá nhân, gia đình trẻ tại đô thị có nhu cầu tiêu dùng nông sản sạch, rau củ quả an toàn, mong muốn kiểm tra tường tận nguồn gốc và nhận được sự tư vấn chu đáo, cá nhân hóa.
- **Hộ nông dân, Hợp tác xã (HTX) và Nhà cung cấp nông sản sạch**: Sở hữu kênh giới thiệu sản phẩm trực tuyến bài bản, minh bạch hóa chất lượng canh tác, mở rộng tập khách hàng mà không phụ thuộc vào thương lái trung gian.
- **Đội ngũ Quản trị viên & Nhân viên vận hành (Store Admins & Staff)**: Có công cụ quản lý tập trung toàn diện từ kho hàng, lô hàng, trạng thái đơn hàng đến biểu đồ phân tích hành vi người tiêu dùng.
- **Bản thân sinh viên thực hiện dự án**: Trực tiếp làm chủ quy trình phát triển phần mềm hiện đại từ phân tích yêu cầu, thiết kế kiến trúc hệ thống (UML, ERD), lập trình hướng dịch vụ Django MVT, quản trị CSDL MySQL, tích hợp API AI tiên tiến đến kiểm thử tự động toàn diện.

---

## 2. Mục tiêu dự án theo tiêu chí SMART

### 2.1. S (Specific - Cụ thể)
Xây dựng hoàn chỉnh nền tảng web thương mại điện tử chuyên biệt cho nông sản (AgriSense Platform) hoạt động ổn định trên môi trường máy chủ cục bộ (Django Development Server kết nối MySQL Server). Nền tảng tích hợp 4 nhóm nghiệp vụ chính:
1. **Bán hàng & Thanh toán số VietQR Napas 247**: Quản lý tài khoản, danh mục, giỏ hàng, đặt hàng giao dịch nguyên tử `@transaction.atomic`, hủy đơn hoàn kho tự động và sinh mã VietQR động.
2. **Trí tuệ nhân tạo (AI)**: Ghi nhận hành vi đa sự kiện, phân nhóm khách hàng RFM 5 mức, động cơ gợi ý Content-based Filtering và Chatbot AI đàm thoại lên đơn hàng trực tiếp bằng ngôn ngữ tự nhiên.
3. **Truy xuất nguồn gốc lô hàng bằng mã QR**: Sinh mã QR PNG chuẩn ISO trỏ về trang thông tin công khai không cần đăng nhập.
4. **Quản trị kinh doanh Dashboard**: Bảo mật phân quyền nghiêm ngặt `@staff_member_required`, 3 biểu đồ tương tác Chart.js (đường, tròn, cột) và công cụ xuất file Excel báo cáo đơn hàng (`.xlsx`) chuyên nghiệp qua thư viện `openpyxl`.

### 2.2. M (Measurable - Đo lường được)
Hệ thống được định lượng bằng các chỉ số kỹ thuật và kết quả nghiệm thu cụ thể sau:
- **Kiến trúc CSDL**: Chuẩn hóa gồm 12 model cốt lõi tạo thành 26 bảng dữ liệu hệ thống trên MySQL Server Community 26.7.0.
- **Khối lượng tính năng**: Xây dựng thành công 8 phân hệ ứng dụng (apps) với hơn 25 tính năng nghiệp vụ hoàn chỉnh.
- **Kho dữ liệu mẫu (Seed Data)**: Tự động khởi tạo 6 danh mục, 7 nhà cung cấp, 32 sản phẩm nông sản, 24 khách hàng mẫu, 52 đơn hàng, 11 lô hàng có mã QR và 165 sự kiện tương tác.
- **Kiểm thử tự động**: Đạt 100% tỷ lệ PASS cho 43/43 Unit Tests (`django.test.TestCase`) bao quát mọi luồng nghiệp vụ chính (0 errors, 0 failures).
- **Độ chính xác Chatbot**: Đạt độ chính xác ≥ 90% trên bộ test kịch bản hội thoại và thời gian phản hồi dự phòng Fallback tức thời (< 1.5 giây).
- **Hồ sơ bàn giao**: Đầy đủ mã nguồn GitHub, tài liệu hướng dẫn kỹ thuật `README.md`, nhật ký tiến độ 8 tuần `NHAT_KY_DU_AN.md` và file báo cáo Word/PDF định dạng chuẩn.

### 2.3. A (Achievable - Khả thi)
Dự án hoàn toàn khả thi nhờ vào năng lực kỹ thuật và nguồn tài nguyên hiện có:
- Nhóm sinh viên đã hoàn thành các học phần nền tảng về Lập trình Python, Công nghệ Web, Cơ sở dữ liệu quan hệ và Phân tích thiết kế hệ thống.
- Toàn bộ công nghệ sử dụng là mã nguồn mở ổn định (Django 6.1.2, MySQL 26.7.0, Bootstrap 5.3.3, Chart.js, openpyxl, qrcode, Pillow).
- Chatbot AI tích hợp API miễn phí (Gemini 1.5 Flash / Groq) kết hợp giải pháp Rule-based Fallback bằng Regex độc lập đảm bảo hệ thống không bị phụ thuộc vào kết nối mạng bên ngoài.
- Khối lượng công việc 8 tuần được phân bổ khoa học (khoảng 25-30 giờ làm việc/tuần).

### 2.4. R (Relevant - Thực tế)
Dự án gắn liền trực tiếp với chuẩn đầu ra (CLOs) của học phần Công nghệ Phần mềm / Hệ thống Thông tin:
- Vận dụng thành thạo mô hình phân tích thiết kế phần mềm hướng đối tượng (Use Case, Activity, Class, Sequence Diagram, ERD).
- Thiết kế kiến trúc MVT chuẩn hóa và tối ưu hóa truy vấn CSDL quan hệ với chỉ mục (indexes).
- Ứng dụng kỹ thuật AI/ML giải quyết bài toán nghiệp vụ thương mại điện tử thực tế.
- Nâng cao năng lực kiểm thử phần mềm tự động và tài liệu hóa dự án chuyên nghiệp. Sản phẩm có khả năng phát triển mở rộng thành Đồ án tốt nghiệp đại học.

### 2.5. T (Time-bound - Thời hạn)
- **Thời gian thực hiện**: Từ ngày 14/10/2026 đến ngày 07/12/2026 (Tổng cộng 8 tuần làm việc).
- **Hạn chót nộp toàn bộ sản phẩm và báo cáo**: Ngày 07/12/2026.
- **Thời gian bảo vệ**: Theo lịch xếp của Giảng viên hướng dẫn và Bộ môn.

---

## 3. Phạm vi triển khai dự án (Project Scope)

### 3.1. Các phân hệ và chức năng nằm trong phạm vi (In-Scope)
- **Phân hệ Quản lý tài khoản (`accounts`)**: Đăng ký, đăng nhập bảo mật Django Auth, quản lý hồ sơ và sổ địa chỉ giao hàng linh hoạt.
- **Phân hệ Danh mục & Sản phẩm (`products`)**: Phân loại rau củ, trái cây, gạo, đặc sản; tìm kiếm tiếng Việt; bộ lọc đa tiêu chí; đánh giá sao kèm nhận xét.
- **Phân hệ Giỏ hàng & Đơn hàng (`cart_orders`)**: Giỏ hàng theo phiên, tính phí giao hàng thông minh (30.000đ, miễn phí từ 500.000đ), trừ tồn kho trong giao dịch `@transaction.atomic`, hủy đơn hoàn tồn kho tự động.
- **Cổng thanh toán tự động VietQR Napas 247**: Sinh mã VietQR động theo chuẩn ngân hàng MBBank, nhúng mã đơn hàng và số tiền chính xác trên trang đơn và trong chat.
- **Phân hệ Hành vi & Gợi ý (`behavior` & `recommendation`)**: Ghi nhận 6 loại sự kiện (`view`, `search`, `add_to_cart`, `purchase`, `review`, `chat`); phân nhóm khách hàng RFM; gợi ý nông sản theo thuật toán Content-based Filtering.
- **Phân hệ Chatbot AI & Đặt hàng đàm thoại (`chatbot`)**: Tích hợp Gemini 1.5 Flash / Groq LLM; Fallback regex tiếng Việt; tự động chốt đơn hàng và sinh VietQR tức thời qua tin nhắn chat.
- **Phân hệ Truy xuất nguồn gốc (`traceability`)**: Tự động tạo mã QR PNG chuẩn ISO cho từng lô hàng (`ProductBatch`); trang tra cứu thông tin canh tác công khai không cần đăng nhập.
- **Phân hệ Dashboard Quản trị (`dashboard`)**: Phân quyền `@staff_member_required`; 3 biểu đồ tương tác Chart.js; công cụ xuất báo cáo danh sách đơn hàng ra file Excel (`.xlsx`).

### 3.2. Các giới hạn nằm ngoài phạm vi (Out-of-Scope)
- **Ứng dụng di động Native (iOS/Android)**: Hệ thống tập trung tối ưu hóa giao diện Web Responsive bằng Bootstrap 5.3 tương thích mượt mà trên trình duyệt di động.
- **Cổng thanh toán thẻ quốc tế thanh toán trực tiếp qua Visa/Mastercard** đòi hỏi pháp nhân doanh nghiệp và chi phí đăng ký cổng trung gian (hệ thống sử dụng cổng VietQR Napas 247 và COD hoàn hảo cho bài toán thực tế).
- **Triển khai hạ tầng Cloud phân tán Kubernetes / Microservices quy mô lớn**: Dự án tập trung tối ưu hóa kiến trúc nguyên khối theo mô-đun (Modular Monolith) chạy ổn định trên môi trường máy chủ cục bộ.

---

## 4. Yêu cầu kỹ thuật & Kiến trúc hệ thống AgriSense

### 4.1. Thông số môi trường công nghệ và công cụ phát triển

| Thành phần kỹ thuật | Công nghệ / Phiên bản | Vai trò và đặc tả trong hệ thống |
| :--- | :--- | :--- |
| **Hệ điều hành** | Windows 11 Pro (64-bit) | Môi trường phát triển và kiểm thử chuẩn của dự án |
| **Ngôn ngữ lập trình** | Python 3.14.3 | Nền tảng thực thi logic chính của hệ thống Backend |
| **Web Framework** | Django 6.1.2 | Kiến trúc MVT, bảo mật CSRF, ORM, URL Routing |
| **Hệ quản trị CSDL** | MySQL Community Server 26.7.0 | Lưu trữ dữ liệu quan hệ, bảng mã `utf8mb4_0900_ai_ci` |
| **Database Driver** | PyMySQL 1.2.3 | Kết nối thuần Python tương thích hoàn hảo Python 3.14 |
| **Giao diện người dùng** | Bootstrap 5.3.3 & Bootstrap Icons | Xây dựng UI Responsive thích ứng đa kích thước màn hình |
| **Trực quan hóa dữ liệu** | Chart.js 4.4 | Hiển thị biểu đồ tương tác thời gian thực trên Dashboard |
| **Xuất file báo cáo** | openpyxl 3.1.5 | Sinh file Excel (.xlsx) danh sách đơn hàng có định dạng chuẩn |
| **Mã QR & Hình ảnh** | qrcode 7.4.2 & Pillow 11.0.0 | Sinh ảnh mã QR ISO cho từng lô nông sản thu hoạch |
| **Mô hình AI & LLM** | Google Gemini 1.5 Flash / Groq Cloud | Trí tuệ nhân tạo đàm thoại và phân tích ngữ cảnh |

### 4.2. Kiến trúc phần mềm MVT & Thiết kế 12 Model CSDL MySQL
AgriSense được cấu trúc theo mô hình kiến trúc Django MVT (Model - View - Template) hướng mô-đun hóa cao, phân chia rõ ràng trách nhiệm nghiệp vụ giữa các tầng:
- **Tầng Dữ liệu (Model & CSDL)**: 12 Model chuẩn hóa bao gồm `accounts.User`, `accounts.UserAddress`, `products.Category`, `products.Supplier`, `products.Product`, `products.ProductReview`, `cart_orders.Cart`, `cart_orders.CartItem`, `cart_orders.Order`, `cart_orders.OrderItem`, `behavior.UserEvent`, `behavior.UserSegment`, `chatbot.ChatSession`, `chatbot.ChatMessage`, `traceability.ProductBatch`, `traceability.TraceabilityRecord`.
- **Tầng Xử lý nghiệp vụ (Services & Views)**: Phân tách logic đặt hàng, tính cước giao hàng, tạo mã VietQR, gợi ý sản phẩm và chốt đơn chat vào các module services chuyên biệt.
- **Tầng Bảo mật & Giao vận**: Áp dụng `@transaction.atomic` cho mọi thao tác tác động tồn kho; mã hóa mật khẩu PBKDF2; middleware bắt buộc kiểm tra phân quyền truy cập `staff_member_required`.

---

# II. KẾ HOẠCH TRIỂN KHAI VÀ PHÂN CHIA CÔNG VIỆC (WBS)

## 1. Phân rã công việc theo 6 giai đoạn phát triển (8 tuần)

### 1.1. Giai đoạn 1: Khởi động & Thiết lập môi trường (Tuần 1: 14/10 – 20/10/2026)
- Nghiên cứu thị trường thương mại điện tử nông sản, khảo sát 5 website hiện có, xác định bài toán cốt lõi và lập bản đề xuất đề tài.
- Thiết lập môi trường phát triển: Cài đặt Python 3.14.3, MySQL Server 26.7.0, Django 6.1.2, PyMySQL, Git và VS Code.
- Khởi tạo kho mã nguồn GitHub, cấu hình `.gitignore` bảo vệ file bảo mật `.env` và kết nối thành công Django với MySQL Database `nongsan_db`.

### 1.2. Giai đoạn 2: Phân tích, Thiết kế hệ thống & CSDL (Tuần 2: 21/10 – 28/10/2026)
- Xây dựng hồ sơ thiết kế kỹ thuật: Sơ đồ Use Case toàn hệ thống, Activity Diagram luồng đặt hàng, Class Diagram cấu trúc mô hình dữ liệu, Sequence Diagram luồng AI Chatbot và ERD 12 bảng CSDL.
- Thiết kế wireframe giao diện khách hàng và bảng điều khiển quản trị Dashboard.
- Khởi tạo mã nguồn Model Django và thực thi `makemigrations`, `migrate` tạo 26 bảng dữ liệu trong MySQL.

### 1.3. Giai đoạn 3: Thực thi - Xây dựng phân hệ cốt lõi (Tuần 3 - 5: 29/10 – 18/11/2026)
- **Tuần 3 (29/10 – 04/11)**: Xây dựng phân hệ tài khoản (`accounts`) và phân hệ duyệt danh mục, tìm kiếm, lọc và chi tiết nông sản (`products`).
- **Tuần 4 (05/11 – 11/11)**: Xây dựng phân hệ giỏ hàng, dịch vụ đặt hàng COD/Chuyển khoản, tích hợp thanh toán VietQR Napas 247 tự động, quản lý lịch sử đơn hàng và tính năng hủy đơn hoàn kho (`cart_orders`).
- **Tuần 5 (12/11 – 18/11)**: Thiết kế hệ thống giao diện chuẩn Bootstrap 5.3.3 responsive và triển khai `BehaviorTrackingMiddleware` tự động ghi nhận hành vi tìm kiếm và xem sản phẩm của người dùng.

### 1.4. Giai đoạn 4: Thực thi - Tích hợp AI, QR & Dashboard (Tuần 6 - 7: 19/11 – 02/12/2026)
- **Tuần 6 (19/11 – 25/11)**: Triển khai thuật toán phân loại khách hàng RFM (`new`, `interested`, `loyal`, `at_risk`, `normal`), lệnh quản trị `update_segments` và động cơ gợi ý sản phẩm cá nhân hóa Content-based Filtering.
- **Tuần 7 (26/11 – 02/12)**: Xây dựng Chatbot AI tư vấn nông sản (Gemini/Groq API + Fallback Regex tiếng Việt đa từ khóa), tính năng lên đơn hàng đàm thoại trực tiếp; triển khai sinh mã QR PNG lô hàng (`traceability`) và Dashboard quản trị kinh doanh Chart.js có xuất file Excel.

### 1.5. Giai đoạn 5: Hoàn thiện, Kiểm thử & Đóng gói sản phẩm (Tuần 8: 03/12 – 07/12/2026)
- Xây dựng lệnh `seed_data` khởi tạo trọn bộ dữ liệu thực tế mẫu; viết và thực thi 43/43 Unit Tests đạt tỷ lệ thành công 100%.
- Rà soát bảo mật file biến môi trường `.env`, hoàn thiện tài liệu hướng dẫn kỹ thuật `README.md` và biên soạn Báo cáo tổng kết dự án bản Word/PDF.

### 1.6. Giai đoạn 6: Nghiệm thu & Báo cáo trước Giảng viên (Sau Tuần 8)
- Thiết kế slide thuyết trình, quay video demo kịch bản nghiệp vụ dự phòng và chuẩn bị bộ câu hỏi vấn đáp (Q&A) bảo vệ đồ án.
- Báo cáo và thuyết minh trực tiếp sản phẩm trước Giảng viên hướng dẫn và Hội đồng chấm thi.

---

## 2. Bảng phân rã cấu trúc công việc WBS chi tiết

| STT | Giai đoạn & Công việc cụ thể | Người phụ trách | Thời gian bắt đầu | Thời gian kết thúc | Kết quả đầu ra dự kiến (Deliverables) | Trạng thái |
| :---: | :--- | :---: | :---: | :---: | :--- | :---: |
| **1** | **GIAI ĐOẠN 1: KHỞI ĐỘNG & THIẾT LẬP MÔI TRƯỜNG** | **Cả nhóm** | **14/10/2026** | **20/10/2026** | **Môi trường dev & Kho mã nguồn** | **Hoàn thành** |
| 1.1 | Họp nhóm, chọn đề tài, xác định phạm vi & tiêu chí SMART | Cả nhóm | 14/10/2026 | 16/10/2026 | Biên bản họp nhóm số 1 & Bản phạm vi | Hoàn thành |
| 1.2 | Lập và nộp Kế hoạch thực hiện dự án (WBS) | Nhóm trưởng | 17/10/2026 | 18/10/2026 | File Kế hoạch dự án (Word/PDF) | Hoàn thành |
| 1.3 | Cài đặt môi trường Python 3.14, MySQL 26.7, Django 6.1 | Cả nhóm | 19/10/2026 | 20/10/2026 | Mã nguồn khung kết nối CSDL thành công | Hoàn thành |
| **2** | **GIAI ĐOẠN 2: THIẾT KẾ HỆ THỐNG & CSDL** | **Cả nhóm** | **21/10/2026** | **28/10/2026** | **Hồ sơ thiết kế & Migration MySQL** | **Hoàn thành** |
| 2.1 | Vẽ 5 sơ đồ UML (Use Case, Activity, Class, Sequence, ERD) | Thành viên A, B | 21/10/2026 | 24/10/2026 | Bộ sơ đồ UML chuẩn hóa | Hoàn thành |
| 2.2 | Thiết kế 12 Model Django và chạy Migration vào MySQL | Nhóm trưởng | 25/10/2026 | 26/10/2026 | 26 bảng dữ liệu trong nongsan_db | Hoàn thành |
| 2.3 | Thiết kế Wireframe giao diện khách hàng & Dashboard | Thành viên B | 27/10/2026 | 28/10/2026 | Bản vẽ Wireframe UI/UX | Hoàn thành |
| **3** | **GIAI ĐOẠN 3: PHÁT TRIỂN PHÂN HỆ CỐT LÕI** | **Cả nhóm** | **29/10/2026** | **18/11/2026** | **Mã nguồn cốt lõi Bán hàng & UI** | **Hoàn thành** |
| 3.1 | Phân hệ Tài khoản (accounts) & Sổ địa chỉ giao hàng | Thành viên A | 29/10/2026 | 04/11/2026 | Module đăng ký/đăng nhập/profile | Hoàn thành |
| 3.2 | Phân hệ Danh mục, Sản phẩm, Tìm kiếm & Đánh giá sao | Thành viên B | 05/11/2026 | 11/11/2026 | Trang duyệt & chi tiết nông sản | Hoàn thành |
| 3.3 | Phân hệ Giỏ hàng, Đặt hàng atomic & Cổng VietQR Napas | Nhóm trưởng | 08/11/2026 | 14/11/2026 | Dịch vụ đặt hàng & sinh mã VietQR | Hoàn thành |
| 3.4 | Xây dựng Giao diện Bootstrap 5.3 & Middleware hành vi | Cả nhóm | 12/11/2026 | 18/11/2026 | Bộ giao diện UI responsive & logs | Hoàn thành |
| **4** | **GIAI ĐOẠN 4: TÍCH HỢP AI, QR & DASHBOARD** | **Cả nhóm** | **19/11/2026** | **02/12/2026** | **Phân hệ AI, QR và Dashboard** | **Hoàn thành** |
| 4.1 | Phân nhóm khách hàng RFM & Động cơ gợi ý Content-based | Nhóm trưởng | 19/11/2026 | 25/11/2026 | Module segmentation & recommendation | Hoàn thành |
| 4.2 | Chatbot AI (Gemini/Groq + Fallback) & Lên đơn qua chat | Thành viên A | 26/11/2026 | 29/11/2026 | Widget Chatbot tư vấn & chốt đơn | Hoàn thành |
| 4.3 | Sinh mã QR PNG lô hàng & Trang tra cứu nguồn gốc | Thành viên B | 30/11/2026 | 01/12/2026 | Module QR & Public trace page | Hoàn thành |
| 4.4 | Dashboard Quản trị Chart.js & Xuất báo cáo Excel .xlsx | Nhóm trưởng | 01/12/2026 | 02/12/2026 | Trang Dashboard 6 màn hình | Hoàn thành |
| **5** | **GIAI ĐOẠN 5: HOÀN THIỆN, KIỂM THỬ & ĐÓNG GÓI** | **Cả nhóm** | **03/12/2026** | **07/12/2026** | **Hệ thống hoàn chỉnh & Tài liệu** | **Hoàn thành** |
| 5.1 | Lệnh seed_data mẫu & Xây dựng bộ 43 Unit Tests tự động | Nhóm trưởng | 03/12/2026 | 05/12/2026 | Bộ dữ liệu mẫu & 43 tests PASS | Hoàn thành |
| 5.2 | Biên soạn README, NHAT_KY_DU_AN & Báo cáo tổng kết | Cả nhóm | 06/12/2026 | 07/12/2026 | File Báo cáo Word/PDF & README | Hoàn thành |
| **6** | **GIAI ĐOẠN 6: NGHIỆM THU & BẢO VỆ DỰ ÁN** | **Cả nhóm** | **Sau 07/12** | **Theo lịch GV** | **Slide, Video Demo & Buổi bảo vệ** | **Sẵn sàng** |

---

# III. CÁC MỐC KIỂM TRA TIẾN ĐỘ QUAN TRỌNG (MILESTONES)

## Mốc 1 (Tuần 1: 14/10 – 20/10/2026): Giảng viên duyệt Tên đề tài và Bản kế hoạch
- **Nội dung kiểm tra**: Giảng viên duyệt Tên đề tài, tính cấp thiết, phạm vi thực hiện và Bản kế hoạch thực hiện dự án này.
- **Sản phẩm cần đạt**: Bản Kế hoạch thực hiện dự án chi tiết (WBS, SMART, phân chia công việc), biên bản họp nhóm số 1 và kho mã nguồn GitHub khởi tạo kết nối MySQL.

## Mốc 2 (Tuần 4: 05/11 – 11/11/2026): Giảng viên kiểm tra tiến độ phân thô (Đạt ≥ 50%)
- **Nội dung kiểm tra**: Giảng viên kiểm tra tiến độ phần thô (Đạt tối thiểu 50% khối lượng công việc theo cam kết).
- **Sản phẩm cần đạt**: Mô hình CSDL MySQL 12 bảng đã migrate hoàn tất; phân hệ Tài khoản (`accounts`), Sản phẩm (`products`), và Giỏ hàng - Đặt hàng (`cart_orders`) hoạt động trơn tru trên Localhost.

## Mốc 3 (Tuần 6: 19/11 – 25/11/2026): Kiểm tra tiến độ phân hệ AI & gợi ý thông minh
- **Nội dung kiểm tra**: Giảng viên kiểm tra việc triển khai thuật toán phân nhóm khách hàng RFM và động cơ gợi ý sản phẩm cá nhân hóa.
- **Sản phẩm cần đạt**: Lệnh quản trị `update_segments` phân bổ chính xác 5 nhóm khách hàng; giao diện hiển thị danh mục sản phẩm gợi ý cá nhân hóa dựa trên lịch sử tương tác của người dùng.

## Mốc 4 (Tuần 8: 03/12 – 07/12/2026): Hạn chót nộp toàn bộ sản phẩm và báo cáo
- **Nội dung kiểm tra**: Hạn chót nộp toàn bộ sản phẩm hoàn chỉnh, mã nguồn và báo cáo cuối cùng lên hệ thống quản lý học tập.
- **Sản phẩm cần đạt**: Toàn bộ mã nguồn trên GitHub, bộ 43 Unit Tests đạt 100% PASS, Báo cáo dự án Word/PDF hoàn chỉnh, Slide thuyết trình và Video demo kịch bản nghiệp vụ.

---

# IV. QUẢN LÝ RỦI RO (RISK MANAGEMENT)

## 1. Ma trận nhận diện và phân tích rủi ro dự án

| Tình huống rủi ro có thể xảy ra | Mức độ ảnh hưởng (Cao/Vừa/Thấp) | Giải pháp phòng ngừa / Xử lý của nhóm |
| :--- | :---: | :--- |
| **Thành viên gặp sự cố sức khỏe, trễ deadline hoặc bận việc đột xuất.** | **Cao** | Thiết lập deadline nội bộ sớm hơn hạn của Giảng viên 3 ngày. Nhóm trưởng chủ động điều phối chia nhỏ task hỗ trợ chéo hoặc báo cáo sớm nếu có khó khăn phát sinh. |
| **Máy tính hỏng hóc, lỗi phần cứng hoặc mất mát mã nguồn.** | **Cao** | Áp dụng quy tắc quản lý mã nguồn nghiêm ngặt: Commit và Push code lên GitHub tối thiểu 2 lần/tuần; toàn bộ tài liệu báo cáo lưu trữ đồng bộ trên Google Drive dùng chung của nhóm. |
| **Xung đột phiên bản môi trường mới (Python 3.14.3 và MySQL 26.7.0 thiếu wheel biên dịch C++).** | **Cao** | Sử dụng driver PyMySQL thuần Python thay cho mysqlclient; cấu hình `pymysql.install_as_MySQLdb()` trong `nongsan_project/__init__.py`; đóng gói `requirements.txt` chuẩn xác. |
| **API AI của bên thứ ba (Gemini/Groq) bị gián đoạn mạng, hết quota hoặc tăng độ trễ.** | **Vừa** | Xây dựng hệ thống dự phòng kép (Dual-layer Fallback): Nếu API ngoại tuyến hoặc timeout sau 10 giây, cơ chế Fallback Regex tiếng Việt tự động kích hoạt trả lời ngay lập tức. |
| **Dữ liệu hành vi người dùng ban đầu quá ít (Vấn đề Cold Start) khiến AI khó phân nhóm và gợi ý.** | **Vừa** | Viết lệnh `seed_data` tự động khởi tạo 24 khách hàng mẫu, 165 sự kiện tương tác và 52 đơn hàng; kết hợp cơ chế fallback tự động gợi ý sản phẩm bán chạy/thịnh hành khi thiếu dữ liệu. |
| **Rủi ro sai lệch dữ liệu tồn kho khi nhiều khách hàng cùng đặt hàng một lúc.** | **Vừa** | Sử dụng giao dịch nguyên tử `@transaction.atomic` và cơ chế kiểm tra lại tồn kho tức thời tại thời điểm chốt đơn để bảo đảm tính toàn vẹn dữ liệu. |
| **Mất kết nối Internet khi báo cáo và trình diễn trực tiếp trước Giảng viên.** | **Thấp** | Hệ thống được thiết kế chạy 100% trên Localhost; chuẩn bị sẵn video quay màn hình toàn bộ các kịch bản demo và bộ luật Chatbot Fallback hoạt động offline hoàn toàn. |

## 2. Kịch bản ứng phó sự cố và phương án dự phòng an toàn
1. **Dự phòng dữ liệu**: Cơ sở dữ liệu MySQL được sao lưu định kỳ bằng lệnh `mysqldump` hàng tuần vào thư mục riêng; mã nguồn được sao lưu trên kho GitHub cá nhân.
2. **Dự phòng trình diễn**: Video demo chất lượng cao 1080p bao quát 100% các tính năng (từ duyệt sản phẩm, quét mã QR lô hàng, đặt hàng VietQR, đến Chatbot AI và Dashboard) được chuẩn bị sẵn trong USB và tải lên Google Drive để phát ngay nếu gặp trục trặc thiết bị.

---

# V. TIÊU CHÍ ĐÁNH GIÁ ĐÓNG GÓP (KPI & PEER REVIEW)

Để đảm bảo tính công bằng, minh bạch và triệt tiêu triệt để tình trạng "gánh tạ / núp bóng" trong quá trình làm việc nhóm, khi kết thúc dự án các thành viên sẽ tiến hành họp đánh giá chéo (Peer Review) lẫn nhau theo thang điểm % đóng góp thực tế:

## 1. Thang đánh giá mức độ hoàn thành nhiệm vụ cá nhân (A, B, C, D)
- **Mức A (90% – 100%)**: Hoàn thành xuất sắc toàn bộ khối lượng công việc được phân công đúng hạn hoặc sớm hơn kế hoạch; chất lượng code sạch sẽ, có kiểm thử đầy đủ; chủ động hỗ trợ các thành viên khác tháo gỡ vướng mắc kỹ thuật và đóng góp nhiều sáng kiến giá trị cho đề tài.
- **Mức B (70% – 89%)**: Hoàn thành đầy đủ các đầu việc được giao đúng hạn; sản phẩm đạt yêu cầu nghiệp vụ cơ bản; có tinh thần trách nhiệm và phối hợp tốt với nhóm nhưng ít có đề xuất sáng tạo bổ sung.
- **Mức C (50% – 69%)**: Hoàn thành công việc được giao nhưng thường xuyên chậm tiến độ, chất lượng sản phẩm còn nhiều lỗi, phải để các thành viên khác hỗ trợ sửa đổi hoặc làm lại đáng kể.
- **Mức D (< 50%)**: Không hoàn thành nhiệm vụ được giao hoặc khối lượng đóng góp không đáng kể (< 50% yêu cầu); thiếu tinh thần hợp tác, không tham gia các buổi họp nhóm và kiểm tra tiến độ.

## 2. Cơ chế giám sát, đánh giá chéo và công thức tính điểm cá nhân
- **Công thức quy đổi điểm số**:
  $$\text{Điểm số cuối cùng của sinh viên} = \text{Điểm tổng của nhóm do Giảng viên chấm} \times \% \text{Đóng góp cá nhân}$$
- **Quy chế làm việc nội bộ nhóm**:
  1. Biên bản họp nhóm định kỳ được lập vào cuối mỗi tuần, ghi nhận rõ ràng tiến độ của từng thành viên và những trở ngại cần giải quyết.
  2. Mỗi thành viên có trách nhiệm tự kiểm thử (Self-test) phần việc của mình trước khi tích hợp vào nhánh chính trên GitHub.
  3. Bảng tổng kết tỷ lệ phần trăm đóng góp phải có chữ ký xác nhận đồng thuận của 100% thành viên trong nhóm trước khi nộp chính thức lên Giảng viên.
