| BỘ GIÁO DỤC VÀ ĐÀO TẠO  TRƯỜNG ĐẠI HỌC CÔNG NGHỆ ĐÔNG Á  https://upload.wikimedia.org/wikipedia/vi/a/a1/Logo_%C4%90%E1%BA%A1i_h%E1%BB%8Dc_C%C3%B4ng_ngh%E1%BB%87_%C4%90%C3%B4ng_%C3%81.png  ĐỀ CƯƠNG BÀI TẬP LỚN  Môn: Đồ án chuyên ngành Công nghệ phần mềm  TÊN ĐỀ BÀI TẬP LỚN: WEBSITE BÁN NÔNG SẢN TÍCH HỢP AI (AGRISENSE PLATFORM)  Mã sinh viên   | Tên sinh viên   | Lớp hành chính   |
| :--- | :--- | :--- |
| **20234070** | **Nguyễn Hồng Hoàng** | **DCCNTT 14.10** |

**Người hướng dẫn**: ThS. Mai Văn Linh  
**Bắc Ninh, 2026**

---

# LỜI CẢM ƠN

Trước tiên, em xin gửi lời bày tỏ lòng biết ơn sâu sắc nhất tới Ban Giám hiệu, Khoa Công nghệ Thông tin - Trường Đại học Công nghệ Đông Á đã tạo mọi điều kiện thuận lợi và xây dựng môi trường học tập, nghiên cứu chuyên nghiệp cho chúng em trong suốt quá trình theo học học phần **Đồ án chuyên ngành Công nghệ phần mềm**.

Đặc biệt, em xin bày tỏ lòng kính trọng và biết ơn sâu sắc nhất tới **ThS. Mai Văn Linh** – Giảng viên hướng dẫn trực tiếp. Thầy đã dành nhiều thời gian quý báu để tận tình định hướng đề tài, gợi mở các giải pháp công nghệ tiên tiến, chỉ bảo tỉ mỉ về phương pháp nghiên cứu khoa học cũng như giải quyết các rào cản kỹ thuật phức tạp trong suốt quá trình xây dựng Đề cương và hiện thực hóa dự án **AgriSense Platform**.

Mặc dù đã có nhiều nỗ lực và nghiêm túc trong quá trình nghiên cứu, xây dựng hệ thống, song do giới hạn về mặt thời gian và kinh nghiệm thực tiễn, bản Đề cương Bài tập lớn chắc chắn không tránh khỏi những thiếu sót nhất định. Kính mong nhận được sự góp ý quý báu của Thầy và Hội đồng thẩm định để đề tài được hoàn thiện một cách trọn vẹn và đạt kết quả cao nhất.

---

# MỤC LỤC

- [LỜI CẢM ƠN](#lời-cảm-ơn)
- [MỤC LỤC](#mục-lục)
- [DANH MỤC CÁC TỪ VIẾT TẮT](#danh-mục-các-từ-viết-tắt)
- [DANH MỤC CÁC BẢNG](#danh-mục-các-bảng)
- [DANH MỤC CÁC HÌNH VẼ](#danh-mục-các-hình-vẽ)
- [MỞ ĐẦU](#mở-đầu)
  - [1.1. Lý do chọn đề tài](#11-lý-do-chọn-đề-tài)
  - [1.2. Mục tiêu của đề tài](#12-mục-tiêu-của-đề-tài)
  - [1.3. Nội dung và phạm vi nghiên cứu](#13-nội-dung-và-phạm-vi-nghiên-cứu)
  - [1.4. Đóng góp của đề tài](#14-đóng-góp-của-đề-tài)
  - [1.5. Cấu trúc của Đề cương Bài tập lớn](#15-cấu-trúc-của-đề-cương-bài-tập-lớn)
- [CHƯƠNG 1. CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ NÔNG SẢN TÍCH HỢP AI](#chương-1-cơ-sở-lý-thuyết-và-tổng-quan-hệ-thống-thương-mại-điện-tử-nông-sản-tích-hợp-ai)
  - [1.1. Cơ sở lý luận về thương mại điện tử trong chuỗi cung ứng nông sản sạch](#11-cơ-sở-lý-luận-về-thương-mại-điện-tử-trong-chuỗi-cung-ứng-nông-sản-sạch)
    - [1.1.1. Khái niệm, vai trò và xu thế chuyển đổi số trong nông nghiệp tại Việt Nam](#111-khái-niệm-vai-trò-và-xu-thế-chuyển-đổi-số-trong-nông-nghiệp-tại-việt-nam)
    - [1.1.2. Đặc thù của chuỗi cung ứng nông sản sạch và các tiêu chuẩn chất lượng](#112-đặc-thù-của-chuỗi-cung-ứng-nông-sản-sạch-và-các-tiêu-chuẩn-chất-lượng)
    - [1.1.3. Nhu cầu minh bạch hóa thông tin và tâm lý hành vi người tiêu dùng nông sản hiện đại](#113-nhu-cầu-minh-bạch-hóa-thông-tin-và-tâm-lý-hành-vi-người-tiêu-dùng-nông-sản-hiện-đại)
  - [1.2. Khảo sát các công trình liên quan và những vấn đề còn tồn tại](#12-khảo-sát-các-công-trình-liên-quan-và-những-vấn-đề-còn-tồn-tại)
    - [1.2.1. Khảo sát các mô hình thương mại điện tử nông sản trong và ngoài nước](#121-khảo-sát-các-mô-hình-thương-mại-điện-tử-nông-sản-trong-và-ngoài-nước)
    - [1.2.2. Phân tích so sánh ưu điểm, nhược điểm và khoảng trống công nghệ](#122-phân-tích-so-sánh-ưu-điểm-nhược-điểm-và-khoảng-trống-công-nghệ)
    - [1.2.3. Định vị giải pháp của nền tảng AgriSense Platform](#123-định-vị-giải-pháp-của-nền-tảng-agrisense-platform)
  - [1.3. Tổng quan nền tảng công nghệ phát triển hệ thống](#13-tổng-quan-nền-tảng-công-nghệ-phát-triển-hệ-thống)
    - [1.3.1. Ngôn ngữ lập trình Python 3.14 và hệ sinh thái xử lý dữ liệu](#131-ngôn-ngữ-lập-trình-python-314-và-hệ-sinh-thái-xử-lý-dữ-liệu)
    - [1.3.2. Web Framework Django 6.1.2 và mô hình kiến trúc MVT](#132-web-framework-django-612-và-mô-hình-kiến-trúc-mvt)
    - [1.3.3. Hệ quản trị cơ sở dữ liệu quan hệ MySQL Server 26.7.0 và PyMySQL Driver](#133-hệ-quản-trị-cơ-sở-dữ-liệu-quan-hệ-mysql-server-2670-và-pymysql-driver)
    - [1.3.4. Công nghệ Frontend giao diện và trực quan hóa dữ liệu (Bootstrap 5.3.3, Chart.js 4.4)](#134-công-nghệ-frontend-giao-diện-và-trực-quan-hóa-dữ-liệu-bootstrap-533-chartjs-44)
  - [1.4. Cơ sở lý thuyết về Trí tuệ nhân tạo (AI/LLM, Phân nhóm RFM, Gợi ý Content-based)](#14-cơ-sở-lý-thuyết-về-trí-tuệ-nhân-tạo-aillm-phân-nhóm-rfm-gợi-ý-content-based)
    - [1.4.1. Tổng quan về Mô hình ngôn ngữ lớn (Large Language Models - LLMs) và Generative AI](#141-tổng-quan-về-mô-hình-ngôn-ngữ-lớn-large-language-models---llms-và-generative-ai)
    - [1.4.2. Kiến trúc dịch vụ Chatbot AI đa tầng (Multi-tier) và cơ chế Fallback Regex](#142-kiến-trúc-dịch-vụ-chatbot-ai-đa-tầng-multi-tier-và-cơ-chế-fallback-regex)
    - [1.4.3. Cơ sở lý thuyết và mô hình phân khúc khách hàng RFM](#143-cơ-sở-lý-thuyết-và-mô-hình-phân-khúc-khách-hàng-rfm)
    - [1.4.4. Động cơ gợi ý sản phẩm cá nhân hóa (Content-based Filtering Recommendation Engine)](#144-động-cơ-gợi-ý-sản-phẩm-cá-nhân-hóa-content-based-filtering-recommendation-engine)
  - [1.5. Công nghệ mã QR truy xuất nguồn gốc và cổng thanh toán tự động VietQR Napas 247](#15-công-nghệ-mã-qr-truy-xuất-nguồn-gốc-và-cổng-thanh-toán-tự-động-vietqr-napas-247)
    - [1.5.1. Tiêu chuẩn mã ma trận hai chiều Quick Response (QR Code) và ứng dụng truy xuất nguồn gốc](#151-tiêu-chuẩn-mã-ma-trận-hai-chiều-quick-response-qr-code-và-ứng-dụng-truy-xuất-nguồn-gốc)
    - [1.5.2. Tiêu chuẩn mã thanh toán số VietQR Napas 247 và quy chuẩn EMVCo](#152-tiêu-chuẩn-mã-thanh-toán-số-vietqr-napas-247-và-quy-chuẩn-emvco)
  - [Kết luận Chương 1](#kết-luận-chương-1)
- [CHƯƠNG 2. PHÂN TÍCH YÊU CẦU VÀ THIẾT KẾ HỆ THỐNG AGRISENSE PLATFORM](#chương-2-phân-tích-yêu-cầu-và-thiết-kế-hệ-thống-agrisense-platform)
  - [2.1. Phân tích hiện trạng và khảo sát thực tế quy trình mua bán nông sản](#21-phân-tích-hiện-trạng-và-khảo-sát-thực-tế-quy-trình-mua-bán-nông-sản)
  - [2.2. Đặc tả yêu cầu bài toán (Yêu cầu chức năng và Yêu cầu phi chức năng)](#22-đặc-tả-yêu-cầu-bài-toán-yêu-cầu-chức-năng-và-yêu-cầu-phi-chức-năng)
  - [2.3. Thiết kế kiến trúc tổng thể hệ thống (Django MVT & Service Layer)](#23-thiết-kế-kiến-trúc-tổng-thể-hệ-thống-django-mvt--service-layer)
  - [2.4. Thiết kế các sơ đồ UML (Use Case, Activity, Class, Sequence Diagram)](#24-thiết-kế-các-sơ-đồ-uml-use-case-activity-class-sequence-diagram)
  - [2.5. Thiết kế cơ sở dữ liệu quan hệ (12 Model, 26 bảng MySQL, ERD)](#25-thiết-kế-cơ-sở-dữ-liệu-quan-hệ-12-model-26-bảng-mysql-erd)
  - [Kết luận Chương 2](#kết-luận-chương-2)
- [CHƯƠNG 3. HIỆN THỰC HÓA HỆ THỐNG, KẾT QUẢ THỰC NGHIỆM VÀ KIỂM THỬ](#chương-3-hiện-thực-hóa-hệ-thống-kết-quả-thực-nghiệm-và-kiểm-thử)
  - [3.1. Hiện thực hóa các phân hệ chức năng cốt lõi (Tài khoản, Sản phẩm, Đơn hàng)](#31-hiện-thực-hóa-các-phân-hệ-chức-năng-cốt-lõi-tài-khoản-sản-phẩm-đơn-hàng)
  - [3.2. Hiện thực hóa phân hệ AI (Chatbot đàm thoại lên đơn, RFM và Gợi ý cá nhân hóa)](#32-hiện-thực-hóa-phân-hệ-ai-chatbot-đàm-thoại-lên-đơn-rfm-và-gợi-ý-cá-nhân-hóa)
  - [3.3. Hiện thực hóa phân hệ Truy xuất nguồn gốc QR và Cổng thanh toán VietQR Napas 247](#33-hiện-thực-hóa-phân-hệ-truy-xuất-nguồn-gốc-qr-và-cổng-thanh-toán-vietqr-napas-247)
  - [3.4. Hiện thực hóa Dashboard Quản trị kinh doanh Chart.js và trích xuất Excel (.xlsx)](#34-hiện-thực-hóa-dashboard-quản-trị-kinh-doanh-chartjs-và-trích-xuất-excel-xlsx)
  - [3.5. Kết quả thực nghiệm dữ liệu mẫu (Seed Data) và Kiểm thử tự động (43 Tests PASS)](#35-kết-quả-thực-nghiệm-dữ-liệu-mẫu-seed-data-và-kiểm-thử-tự-động-43-tests-pass)
  - [Kết luận Chương 3](#kết-luận-chương-3)
- [KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN](#kết-luận-và-hướng-phát-triển)
  - [1. Những kết quả và đóng góp chính đã đạt được](#1-những-kết-quả-và-đóng-góp-chính-đã-đạt-được)
  - [2. Hạn chế còn tồn tại](#2-hạn-chế-còn-tồn-tại)
  - [3. Hướng nghiên cứu và phát triển tiếp theo](#3-hướng-nghiên-cứu-và-phát-triển-tiếp-theo)
- [TÀI LIỆU THAM KHẢO](#tài-liệu-tham-khảo)
- [PHỤ LỤC](#phụ-lục)
- [TIẾN ĐỘ THỰC HIỆN ĐỒ ÁN](#tiến-độ-thực-hiện-đồ-án)

---

# DANH MỤC CÁC TỪ VIẾT TẮT

| Từ viết tắt | Thuật ngữ tiếng Anh | Ý nghĩa / Diễn giải tiếng Việt |
| :---: | :--- | :--- |
| **AI** | Artificial Intelligence | Trí tuệ nhân tạo |
| **API** | Application Programming Interface | Giao diện lập trình ứng dụng |
| **CLO** | Course Learning Outcome | Chuẩn đầu ra của học phần |
| **COD** | Cash On Delivery | Thanh toán bằng tiền mặt khi nhận hàng |
| **CSRF** | Cross-Site Request Forgery | Tấn công giả mạo yêu cầu từ phía người dùng |
| **ERD** | Entity Relationship Diagram | Sơ đồ thực thể liên kết cơ sở dữ liệu |
| **LLM** | Large Language Model | Mô hình ngôn ngữ lớn |
| **MVT** | Model - View - Template | Mô hình kiến trúc phần mềm chuẩn của Django |
| **ORM** | Object-Relational Mapping | Ánh xạ cơ sở dữ liệu quan hệ sang đối tượng |
| **QR** | Quick Response | Mã phản hồi nhanh (mã vạch ma trận hai chiều) |
| **RFM** | Recency - Frequency - Monetary | Mô hình phân loại khách hàng theo hành vi |
| **UML** | Unified Modeling Language | Ngôn ngữ mô hình hóa thống nhất |
| **VietGAP** | Vietnamese Good Agricultural Practices | Thực hành sản xuất nông nghiệp tốt tại Việt Nam |
| **WBS** | Work Breakdown Structure | Cấu trúc phân rã công việc dự án |

---

# DANH MỤC CÁC BẢNG

- **Bảng 1.1**: So sánh đối chiếu tính năng giữa các nền tảng thương mại điện tử hiện hành và AgriSense Platform
- **Bảng 1.2**: Thông số môi trường công nghệ và công cụ phát triển hệ thống AgriSense
- **Bảng 1.3**: Đặc tả quy tắc phân nhóm khách hàng theo mô hình RFM trong hệ thống AgriSense
- **Bảng 2.1**: Đặc tả 12 Model cơ sở dữ liệu cốt lõi phân theo nhóm nghiệp vụ
- **Bảng 2.2**: Đặc tả các quy tắc phân nhóm khách hàng theo mô hình RFM
- **Bảng 3.1**: Kết quả thống kê khởi tạo dữ liệu mẫu (Seed Data)
- **Bảng 3.2**: Tổng hợp kết quả kiểm thử tự động 43 Unit Tests theo phân hệ
- **Bảng 4.1**: Kế hoạch tiến độ thực hiện đề tài Đồ án chuyên ngành

---

# DANH MỤC CÁC HÌNH VẼ

- **Hình 1.1**: Mô hình chuỗi phân phối nông sản truyền thống và mô hình chuỗi cung ứng số Farm-to-Fork AgriSense
- **Hình 1.2**: Sơ đồ kiến trúc ngăn xếp công nghệ hệ thống AgriSense Platform (MVT & Services)
- **Hình 1.3**: Chu trình xử lý yêu cầu HTTP trong kiến trúc Django MVT
- **Hình 1.4**: Mô hình xử lý nghiệp vụ thương mại đàm thoại (Conversational Commerce)
- **Hình 1.5**: Sơ đồ luồng điều phối tin nhắn Chatbot AI đa tầng (Multi-tier) và Fallback Regex
- **Hình 1.6**: Quy trình tính điểm sở thích và đề xuất nông sản thông minh
- **Hình 1.7**: Cấu trúc hình học cơ bản của mã QR theo chuẩn quốc tế ISO/IEC 18004
- **Hình 1.8**: So sánh quy trình thanh toán chuyển khoản truyền thống và thanh toán tự động VietQR Napas 247
- **Hình 2.1**: Sơ đồ Use Case tổng quát toàn hệ thống AgriSense
- **Hình 2.2**: Sơ đồ Activity luồng đặt hàng và thanh toán VietQR Napas 247
- **Hình 2.3**: Sơ đồ Sequence luồng xử lý Chatbot AI đàm thoại và Fallback Regex
- **Hình 2.4**: Sơ đồ thực thể liên kết CSDL quan hệ (ERD 12 Model)
- **Hình 3.1**: Giao diện trang chủ và khối gợi ý nông sản cá nhân hóa
- **Hình 3.2**: Giao diện giỏ hàng và thanh toán tự động VietQR Napas 247
- **Hình 3.3**: Widget Chatbot AI hỗ trợ tư vấn và chốt đơn trực tiếp trong khung chat
- **Hình 3.4**: Trang thông tin tra cứu truy xuất nguồn gốc lô hàng qua mã QR
- **Hình 3.5**: Giao diện Dashboard Admin với 3 biểu đồ tương tác Chart.js và nút xuất Excel

---

# MỞ ĐẦU

## 1.1. Lý do chọn đề tài
Nông nghiệp là trụ cột kinh tế trọng yếu của Việt Nam, trong đó phong trào sản xuất và tiêu dùng nông sản sạch, nông sản hữu cơ đạt chuẩn (VietGAP, GlobalGAP, Organic) đang phát triển vô cùng mạnh mẽ. Tuy nhiên, chuỗi phân phối từ người nông dân đến tay người tiêu dùng cuối cùng hiện vẫn gặp nhiều nút thắt nan giải:
- **Thiếu minh bạch về nguồn gốc xuất xứ**: Người tiêu dùng luôn lo ngại về độ an toàn của thực phẩm nhưng các sàn thương mại điện tử tổng hợp chỉ cung cấp mô tả văn bản chung chung, thiếu công cụ xác thực nhật ký canh tác và chứng nhận theo từng lô hàng thu hoạch cụ thể.
- **Thiếu giải pháp tư vấn cá nhân hóa tức thời**: Nông sản là mặt hàng tươi sống có tính chất mùa vụ và đặc thù bảo quản cao. Người mua luôn cần được tư vấn chi tiết 24/7 về giá cả, hạn dùng, cách chế biến nhưng đội ngũ bán hàng truyền thống không thể phản hồi tức thì.
- **Thách thức trong chuyển đổi số của nhà vườn**: Các hợp tác xã và hộ nông dân nhỏ lẻ thiếu công cụ kỹ thuật số bài bản để quảng bá sản phẩm, quản lý kho hàng và ứng dụng dữ liệu thông minh trong việc chăm sóc khách hàng.

Xuất phát từ thực tiễn trên, việc nghiên cứu và xây dựng đề tài **"Website Bán Nông Sản Tích Hợp AI (AgriSense Platform)"** có ý nghĩa khoa học và thực tiễn sâu sắc. Dự án kết hợp công nghệ web hiện đại (Django, MySQL, Bootstrap 5) với Trí tuệ nhân tạo (Chatbot LLM, phân nhóm RFM, lọc nội dung Content-based) cùng mã QR truy xuất và cổng VietQR Napas 247 nhằm giải quyết trọn vẹn bài toán thương mại điện tử nông sản bền vững.

## 1.2. Mục tiêu của đề tài
- **Mục tiêu khoa học**: Nghiên cứu phương pháp tích hợp mô hình ngôn ngữ lớn (LLM) vào bài toán thương mại đàm thoại (Conversational Commerce); áp dụng mô hình phân nhóm hành vi RFM và thuật toán gợi ý Content-based Filtering trong thương mại điện tử nông sản.
- **Mục tiêu ứng dụng**: Xây dựng hoàn chỉnh một nền tảng web thương mại điện tử chuyên biệt cho nông sản (AgriSense Platform) vận hành ổn định trên máy chủ cục bộ, đáp ứng đầy đủ quy trình bán hàng, truy xuất nguồn gốc bằng mã QR chuẩn ISO, thanh toán tự động VietQR Napas 247 và quản trị kinh doanh trực quan.
- **Mục tiêu đào tạo**: Vận dụng toàn diện kiến thức học phần Đồ án chuyên ngành Công nghệ phần mềm: phân tích thiết kế hướng đối tượng UML, thiết kế CSDL quan hệ chuẩn hóa, xây dựng ứng dụng MVT, kiểm thử tự động và hoàn thiện tài liệu chuyên nghiệp.

## 1.3. Nội dung và phạm vi nghiên cứu
- **Nội dung nghiên cứu**: Tập trung vào 4 trọng tâm chính:
  1. Nghiên cứu và thiết kế kiến trúc MVT hướng dịch vụ trên nền tảng Django Framework kết nối MySQL Server 26.7.0 thông qua PyMySQL driver.
  2. Xây dựng thuật toán theo dõi hành vi, phân nhóm khách hàng RFM và gợi ý nông sản thông minh.
  3. Tích hợp Chatbot AI đa nền tảng (Gemini 1.5 Flash / Groq LLM) kết hợp bộ luật Fallback Regex tiếng Việt và tính năng chốt đơn hàng tự động.
  4. Hiện thực hóa quy trình sinh mã QR truy xuất nguồn gốc lô hàng và cổng thanh toán nhanh VietQR.
- **Phạm vi nghiên cứu**:
  - *Trong phạm vi*: Phát triển ứng dụng Web Responsive chạy trên máy chủ phát triển Django Development Server kết nối MySQL Server; 8 phân hệ nghiệp vụ cốt lõi; hệ thống kiểm thử tự động Unit Tests; khởi tạo dữ liệu mẫu thực nghiệm phong phú.
  - *Ngoài phạm vi*: Chưa triển khai hạ tầng máy chủ Cloud phân tán quy mô lớn; chưa phát triển ứng dụng di động Native (tập trung giao diện Web Responsive tương thích di động); không tích hợp cổng thẻ quốc tế trả phí phức tạp.

## 1.4. Đóng góp của đề tài
1. **Về mặt thực tiễn**: Cung cấp nền tảng số khép kín, minh bạch cho nông sản sạch, giúp người tiêu dùng an tâm tra cứu nguồn gốc bằng mã QR và mua sắm tiện lợi với mã VietQR tự động.
2. **Về mặt công nghệ**: Hiện thực hóa thành công mô hình "Conversational Commerce" - cho phép khách hàng ra lệnh bằng văn bản tự nhiên để hệ thống tự động nhận diện sản phẩm, trừ tồn kho an toàn và sinh mã thanh toán tức thì ngay trong khung chat.
3. **Về mặt học thuật và kỹ năng kỹ thuật**: Đóng góp một bộ mã nguồn hoàn chỉnh, kiến trúc chuẩn hóa MVT, 12 Model nghiệp vụ rõ ràng và hệ thống 43 Unit Tests đạt tỷ lệ thành công 100%, phục vụ làm tài liệu tham khảo cho sinh viên ngành Công nghệ phần mềm.

## 1.5. Cấu trúc của Đề cương Bài tập lớn
Đề cương Bài tập lớn được kết cấu thành 3 chương chính và các phần phụ trợ theo đúng quy chuẩn:
- **Mở đầu**: Trình bày lý do chọn đề tài, mục tiêu, đối tượng, phạm vi nghiên cứu và những đóng góp chính của đề tài.
- **Chương 1**: Cơ sở lý thuyết và tổng quan hệ thống thương mại điện tử nông sản tích hợp Trí tuệ nhân tạo.
- **Chương 2**: Phân tích yêu cầu và thiết kế hệ thống AgriSense Platform (kiến trúc, sơ đồ UML và CSDL).
- **Chương 3**: Hiện thực hóa hệ thống, kết quả thực nghiệm và kiểm thử.
- **Kết luận và hướng phát triển**: Tổng kết kết quả đạt được, chỉ ra hạn chế và định hướng phát triển tiếp theo.
- **Tài liệu tham khảo, Phụ lục và Tiến độ thực hiện đồ án**.

---

# CHƯƠNG 1. CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ NÔNG SẢN TÍCH HỢP AI

## 1.1. Cơ sở lý luận về thương mại điện tử trong chuỗi cung ứng nông sản sạch

### 1.1.1. Khái niệm, vai trò và xu thế chuyển đổi số trong nông nghiệp tại Việt Nam
Thương mại điện tử nông nghiệp (*Agricultural E-Commerce* hay *Agri-eCommerce*) là quá trình ứng dụng toàn diện công nghệ thông tin, mạng viễn thông kỹ thuật số và các nền tảng trực tuyến vào toàn bộ chuỗi giá trị nông nghiệp: từ quảng bá, tiếp thị, kết nối cung cầu, xúc tiến thương mại, đặt hàng, xử lý giao dịch tài chính đến khâu giao nhận và truy xuất nguồn gốc thực phẩm.

Việt Nam sở hữu lợi thế tự nhiên đặc thù của một quốc gia nhiệt đới gió mùa với bề dày truyền thống sản xuất nông nghiệp. Nông nghiệp không chỉ là bệ đỡ kinh tế vĩ mô mà còn là nguồn sinh kế cốt lõi của hơn 60% dân số. Tuy nhiên, mô hình phân phối nông sản truyền thống tại nước ta từ lâu đã bộc lộ những mắt xích yếu kém mang tính cố hữu:
1. **Chuỗi cung ứng đa tầng nấc và phân tán**: Nông sản sau khi thu hoạch tại vườn thường phải trải qua từ 3 đến 5 khâu trung gian (thương lái thu mua tại ruộng $\\rightarrow$ chủ vựa đầu mối địa phương $\\rightarrow$ thương lái vận chuyển đường dài $\\rightarrow$ tiểu thương chợ đầu mối bán buôn $\\rightarrow$ người bán lẻ tại chợ dân sinh $\\rightarrow$ người tiêu dùng cuối). Mỗi tầng trung gian đều làm tăng chi phí lưu kho bãi, hao hụt vận chuyển và biên lợi nhuận bị phân mảnh, khiến người nông dân trực tiếp sản xuất chịu mức giá rẻ mạt trong khi người tiêu dùng thành thị phải chi trả mức giá đắt đỏ.
2. **Hiện tượng bất đối xứng thông tin (*Information Asymmetry*)**: Người nông dân thường xuyên chịu cảnh "được mùa mất giá, được giá mất mùa" do thiếu thông tin dự báo nhu cầu thị trường thời gian thực; ngược lại, người tiêu dùng hoàn toàn thụ động, không có công cụ xác minh chất lượng và quy trình canh tác thực tế của sản phẩm.

```
MÔ HÌNH PHÂN PHỐI NÔNG SẢN TRUYỀN THỐNG (ĐA TẦNG NẤC):
[Hộ Nông Dân] ──> [Thương Lái Vườn] ──> [Vựa Thu Mua] ──> [Chợ Đầu Mối] ──> [Tiểu Thương Chợ Dân Sinh] ──> [Người Tiêu Dùng]
(Rủi ro: Hao hụt cao, đội giá 200-300%, đứt gãy thông tin, không thể truy xuất nguồn gốc)

MÔ HÌNH THƯƠNG MẠI ĐIỆN TỬ AGRISENSE ("FARM-TO-FORK"):
[Nhà Vườn / Hợp Tác Xã VietGAP] <═══════════════[ NỀN TẢNG AGRISENSE PLATFORM ]═══════════════> [Người Tiêu Dùng Cuối]
  ├── Nhật ký canh tác / Lô hàng                 ├── Tra cứu nguồn gốc mã QR công khai              ├── Đặt hàng trực tiếp & COD
  └── Cập nhật tồn kho tự động                   ├── Trợ lý Chatbot AI tư vấn & chốt đơn 24/7        └── Quét VietQR Napas thanh toán tức thì
```
*Hình 1.1: Mô hình chuỗi phân phối nông sản truyền thống và mô hình chuỗi cung ứng số Farm-to-Fork AgriSense*

Thực hiện Nghị quyết số 52-NQ/TW của Bộ Chính trị về một số chủ trương, chính sách chủ động tham gia cuộc Cách mạng công nghiệp lần thứ tư và Quyết định số 749/QĐ-TTg của Thủ tướng Chính phủ phê duyệt "Chương trình Chuyển đổi số quốc gia đến năm 2025, định hướng đến năm 2030", nông nghiệp được xác định là một trong 8 lĩnh vực ưu tiên hàng đầu trong chuyển đổi số. Việc ứng dụng công nghệ web hiện đại kết hợp Trí tuệ nhân tạo (AI) để xây dựng chuỗi cung ứng ngắn (*Short Food Supply Chain - SFSC*) theo mô hình "Từ nông trại đến bàn ăn" (*Farm-to-Fork* / *Farm-to-Table*) là lời giải căn cơ nhằm rút ngắn khoảng cách địa lý, giảm thiểu lãng phí thực phẩm và gia tăng giá trị kinh tế bền vững.

---

### 1.1.2. Đặc thù của chuỗi cung ứng nông sản sạch và các tiêu chuẩn chất lượng
Khác biệt hoàn toàn với các mặt hàng công nghiệp tiêu chuẩn (điện tử, may mặc, gia dụng) có vòng đời dài và điều kiện bảo quản ổn định, nông sản tươi sống sở hữu những đặc tính sinh hóa và vận hành vô cùng khắt khe:
- **Tính dễ suy giảm chất lượng và vòng đời ngắn (*High Perishability*)**: Rau ăn lá, củ quả và trái cây tươi liên tục diễn ra quá trình hô hấp tế bào, thoát hơi nước và biến đổi sinh hóa sau thu hoạch. Nếu không có quy trình bảo quản tối ưu và luồng tiêu thụ tức thời, tỷ lệ hao hụt cơ học và suy thoái phẩm cấp có thể lên tới 25% – 35% tổng sản lượng chỉ sau 48 đến 72 giờ.
- **Tính thời vụ và phụ thuộc điều kiện thổ nhưỡng, vi khí hậu (*Seasonality*)**: Mỗi loại đặc sản nông nghiệp gắn liền với chu kỳ mùa vụ sinh trưởng và địa bàn canh tác đặc thù (ví dụ: Xoài cát Hòa Lộc Tiền Giang, Cà chua bi Đà Lạt, Nhãn lồng Hưng Yên, Cam sành Hàm Yên). Nhu cầu quản lý lô hàng (*Product Batch*) theo từng đợt thu hoạch là yêu cầu bắt buộc để quản lý hạn sử dụng và cam kết độ tươi ngon với người mua.
- **Tính biến động giá cả theo thời gian thực (*Price Volatility*)**: Giá bán nông sản biến động liên tục theo ngày dựa trên sản lượng cung ứng thực tế tại ruộng và thời tiết. Hệ thống thương mại điện tử cần hỗ trợ quản trị viên linh hoạt cập nhật biểu giá, số lượng tồn kho khả dụng và chính sách khuyến mãi.

```
+---------------------------------------------------------------------------------------------------+
|                         CÁC TIÊU CHUẨN CHẤT LƯỢNG NÔNG SẢN NỔI BẬT HIỆN NAY                       |
+--------------------+------------------------------------------------------------------------------+
| VietGAP            | Tiêu chuẩn Thực hành sản xuất nông nghiệp tốt tại Việt Nam theo TCVN         |
| (TCVN 11892-1:2017)| 11892-1:2017: Kiểm soát 4 mối nguy (an toàn thực phẩm, môi trường, sức khỏe  |
|                    | người lao động và truy nguyên nguồn gốc sản phẩm).                          |
+--------------------+------------------------------------------------------------------------------+
| GlobalG.A.P.       | Tiêu chuẩn thực hành nông nghiệp tốt toàn cầu: Yêu cầu khắt khe về nhật ký   |
|                    | sử dụng phân bón, thuốc bảo vệ thực vật, nguồn nước tưới và chứng nhận quốc tế|
+--------------------+------------------------------------------------------------------------------+
| Nông nghiệp hữu cơ | Tiêu chuẩn quốc gia TCVN 11041 / Tiêu chuẩn USDA Organic: Tuyệt đối không sử |
| (Organic Standards)| dụng thuốc trừ sâu hóa học, phân bón vô cơ tổng hợp, chất kích thích sinh    |
|                    | trưởng và giống cây trồng biến đổi gen (Non-GMO).                            |
+--------------------+------------------------------------------------------------------------------+
```

Việc tích hợp quản lý thông tin các tiêu chuẩn trên vào hệ thống thương mại điện tử giúp nâng tầm giá trị nông sản Việt, đồng thời bảo vệ quyền lợi chính đáng của những đơn vị sản xuất uy tín.

---

### 1.1.3. Nhu cầu minh bạch hóa thông tin và tâm lý hành vi người tiêu dùng nông sản hiện đại
Trong bối cảnh thu nhập bình quân đầu người tại các đô thị tăng trưởng nhanh chóng, nhận thức của người tiêu dùng về sức khỏe, dinh dưỡng và lối sống xanh đã có bước chuyển biến sâu sắc. Tuy nhiên, thị trường thực phẩm Việt Nam trong nhiều năm qua liên tục đối mặt với vấn nạn thực phẩm bẩn, dư lượng thuốc bảo vệ thực vật vượt ngưỡng cho phép, chất bảo quản độc hại và tình trạng "gian lận nhãn mác" (nông sản trôi nổi tại chợ đầu mối được gắn mác VietGAP/Đà Lạt nhằm trục lợi). 

Thực trạng này đã tạo ra một rào cản tâm lý lớn: **"Khủng hoảng niềm tin" (*Trust Deficit*)**. Người tiêu dùng sẵn sàng chi trả mức giá cao hơn từ 30% đến 100% cho nông sản sạch, nhưng họ đặt ra những yêu cầu khắt khe về tính minh chứng:
- Sản phẩm được trồng tại nông trại nào, hợp tác xã nào phụ trách?
- Ngày gieo hạt, ngày bón phân đợt cuối và ngày thu hoạch chính xác là khi nào?
- Lô hàng có giấy kiểm nghiệm an toàn thực phẩm hay chứng chỉ hợp chuẩn hợp quy còn hiệu lực hay không?
- Khi hàng giao đến nơi, có cơ chế nào để đối chiếu tức thì bao bì với hồ sơ kỹ thuật số của lô hàng?

Ngoài ra, người tiêu dùng bận rộn tại các đô thị hiện đại ngày nay có xu hướng chuộng sự tiện dụng tối đa: họ mong muốn được tư vấn chế biến, bảo quản ngay khi đang xem sản phẩm, và kỳ vọng phương thức thanh toán phải diễn ra tức thì trong vài giây trên thiết bị di động mà không cần thao tác gõ số tài khoản thủ công dễ nhầm lẫn.

---

## 1.2. Khảo sát các công trình liên quan và những vấn đề còn tồn tại

### 1.2.1. Khảo sát các mô hình thương mại điện tử nông sản trong và ngoài nước

#### A. Các mô hình tiêu biểu trên thế giới
1. **Pinduoduo (Trung Quốc)**: Nền tảng khởi nghiệp đột phá bằng mô hình "C2M" (*Consumer-to-Manufacturer*) và mua chung (*Team Purchase*) cho nông sản. Bằng cách tập hợp nhu cầu của hàng triệu người tiêu dùng qua mạng xã hội, Pinduoduo chuyển tiếp đơn hàng trực tiếp tới các vùng chuyên canh nông nghiệp, cắt bỏ toàn bộ khâu trung gian, vận chuyển nông sản tươi đến tay người mua chỉ trong vòng 24 - 48 giờ. Tuy nhiên, mô hình này đòi hỏi quy mô vốn khổng lồ và tập trung chính vào hạ tầng vận chuyển liên tỉnh siêu tốc, chưa chú trọng sâu đến việc cá nhân hóa thông qua đàm thoại AI chuyên sâu ở mức bán lẻ vi mô.
2. **Farmdrop (Vương quốc Anh)**: Mô hình trực tuyến kết nối các trang trại hữu cơ địa phương với người tiêu dùng thành thị. Điểm nổi bật là cung cấp hồ sơ trang trại minh bạch, thông tin về phúc lợi động vật và quy trình canh tác sinh thái. Mặc dù tạo dựng được niềm tin thương hiệu rất tốt, Farmdrop từng gặp khó khăn nghiêm trọng về chi phí hoàn tất đơn hàng (*fulfillment cost*) và chi phí duy trì đội ngũ chăm sóc khách hàng thủ công.
3. **Cropwise & Indigo Ag (Hoa Kỳ)**: Các nền tảng số hóa nông nghiệp định hướng dữ liệu B2B, cung cấp công cụ giám sát mùa màng vệ tinh và kết nối các nhà sản xuất ngũ cốc quy mô lớn với các tập đoàn chế biến. Các nền tảng này tập trung vào thị trường nguyên liệu thô công nghiệp, không phục vụ đối tượng người tiêu dùng cá nhân B2C.

#### B. Khảo sát hiện trạng thị trường tại Việt Nam
1. **Các sàn thương mại điện tử tổng hợp (Shopee, Tiki Farm, Lazada)**:
   - *Ưu điểm*: Lưu lượng người dùng khổng lồ, hạ tầng thanh toán và đối tác vận chuyển nội thành phủ rộng.
   - *Hạn chế*: Nông sản tươi sống chỉ chiếm tỷ trọng nhỏ; hệ thống không được thiết kế chuyên biệt để quản lý lô hàng (*Batch*), không có cơ chế liên kết động giữa mã QR lô hàng thu hoạch và nhật ký kiểm định; mô hình duyệt sản phẩm chung chung, không hỗ trợ tư vấn chuyên sâu về điều kiện bảo quản nông sản theo mùa.
2. **Các chuỗi bán lẻ thực phẩm sạch (Bách Hóa Xanh Online, WinMart, Sói Biển, Bác Tôm)**:
   - *Ưu điểm*: Có chuỗi cửa hàng vật lý bổ trợ, nguồn hàng kiểm soát tương đối tốt.
   - *Hạn chế*: Ứng dụng web/app đa phần đóng vai trò như một catalogue điện tử tĩnh; thiếu cơ chế khuyến nghị cá nhân hóa dựa trên học máy; việc hỗ trợ khách hàng phụ thuộc vào tổng đài viên trong giờ hành chính; khâu thanh toán chuyển khoản thường yêu cầu người mua tự sao chép số tài khoản và gõ nội dung chuyển khoản, phát sinh nhiều sai sót cần đối soát thủ công.
3. **Các sàn nông sản bưu chính (Voso.vn, Postmart.vn)**:
   - *Ưu điểm*: Hỗ trợ tiêu thụ đặc sản OCOP các tỉnh thành dựa trên mạng lưới bưu chính rộng khắp.
   - *Hạn chế*: Giao diện người dùng (*UI/UX*) chưa tối ưu, trải nghiệm tìm kiếm nông sản khó khăn, thiếu công nghệ tương tác thông minh như Chatbot AI đàm thoại và tỷ lệ giữ chân khách hàng chưa cao.

---

### 1.2.2. Phân tích so sánh ưu điểm, nhược điểm và khoảng trống công nghệ

Nhằm làm rõ khoảng trống kỹ thuật giữa các giải pháp hiện hành và định vị mục tiêu xây dựng nền tảng AgriSense, bảng so sánh đa tiêu chí dưới đây tổng hợp các khía cạnh cốt lõi của một hệ thống thương mại điện tử nông sản hiện đại:

*Bảng 1.1: So sánh đối chiếu tính năng giữa các nền tảng thương mại điện tử hiện hành và AgriSense Platform*

| Tiêu chí so sánh | Sàn TMĐT tổng hợp (Shopee/Lazada) | Web chuỗi thực phẩm (Sói Biển/Bách Hóa Xanh) | Sàn nông sản OCOP (Voso/Postmart) | **Hệ thống đề xuất: AgriSense Platform** |
| :--- | :--- | :--- | :--- | :--- |
| **Đối tượng sản phẩm** | Hàng tiêu dùng tổng hợp | Thực phẩm sạch, rau thịt cá | Đặc sản vùng miền OCOP | **Nông sản sạch, hữu cơ, đặc sản VietGAP** |
| **Quản lý theo lô hàng (Product Batch)** | Không có (chỉ quản lý SKU) | Rất hạn chế (nội bộ ERP) | Không có | **Có chuyên biệt (Lô, ngày hái, chứng chỉ)** |
| **Truy xuất nguồn gốc QR động** | Không có | QR tĩnh in sẵn bao bì | QR tĩnh dẫn về link tổng | **QR động chuẩn ISO dẫn thẳng hồ sơ lô hàng** |
| **Tư vấn đàm thoại AI (LLM)** | Chatbot kịch bản tĩnh (Rule/FAQ đơn giản) | Không có (chat nhân viên trực tiếp) | Không có | **AI LLM (Gemini/Groq) + Fallback Regex tiếng Việt** |
| **Đặt hàng qua hội thoại (Conversational Commerce)** | Không hỗ trợ | Không hỗ trợ | Không hỗ trợ | **Hỗ trợ đặt hàng trực tiếp bằng ngôn ngữ tự nhiên** |
| **Phân khúc khách hàng** | Phức tạp, ẩn trong hệ thống lõi | Phân hạng tích điểm thủ công | Không phân khúc rõ ràng | **Mô hình RFM rules 5 mức cập nhật tự động** |
| **Gợi ý cá nhân hóa** | Ma trận đề xuất tổng hợp lớn | Không có / Gợi ý ngẫu nhiên | Đề xuất sản phẩm mới nhất | **Content-based Filtering theo trọng số hành vi** |
| **Thanh toán chuyển khoản** | Cổng thanh toán trung gian, ví điện tử | Chuyển khoản thủ công / COD | Chuyển khoản thủ công / COD | **Cổng tự động VietQR Napas 247 nhúng sẵn mã đơn** |
| **Báo cáo phân tích quản trị** | Dashboard sàn phức tạp | Báo cáo ERP nội bộ đóng kín | Thống kê cơ bản | **Dashboard Chart.js trực quan + Xuất Excel (.xlsx)** |

---

### 1.2.3. Định vị giải pháp của nền tảng AgriSense Platform
Qua quá trình phân tích và khảo sát thực tiễn, đề tài xác định nền tảng **AgriSense Platform** được xây dựng nhằm giải quyết triệt để 4 mắt xích yếu nhất trong chuỗi phân phối số nông sản:
1. **Minh bạch hóa tuyệt đối chuỗi cung ứng**: Mỗi lô hàng nông sản đưa lên hệ thống bắt buộc gắn liền với thông tin vùng trồng, nông trại, ngày thu hoạch và chứng nhận hợp quy, được mã hóa dưới dạng mã QR động chuẩn ISO để người tiêu dùng quét tức thì mà không cần cài đặt ứng dụng phức tạp.
2. **Hiện thực hóa thương mại đàm thoại (*Conversational Commerce*)**: Thay vì bắt người dùng phải duyệt qua hàng chục trang danh mục, Chatbot AI đóng vai trò như một người bán hàng tận tâm tại quầy: vừa tư vấn đặc tính, xuất xứ, vừa hiểu được câu lệnh đặt hàng tự nhiên của khách (ví dụ: *"Tôi muốn mua 2kg cà chua bi giao về Cầu Giấy Hà Nội"*), tự động trừ kho an toàn và trả về mã VietQR thanh toán ngay trong khung chat.
3. **Cá nhân hóa trải nghiệm tiêu dùng**: Ứng dụng mô hình phân nhóm hành vi RFM kết hợp thuật toán lọc nội dung Content-based Filtering để thấu hiểu khẩu vị của từng khách hàng, từ đó đề xuất đúng loại nông sản tươi ngon theo thói quen mua sắm.
4. **Đơn giản hóa giao dịch tài chính**: Triệt tiêu hoàn toàn thao tác gõ số tài khoản và nội dung chuyển khoản rườm rà thông qua chuẩn quét mã VietQR Napas 247, giúp quy trình thanh toán diễn ra chính xác 100% trong vòng dưới 10 giây.

---

## 1.3. Tổng quan nền tảng công nghệ phát triển hệ thống

Để hiện thực hóa một hệ thống thương mại điện tử chuyên biệt đòi hỏi tính toàn vẹn dữ liệu cao, tốc độ xử lý nhanh và khả năng tích hợp linh hoạt các module Trí tuệ nhân tạo, đề tài lựa chọn ngăn xếp công nghệ (*Tech Stack*) vững chắc, hiện đại và chuẩn mực trong ngành kỹ thuật phần mềm.

```
+---------------------------------------------------------------------------------------------------+
|                        KIẾN TRÚC NGĂN XẾP CÔNG NGHỆ CỦA AGRISENSE PLATFORM                         |
+---------------------------------------------------------------------------------------------------+
| [PRESENTATION LAYER]  : HTML5, CSS3, Bootstrap 5.3.3, Bootstrap Icons, Chart.js 4.4, JavaScript   |
| [APPLICATION LAYER]   : Django 6.1.2 Framework (Architecture: Model - View - Template)            |
|   ├── Services Layer  : AI Service, Order Assistant, Recommendation Engine, VietQR, QR Generator  |
|   └── Middleware Layer: Authentication Middleware, CSRF Defense, Behavior Tracking Middleware     |
| [AI & DATA SCIENCE]   : Google Gemini 1.5 Flash API, Groq Cloud API, Pandas, Scikit-learn, openpyxl|
| [DATA ACCESS LAYER]   : Django ORM, PyMySQL 1.2.3 (Native Python Driver)                          |
| [PERSISTENCE LAYER]   : MySQL Server Community Edition 26.7.0 (Port 3306, utf8mb4_0900_ai_ci)      |
+---------------------------------------------------------------------------------------------------+
```
*Hình 1.2: Sơ đồ kiến trúc ngăn xếp công nghệ hệ thống AgriSense Platform (MVT & Services)*

*Bảng 1.2: Thông số môi trường công nghệ và công cụ phát triển hệ thống AgriSense*

| Thành phần kỹ thuật | Công nghệ / Phiên bản | Vai trò trong hệ thống |
| :--- | :--- | :--- |
| Hệ điều hành | Windows 11 Pro (64-bit) | Môi trường phát triển và kiểm thử chuẩn |
| Ngôn ngữ | Python 3.14.3 | Nền tảng Backend chính, xử lý logic và tính toán dữ liệu |
| Web Framework | Django 6.1.2 | Xử lý nghiệp vụ MVT, ORM, Auth, bảo vệ CSRF |
| CSDL Quan hệ | MySQL Community Server 26.7.0 | Lưu trữ 26 bảng dữ liệu hệ thống (utf8mb4_0900_ai_ci) |
| CSDL Driver | PyMySQL 1.2.3 | Trình điều khiển kết nối thuần Python tương thích 3.14 |
| UI Framework | Bootstrap 5.3.3, Bootstrap Icons | Giao diện Responsive Desktop/Mobile không dùng jQuery |
| Trực quan hóa | Chart.js 4.4 | 3 biểu đồ tương tác thời gian thực trên Dashboard |
| Xuất báo cáo | openpyxl 3.1.5 | Xuất file Excel (.xlsx) danh sách đơn hàng có định dạng |
| Mã QR | qrcode 7.4.2 & Pillow 11.0.0 | Tự động sinh ảnh mã QR PNG chuẩn ISO cho từng lô hàng |
| AI / LLM | Google Gemini 1.5 Flash / Groq | Chatbot đàm thoại, phân tích ngữ cảnh và chốt đơn tự động |

### 1.3.1. Ngôn ngữ lập trình Python 3.14 và hệ sinh thái xử lý dữ liệu
Python là ngôn ngữ lập trình bậc cao, thông dịch, hướng đối tượng mạnh mẽ được tạo ra bởi Guido van Rossum. Trong dự án AgriSense, phiên bản **Python 3.14.3** được lựa chọn làm ngôn ngữ cốt lõi ở tầng Backend nhờ những ưu điểm vượt trội:
- **Cú pháp trong sáng, năng suất phát triển cao**: Cấu trúc cú pháp rõ ràng, gần gũi với ngôn ngữ tự nhiên giúp lập trình viên tập trung tối đa vào việc giải quyết bài toán nghiệp vụ phức tạp thay vì phải quản lý các chi tiết cấp thấp như cấp phát bộ nhớ thủ công.
- **Hệ sinh thái thư viện khoa học dữ liệu và AI số một thế giới**: Python là ngôn ngữ tiêu chuẩn công nghiệp cho các bài toán Trí tuệ nhân tạo và Phân tích dữ liệu. Việc tích hợp các thư viện chuyên sâu như `requests` (giao tiếp HTTP RESTful với API LLM), `qrcode` và `Pillow` (xử lý đồ họa ma trận ảnh 2D), `pandas` và `scikit-learn` (tính toán ma trận sở thích, phân cụm khách hàng), `openpyxl` (đọc/ghi cấu trúc file bảng tính Excel `.xlsx`) được thực hiện một cách liền mạch, không gặp rào cản tương thích.
- **Hiệu năng được cải thiện rõ rệt**: Các phiên bản Python thế hệ mới tối ưu hóa trình thông dịch CPython, giảm độ trễ khi thực thi vòng lặp và tối ưu hóa bộ nhớ đệm giúp đáp ứng tốt khối lượng tải truy cập đồng thời của một website thương mại điện tử.

---

### 1.3.2. Web Framework Django 6.1.2 và mô hình kiến trúc MVT

Django là một web framework bậc cao mã nguồn mở viết bằng Python, tuân thủ nghiêm ngặt triết lý thiết kế *"The web framework for perfectionists with deadlines"* và nguyên lý DRY (*Don't Repeat Yourself*). Django phiên bản 6.1.2 cung cấp nền tảng phát triển vững chắc với cấu trúc module hóa phân minh.

#### A. Nguyên lý hoạt động của kiến trúc MVT (Model - View - Template)
Khác với mô hình MVC (*Model - View - Controller*) truyền thống, Django hiện thực hóa biến thể **MVT**:
1. **Model (Mô hình dữ liệu)**: Lớp trừu tượng hóa định nghĩa cấu trúc dữ liệu, các ràng buộc toàn vẹn, mối quan hệ thực thể và phương thức nghiệp vụ. Mỗi class Model kế thừa từ `django.db.models.Model` sẽ được tự động ánh xạ thành một bảng tương ứng trong cơ sở dữ liệu quan hệ thông qua hệ thống di chuyển lược đồ (*Migrations*).
2. **View (Điều khiển logic nghiệp vụ)**: Thành phần tiếp nhận các yêu cầu HTTP (*HttpRequest*), truy xuất và xử lý dữ liệu thông qua Model, thực thi các thuật toán nghiệp vụ hoặc tương tác với các dịch vụ bên ngoài (AI, thanh toán), sau đó quyết định trả về phản hồi thích hợp (*HttpResponse*, *JsonResponse*, hoặc kết xuất Template HTML).
3. **Template (Lớp trình bày giao diện)**: Tệp văn bản chứa mã HTML tĩnh kết hợp với ngôn ngữ mẫu Django Template Language (DTL). DTL cung cấp các cấu trúc điều khiển an toàn như `{% for %}`, `{% if %}`, bộ lọc định dạng `{{ value|floatformat }}` nhằm tách biệt hoàn toàn mã logic Backend ra khỏi giao diện người dùng.

```
CHU TRÌNH XỬ LÝ YÊU CẦU TRONG KIẾN TRÚC DJANGO MVT:
1. Web Browser (Khách hàng)  ──[ Gửi HTTP Request ]──> 2. urls.py (URL Dispatcher)
                                                               │
                                                       [ Điều hướng theo Path ]
                                                               │
                                                               v
6. Web Browser (Render UI)  <──[ Trả HTTP Response ]──  3. views.py (View Logic)
                                                               │       ▲
                                           [ Truy vấn ORM ]    │       │  [ Trả QuerySet ]
                                                               v       │
                                                        4. models.py (Model Layer)
                                                               │       ▲
                                             [ SQL Query ]     │       │  [ Raw Data ]
                                                               v       │
                                                        [ MySQL Database Engine ]
                                                               │
                                                       (Khi kết xuất giao diện)
                                                               │
                                                               v
                                                        5. templates (DTL Render)
```
*Hình 1.3: Chu trình xử lý yêu cầu HTTP trong kiến trúc Django MVT*

#### B. Cơ chế Django ORM (Object-Relational Mapping)
Django ORM cho phép lập trình viên tương tác với cơ sở dữ liệu hoàn toàn bằng cú pháp đối tượng Python mà không cần viết các câu lệnh SQL thô phức tạp. Những ưu thế kỹ thuật quan trọng của Django ORM trong dự án AgriSense bao gồm:
- **Ngăn chặn triệt để lỗ hổng SQL Injection**: ORM tự động thực hiện cơ chế tham số hóa câu truy vấn (*Parameterization*), phân tách hoàn toàn giữa dữ liệu đầu vào của người dùng và câu lệnh thực thi SQL.
- **Tối ưu hóa hiệu năng truy vấn liên kết**: Bài toán kinh điển $N+1$ truy vấn trong thương mại điện tử (khi hiển thị danh sách sản phẩm kèm tên nhà cung cấp và danh mục) được giải quyết triệt để thông qua phương thức `select_related()` (sử dụng phép `SQL JOIN` cho quan hệ `ForeignKey` 1-N) và `prefetch_related()` (thực thi truy vấn đa bảng độc lập kết hợp trong bộ nhớ cho quan hệ N-N).

#### C. Hệ thống xác thực và các tầng bảo mật tích hợp
- **Hệ thống xác thực tùy biến (*Custom User Model*)**: AgriSense kế thừa từ `AbstractUser`, mở rộng các thuộc tính nghiệp vụ chuyên biệt: vai trò người dùng (`role`: `customer`, `staff`, `admin`), số điện thoại, ảnh đại diện và nhóm khách hàng AI (`segment`).
- **Cơ chế phòng chống tấn công CSRF (*Cross-Site Request Forgery*)**: Tự động sinh mã token ngẫu nhiên gắn kèm trong cookie phiên và form nhập liệu (`{% csrf_token %}`), xác thực chữ ký số trên mọi yêu cầu thay đổi dữ liệu (POST, PUT, DELETE).
- **Mã hóa mật khẩu chuẩn công nghiệp**: Mật khẩu người dùng không bao giờ lưu trữ dưới dạng văn bản thuần (*Plaintext*) mà được băm bằng thuật toán `PBKDF2` (*Password-Based Key Derivation Function 2*) kết hợp giải thuật SHA-256 với muối ngẫu nhiên (*Salt*) và hàng trăm nghìn vòng lặp băm, chống lại các cuộc tấn công tra cứu bảng cầu vồng (*Rainbow Table*).

---

### 1.3.3. Hệ quản trị cơ sở dữ liệu quan hệ MySQL Server 26.7.0 và PyMySQL Driver
Hệ thống AgriSense quản lý dữ liệu giao dịch tài chính, thông tin tài khoản và nhật ký lô hàng – những dữ liệu đòi hỏi tính chính xác và nhất quán tuyệt đối. Do đó, hệ quản trị cơ sở dữ liệu quan hệ mã nguồn mở phổ biến nhất thế giới **MySQL Server Community Edition** được lựa chọn làm kho lưu trữ chính.

#### A. Đảm bảo toàn vẹn dữ liệu với chuẩn ACID
MySQL bảo đảm trọn vẹn 4 đặc tính quan trọng của hệ thống xử lý giao dịch:
- **Tính nguyên tử (*Atomicity*)**: Một chuỗi các thao tác nghiệp vụ hoặc thành công toàn bộ, hoặc thất bại toàn bộ mà không để lại trạng thái dở dang. Trong AgriSense, quá trình tạo đơn hàng yêu cầu: (1) Lưu bản ghi Order; (2) Lưu danh sách OrderItem; (3) Giảm trừ số lượng tồn kho `Product.stock`; (4) Xóa giỏ hàng hiện tại. Django cung cấp decorator `@transaction.atomic` để khóa phiên giao dịch; nếu bất kỳ bước nào phát sinh ngoại lệ (ví dụ: kho không đủ hàng), hệ thống lập tức thực thi lệnh `ROLLBACK`, khôi phục nguyên trạng thái cơ sở dữ liệu.
- **Tính nhất quán (*Consistency*)**: Mọi dữ liệu ghi nhận đều phải tuân thủ nghiêm ngặt các ràng buộc toàn vẹn: khóa chính (`PRIMARY KEY`), khóa ngoại (`FOREIGN KEY ON DELETE CASCADE/SET_NULL`), ràng buộc duy nhất (`UNIQUE`) và điều kiện kiểm tra (`CHECK`).
- **Tính cô lập (*Isolation*)**: Nhiều người dùng đặt hàng đồng thời trên cùng một sản phẩm nông sản sẽ được hệ thống cô lập phiên giao dịch thông qua cơ chế khóa hàng (*Row-level Locking*), ngăn ngừa hiện tượng tranh chấp điều kiện (*Race Condition*).
- **Tính bền vững (*Durability*)**: Khi giao dịch đã hoàn tất (*COMMIT*), dữ liệu được ghi xuống đĩa cứng an toàn thông qua cơ chế nhật ký ghi trước (*Write-Ahead Logging - WAL*) của công cụ lưu trữ InnoDB, không bị thất thoát kể cả khi xảy ra sự cố sập nguồn điện đột ngột.

#### B. Trình điều khiển kết nối PyMySQL và mã hóa ký tự utf8mb4
Trong môi trường Python 3.14 trên hệ điều hành Windows, các thư viện kết nối viết bằng ngôn ngữ C như `mysqlclient` thường đòi hỏi cài đặt bộ biên dịch Microsoft C++ Build Tools cồng kềnh. Dự án AgriSense giải quyết triệt để rào cản này bằng cách ứng dụng **PyMySQL 1.2.3** – driver thuần Python (Pure-Python MySQL Client) chuẩn hóa, được kích hoạt thông qua cơ chế monkey-patching:
```python
import pymysql
pymysql.install_as_MySQLdb()
```
Bên cạnh đó, cơ sở dữ liệu được định hình với bảng mã ký tự `utf8mb4` cùng bộ đối chiếu `utf8mb4_0900_ai_ci`. Bảng mã này hỗ trợ lưu trữ toàn diện 4 byte dữ liệu Unicode, xử lý mượt mà toàn bộ hệ thống tiếng Việt có dấu đầy đủ và các biểu tượng cảm xúc (*Emoji*), đồng thời hỗ trợ tìm kiếm không phân biệt dấu (*Accent-Insensitive*) và không phân biệt chữ hoa chữ thường (*Case-Insensitive*).

---

### 1.3.4. Công nghệ Frontend giao diện và trực quan hóa dữ liệu (Bootstrap 5.3.3, Chart.js 4.4)
- **Bootstrap 5.3.3 & Bootstrap Icons**: Khung giao diện CSS hàng đầu thế giới được xây dựng trên hệ thống lưới phản hồi 12 cột linh hoạt (*Flexbox & CSS Grid*). Bootstrap 5 đã loại bỏ hoàn toàn sự phụ thuộc vào jQuery, chuyển sang sử dụng JavaScript thuần (*Vanilla JS*) giúp giảm tải dung lượng tải trang, đảm bảo giao diện hiển thị tối ưu trên màn hình máy tính để bàn (Desktop), máy tính bảng (Tablet) và điện thoại thông minh (Mobile).
- **Chart.js 4.4**: Thư viện JavaScript mã nguồn mở chuyên dụng cho trực quan hóa dữ liệu trên nền thẻ `<canvas>` của HTML5. Chart.js được ứng dụng tại phân hệ Dashboard Quản trị để hiển thị các biểu đồ tương tác thời gian thực:
  - *Biểu đồ đường (Line Chart)*: Mô tả xu thế doanh thu bán hàng liên tục trong 30 ngày.
  - *Biểu đồ tròn (Doughnut Chart)*: Phản ánh cơ cấu phân bổ tỷ lệ phần trăm giữa 5 nhóm khách hàng AI.
  - *Biểu đồ cột (Bar Chart)*: Xếp hạng Top các sản phẩm nông sản có sản lượng tiêu thụ cao nhất.

---

## 1.4. Cơ sở lý thuyết về Trí tuệ nhân tạo (AI/LLM, Phân nhóm RFM, Gợi ý Content-based)

### 1.4.1. Tổng quan về Mô hình ngôn ngữ lớn (Large Language Models - LLMs) và Generative AI
Mô hình ngôn ngữ lớn (LLM) là bước phát triển nhảy vọt của ngành Trí tuệ nhân tạo, khởi nguồn từ công trình nghiên cứu mang tính bước ngoặt *"Attention Is All You Need"* của nhóm tác giả Vaswani cùng các nhà nghiên cứu tại Google Brain (2017). 

Khác với các kiến trúc mạng nơ-ron hồi quy truyền thống (RNN, LSTM) gặp nút thắt về khả năng xử lý song song và suy giảm gradient trên chuỗi dài, kiến trúc **Transformer** dựa trên **cơ chế tự chú ý (*Self-Attention Mechanism*)**. Cơ chế này cho phép mô hình tính toán mối tương quan động giữa mọi từ trong một câu văn bất kể khoảng cách vị trí của chúng:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Trong đó:
- $Q$ (*Query*), $K$ (*Key*), $V$ (*Value*) là các ma trận biểu diễn ngữ nghĩa của các token đầu vào được chiếu qua các không gian trọng số học được.
- $d_k$ là kích thước chiều của vector key, đóng vai trò nhân tử co dãn để tránh hiện tượng tràn giá trị hàm softmax.

```
+---------------------------------------------------------------------------------------------------+
|                        MÔ HÌNH THƯƠNG MẠI ĐÀM THOẠI (CONVERSATIONAL COMMERCE)                      |
+---------------------------------------------------------------------------------------------------+
| Khách hàng nhập văn bản:                                                                          |
| "Tôi muốn mua 2kg cà chua bi giao về số 15 Hai Bà Trưng Hà Nội, sđt 0987654321"                   |
|                                       │                                                           |
|                                       ▼                                                           |
| [NLP Intent & Entity Parsing]  ──> Trích xuất:                                                    |
|                                    - Tên nông sản: "cà chua bi"                                   |
|                                    - Số lượng: 2 kg                                               |
|                                    - Địa chỉ nhận hàng: "số 15 Hai Bà Trưng, Hà Nội"              |
|                                    - Số điện thoại liên hệ: "0987654321"                          |
|                                       │                                                           |
|                                       ▼                                                           |
| [Atomic Business Logic Engine] ──> - Kiểm tra tồn kho khả dụng (stock >= 2)                       |
|                                    - Khóa giao dịch (@transaction.atomic)                         |
|                                    - Tạo bản ghi Order (ORDxxxxxxxx) & OrderItem                  |
|                                    - Trừ tồn kho an toàn & Xóa giỏ hàng                           |
|                                       │                                                           |
|                                       ▼                                                           |
| [Instant Payment Generation]   ──> Sinh mã VietQR động trực tiếp trong khung chat:                |
|                                    "Đơn hàng ORD2026101401 đã khởi tạo thành công!                |
|                                     Tổng tiền: 90.000đ. Quý khách vui lòng quét mã bên dưới."    |
+---------------------------------------------------------------------------------------------------+
```
*Hình 1.4: Mô hình xử lý nghiệp vụ thương mại đàm thoại (Conversational Commerce)*

Khái niệm **Thương mại đàm thoại (*Conversational Commerce*)** ra đời dựa trên năng lực thấu hiểu ngữ cảnh vượt bậc của LLM. Thay vì giao diện web truyền thống đòi hỏi người dùng phải tự tìm kiếm, bấm chọn từng nút, thêm vào giỏ rồi qua nhiều trang thanh toán, LLM cho phép khách hàng thực hiện toàn bộ quy trình mua sắm chỉ bằng cách trò chuyện tự nhiên.

---

### 1.4.2. Kiến trúc dịch vụ Chatbot AI đa tầng (Multi-tier) và cơ chế Fallback Regex
Trong môi trường thực tế, việc phụ thuộc hoàn toàn vào một API Trí tuệ nhân tạo đám mây công cộng (Public Cloud LLM) tiềm ẩn nhiều rủi ro lớn đối với một hệ thống thương mại điện tử: nguy cơ vượt hạn mức số lần gọi (*Rate Limit*), sự cố đứt cáp quang quốc tế gây nghẽn mạng, độ trễ phản hồi cao, hoặc chi phí bản quyền API vượt ngân sách. Để đảm bảo tính sẵn sàng hoạt động 100% (*High Availability*), hệ thống AgriSense thiết kế kiến trúc Chatbot đa tầng thông minh:

```
SƠ ĐỒ LUỒNG ĐIỀU PHỐI TIN NHẮN CHATBOT ĐA TẦNG (MULTI-TIER ARCHITECTURE):
[ Người Dùng Gửi Tin Nhắn ]
             │
             v
 [ Kiểm Tra Cấu Hình API Key ] ──( Chưa có Key hoặc Rỗng )──> [ CHUYỂN NGAY SANG FALLBACK ]
             │                                                                │
     ( Đã có API Key )                                                        │
             │                                                                v
             v                                                  [ Phân Tích Kịch Bản Cố Định ]
 [ Nạp Ngữ Cảnh Nông Sản CSDL ]                                  ├── Kiểm tra kịch bản mua hàng
             │                                                   ├── Regex từ khóa (giá, nguồn gốc)
             v                                                   └── Tra cứu trạng thái đơn hàng
[ Gửi Yêu Cầu Tới LLM API ]                                                   │
  ├── Ưu tiên 1: Google Gemini 1.5 Flash                                      │
  └── Dự phòng 2: Groq (Llama-3.1-8B-Instant)                                 │
             │                                                                │
     ( Gọi Thành Công )             ( Bị Lỗi Mạng / Quá Timeout 10s )          │
             ├───[ Thành công ]──> [ Trả lời thông minh ]                     │
             └───[ Thất bại  ]────────────────────────────────────────────────┘
```
*Hình 1.5: Sơ đồ luồng điều phối tin nhắn Chatbot AI đa tầng (Multi-tier) và Fallback Regex*

#### A. Kỹ thuật nạp ngữ cảnh động (*Dynamic Context Injection*)
Để loại bỏ hiện tượng "ảo giác" (*Hallucination* - mô hình bịa đặt ra các thông tin không có thật về giá bán hoặc các mặt hàng không kinh doanh), dịch vụ Chatbot thực hiện trích xuất dữ liệu danh mục nông sản đang kích hoạt và tồn kho thực tế từ CSDL MySQL để nhúng trực tiếp vào System Prompt:
```
Dữ liệu sản phẩm thực tế trong cửa hàng:
- Cà chua bi hữu cơ Đà Lạt: Giá 45,000 đ/Hộp 500g, Tồn kho: 80 Hộp, Xuất xứ: Lâm Đồng, Nhà cung cấp: Hợp Tác Xã Rau Sạch Đà Lạt (VietGAP)
- Dưa lưới Huỳnh Long: Giá 95,000 đ/Quả 1.5kg, Tồn kho: 25 Quả, Xuất xứ: Tây Ninh (GlobalGAP)
...
```

#### B. Cơ chế Fallback Regex bằng máy trạng thái hữu hạn
Khi kết nối Internet bị gián đoạn hoặc API Cloud bị lỗi quá thời gian chờ (Timeout > 10 giây), hệ thống tự động kích hoạt bộ luật Fallback (`fallback.py`) dựa trên các biểu thức chính quy (*Regular Expressions*). Module này phân tích cấu trúc cú pháp câu tiếng Việt với các mẫu từ khóa phong phú:
- Nhóm câu hỏi về giá: `r'(bao nhiêu|giá|nhiêu tiền|chi phí)'`
- Nhóm câu hỏi về nguồn gốc: `r'(ở đâu|nguồn gốc|xuất xứ|trồng ở|nhà vườn)'`
- Nhóm câu hỏi về bảo quản: `r'(bảo quản|để được bao lâu|hạn dùng|tươi lâu)'`
- Nhóm tra cứu đơn hàng: `r'(đơn hàng|mã đơn|kiểm tra đơn|tình trạng đơn)'`

Cơ chế này cam kết thời gian phản hồi tức thì dưới 1 giây, bảo đảm khách hàng không bao giờ gặp phải tình trạng ứng dụng bị treo hay màn hình thông báo lỗi kỹ thuật.

---

### 1.4.3. Cơ sở lý thuyết và mô hình phân khúc khách hàng RFM (Recency - Frequency - Monetary)

#### A. Nguyên lý mô hình RFM
Mô hình RFM là phương pháp phân tích định lượng hành vi khách hàng kinh điển do Arthur Hughes phát triển, được ứng dụng rộng rãi trong các hệ thống Quản trị quan hệ khách hàng (CRM) và Khoa học dữ liệu bán lẻ:
- **Recency ($R$)**: Khoảng thời gian tính từ lần tương tác hoặc mua sắm gần đây nhất của khách hàng cho đến thời điểm hiện tại. Khách hàng có tương tác càng gần thì xác suất tái mua sắm và phản hồi chiến dịch tiếp thị càng cao.
- **Frequency ($F$)**: Tần suất mua hàng hoặc số lần tương tác trong một khoảng thời gian khảo sát nhất định. Thước đo này thể hiện độ gắn kết và lòng trung thành của người tiêu dùng đối với thương hiệu.
- **Monetary ($M$)**: Tổng giá trị bằng tiền mà khách hàng đã chi tiêu trên hệ thống. Chỉ số này phản ánh đóng góp tài chính trực tiếp và giá trị vòng đời khách hàng (*Customer Lifetime Value - CLV*).

#### B. Hiện thực hóa quy tắc phân nhóm trong AgriSense Platform
Trên nền tảng bán lẻ nông sản, do đặc tính mua sắm diễn ra thường xuyên theo chu kỳ sinh hoạt tuần của gia đình, AgriSense đã chuẩn hóa mô hình RFM thành hệ thống phân nhóm tự động gồm 5 phân khúc khách hàng rõ rệt:

*Bảng 1.3: Đặc tả quy tắc phân nhóm khách hàng theo mô hình RFM trong hệ thống AgriSense*

| Mã phân nhóm | Tên phân khúc khách hàng | Điều kiện logic xác định |
| :--- | :--- | :--- |
| `new` | Khách hàng mới | Đăng ký tài khoản trong 7 ngày gần nhất và chưa phát sinh đơn hàng nào trên hệ thống. |
| `interested` | Khách hàng tiềm năng quan tâm | Chưa phát sinh đơn hàng, nhưng đã tích lũy từ 5 sự kiện tương tác trở lên (xem sản phẩm, tìm kiếm, giỏ hàng). |
| `loyal` | Khách hàng trung thành | Đã hoàn tất từ 3 đơn hàng hợp lệ trở lên trong vòng 30 ngày gần nhất. |
| `at_risk` | Khách hàng có nguy cơ rời bỏ | Đã từng mua hàng nhưng không có bất kỳ đơn hàng nào mới trong hơn 30 ngày qua. |
| `normal` | Khách hàng thông thường | Các khách hàng có hoạt động mua bán ổn định, không thuộc các trường hợp phân nhóm đặc biệt trên. |

Quy trình cập nhật phân nhóm được tự động hóa thông qua Django Management Command `python manage.py update_segments`. Mỗi khi nhóm khách hàng thay đổi, hệ thống đồng thời ghi một bản ghi lịch sử vào bảng `behavior_usersegment` để phục vụ công tác đối soát và phân tích xu hướng dịch chuyển khách hàng theo thời gian.

---

### 1.4.4. Động cơ gợi ý sản phẩm cá nhân hóa (Content-based Filtering Recommendation Engine)

Hệ thống gợi ý (*Recommender Systems*) đóng vai trò là "chất xúc tác" giúp tăng trưởng doanh thu và cải thiện tỷ lệ chuyển đổi (*Conversion Rate*). Trong khi thuật toán Lọc cộng tác (*Collaborative Filtering*) đòi hỏi một ma trận tương tác người dùng - sản phẩm khổng lồ và thường xuyên gặp thất bại đối với các hệ thống mới triển khai (bài toán *Cold-Start*), giải thuật **Lọc dựa trên nội dung (*Content-based Filtering*)** kết hợp phân tích hành vi là giải pháp tối ưu cho AgriSense.

```
+---------------------------------------------------------------------------------------------------+
|                      CƠ CHẾ TÍNH ĐIỂM SỞ THÍCH VÀ ĐỀ XUẤT NÔNG SẢN THÔNG MINH                      |
+---------------------------------------------------------------------------------------------------+
| BƯỚC 1: Thu thập nhật ký tương tác người dùng trong 30 ngày qua (bảng behavior_userevent)          |
|                                       │                                                           |
| BƯỚC 2: Tính tổng điểm sở thích danh mục S(c) theo trọng số hành vi:                              |
|         - Xem chi tiết sản phẩm (view)       : w = 1.0 điểm                                       |
|         - Tìm kiếm từ khóa (search)          : w = 2.0 điểm                                       |
|         - Thêm vào giỏ hàng (add_to_cart)    : w = 3.0 điểm                                       |
|         - Đánh giá sản phẩm (review)         : w = 4.0 điểm                                       |
|         - Mua hàng thành công (purchase)     : w = 5.0 điểm                                       |
|                                       │                                                           |
| BƯỚC 3: Sắp xếp lấy Top 3 danh mục có điểm tích lũy cao nhất                                      |
|                                       │                                                           |
| BƯỚC 4: Bộ lọc loại trừ (Exclusion Filter):                                                       |
|         Loại bỏ toàn bộ các sản phẩm người dùng đã mua trước đó (bảng cart_orders_orderitem)      |
|                                       │                                                           |
| BƯỚC 5: Trích xuất sản phẩm còn tồn kho khả dụng (stock > 0) thuộc Top danh mục                    |
|                                       │                                                           |
| [ĐẶC BIỆT]: NẾU DỮ LIỆU TƯƠNG TÁC < 3 ĐIỂM HOẶC NGƯỜI DÙNG MỚI:                                    |
|             ==> Tự động kích hoạt Fallback: Gợi ý các sản phẩm nông sản bán chạy nhất             |
|                 (Bestsellers) được tổng hợp từ dữ liệu đơn hàng thực tế trong 30 ngày qua.        |
+---------------------------------------------------------------------------------------------------+
```
*Hình 1.6: Quy trình tính điểm sở thích và đề xuất nông sản thông minh*

Công thức toán học tính điểm sở thích của người dùng $u$ đối với danh mục nông sản $c$ trong cửa sổ thời gian $T = 30$ ngày được định nghĩa:

$$Score(u, c) = \\sum_{e \\in E_{u, c, T}} W(e)$$

Trong đó:
- $E_{u, c, T}$ là tập hợp các sự kiện tương tác của người dùng $u$ đối với danh mục $c$ trong khoảng thời gian $T$.
- $W(e)$ là hàm trọng số tương ứng với loại sự kiện:

$$W(e) = \\begin{cases} 
1.0 & \\text{nếu } e = \\text{'view'} \\\\
2.0 & \\text{nếu } e = \\text{'search'} \\\\
3.0 & \\text{nếu } e = \\text{'add\\_to\\_cart'} \\\\
4.0 & \\text{nếu } e = \\text{'review'} \\\\
5.0 & \\text{nếu } e = \\text{'purchase'}
\\end{cases}$$

Thuật toán đảm bảo tính công bằng, minh bạch, giúp khách hàng khám phá những nông sản mới mẻ thuộc đúng nhóm khẩu vị ưa thích mà không bị làm phiền bởi những mặt hàng họ đã sở hữu.

---

## 1.5. Công nghệ mã QR truy xuất nguồn gốc và cổng thanh toán tự động VietQR Napas 247

### 1.5.1. Tiêu chuẩn mã ma trận hai chiều Quick Response (QR Code) và ứng dụng truy xuất nguồn gốc

#### A. Cấu trúc vật lý và cơ chế sửa lỗi của mã QR theo tiêu chuẩn ISO/IEC 18004
Mã QR (*Quick Response Code*) là ký hiệu mã vạch ma trận hai chiều được phát minh vào năm 1994 bởi công ty Denso Wave (Nhật Bản) và sau đó được chuẩn hóa quốc tế theo tiêu chuẩn **ISO/IEC 18004**. So với mã vạch một chiều truyền thống (UPC/EAN) chỉ lưu trữ được tối đa 20 ký tự số, mã QR có khả năng nén tới 7,089 ký tự số hoặc 4,296 ký tự chữ số nhờ cấu trúc hình học thông minh:

```
CẤU TRÚC HÌNH HỌC CƠ BẢN CỦA MÃ QR (CHUẨN ISO/IEC 18004):
┌──────────────────────────────────────────────┐
│  [■■■■■■■]                         [■■■■■■■]  │  <-- Finder Pattern (Mẫu định vị góc)
│  [■     ■]                         [■     ■]  │
│  [■ ■■■ ■]  •••• Timing Pattern ••• [■ ■■■ ■]  │
│  [■■■■■■■]                         [■■■■■■■]  │
│                                              │
│               [■■■■■] <-- Alignment Pattern  │
│               [■   ■]     (Mẫu căn chỉnh)    │
│               [■■■■■]                        │
│                                              │
│  [■■■■■■■]            ██████████████         │
│  [■     ■]            ██  DATA    ██         │
│  [■ ■■■ ■]            ██  ENCODED ██         │  <-- Vùng dữ liệu mã hóa URL &
│  [■■■■■■■]            ██████████████         │      Khối sửa lỗi Reed-Solomon
└──────────────────────────────────────────────┘
   ^ Quiet Zone (Vùng đệm an toàn bao quanh)
```
*Hình 1.7: Cấu trúc hình học cơ bản của mã QR theo chuẩn quốc tế ISO/IEC 18004*

- **Mẫu định vị (*Finder Patterns*)**: Ba khối vuông đồng tâm nằm tại ba góc (trên-trái, trên-phải, dưới-trái) giúp cảm biến camera của điện thoại nhận dạng góc quét và định hướng mã vạch 360 độ mà không bị ảnh hưởng bởi hướng cầm máy.
- **Mẫu căn chỉnh (*Alignment Pattern*)**: Đảm bảo máy quét hiệu chỉnh đúng tọa độ hình học khi bề mặt bao bì dán nhãn bị cong vênh hoặc nghiêng góc.
- **Mẫu định thì (*Timing Patterns*)**: Dãy các điểm ảnh đen trắng xen kẽ kết nối giữa các khối định vị, xác định mật độ lưới tọa độ dữ liệu.
- **Thuật toán sửa lỗi Reed-Solomon**: Mã QR sở hữu cơ chế toán học tự phục hồi dữ liệu khi mã bị rách, mờ, dơ bẩn hoặc che khuất một phần trong quá trình lưu thông nông sản. AgriSense ứng dụng mức sửa lỗi **Level M (*Medium*)** cho phép phục hồi toàn vẹn thông tin ngay cả khi mã bị tổn hại vật lý tới **15% diện tích**.

#### B. Quy trình sinh mã QR lô hàng nông sản tự động trong AgriSense
Trong module `apps/traceability/qr_generator.py`, hệ thống hiện thực hóa hàm sinh ảnh mã QR chuẩn PNG:
1. Khi quản trị viên tạo một lô hàng thu hoạch mới (`ProductBatch`), hệ thống tự động sinh một mã định danh duy nhất (ví dụ: `BATCH-20261014-001`).
2. Mã QR được nạp dữ liệu là đường dẫn URL tra cứu công khai: `http://<domain_or_lan_ip>:8000/trace/<batch_code>/`.
3. Nhằm giải quyết bài toán kiểm thử đồ án trên thiết bị di động thực tế khi máy chủ chạy trên máy tính cục bộ kết nối cùng mạng Wi-Fi, hàm `get_local_lan_ip()` sử dụng socket mạng để tự động dò tìm địa chỉ IPv4 nội bộ (dải `192.168.x.x`):
```python
def get_local_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"
```
Nhờ đó, người thẩm định chỉ cần dùng camera điện thoại quét mã QR hiển thị trên màn hình máy tính là có thể mở ngay hồ sơ nguồn gốc lô hàng mà không gặp lỗi "không thể kết nối localhost".

---

### 1.5.2. Tiêu chuẩn mã thanh toán số VietQR Napas 247 và quy chuẩn EMVCo

#### A. Tổng quan chuẩn thanh toán VietQR và EMVCo
Trong chiến lược phát triển kinh tế số, Ngân hàng Nhà nước Việt Nam cùng Công ty Cổ phần Thanh toán Quốc gia Việt Nam (NAPAS) đã chính thức ban hành bộ tiêu chuẩn **VietQR** dựa trên tiêu chuẩn kỹ thuật quốc tế **EMVCo Merchant-Presented Mode**.

Mã VietQR là một chuỗi ký tự mã hóa theo cấu trúc TLV (*Tag - Length - Value*) chuẩn xác, tích hợp các trường dữ liệu định danh tài chính bắt buộc:
- **Tag 00**: Định dạng phiên bản payload (`01`).
- **Tag 01**: Phương thức khởi tạo (`12` - QR động dùng cho từng giao dịch đơn lẻ).
- **Tag 38**: Thông tin định danh đơn vị thụ hưởng (Bao gồm mã số định danh ngân hàng BIN code quốc gia theo chuẩn Ngân hàng Nhà nước và số tài khoản ngân hàng của chủ doanh nghiệp).
- **Tag 53**: Mã loại tiền tệ (`704` là mã ISO của Việt Nam Đồng - VND).
- **Tag 54**: Số tiền thanh toán giao dịch chính xác.
- **Tag 62**: Thông tin bổ sung giao dịch (Nội dung chuyển khoản, mã số đơn hàng).
- **Tag 63**: Mã kiểm tra vòng tròn CRC-16 (*Cyclic Redundancy Check*) chống sai lệch dữ liệu truyền dẫn.

```
+---------------------------------------------------------------------------------------------------+
|               SO SÁNH QUY TRÌNH THANH TOÁN CHUYỂN KHOẢN TRUYỀN THỐNG VÀ VIETQR NAPAS 247           |
+---------------------------------------------------------------------------------------------------+
| ❌ QUY TRÌNH CHUYỂN KHOẢN TRUYỀN THỐNG (NHIỀU RỦI RO):                                            |
|    Bước 1: Khách hàng mở app ngân hàng -> Tìm kiếm tên ngân hàng thụ hưởng                         |
|    Bước 2: Gõ thủ công 10-14 chữ số tài khoản (Dễ nhầm lẫn số 0 và O, thừa thiếu số)              |
|    Bước 3: Nhập số tiền thủ công (Nguy cơ chuyển thừa hoặc thiếu 1 chữ số 0)                       |
|    Bước 4: Nhập nội dung chuyển tiền (Thường gõ sai cú pháp, gây khó khăn cho việc đối soát)       |
|    ==> Tỷ lệ xác nhận đơn hàng chậm trễ, phát sinh khiếu nại và tốn nhân sự đối soát thủ công!     |
|                                                                                                   |
| ✔️ QUY TRÌNH THANH TOÁN VIETQR TỰ ĐỘNG CỦA AGRISENSE (1 CHẠM TỨC THÌ):                           |
|    Bước 1: Hệ thống tự động sinh ảnh VietQR động gắn kèm số tiền và mã đơn hàng (ORDxxxxxxxx)     |
|    Bước 2: Khách hàng chỉ cần mở camera hoặc tính năng "Quét QR" trên bất kỳ app ngân hàng nào    |
|    Bước 3: Toàn bộ thông tin: Ngân hàng, Chủ tài khoản, Số tiền chính xác, Nội dung được điền sẵn |
|    Bước 4: Khách hàng xác thực sinh trắc học (vân tay / FaceID) để hoàn tất trong 3 giây          |
|    ==> Chính xác tuyệt đối 100%, bảo mật cao, nâng cao trải nghiệm mua sắm số văn minh!           |
+---------------------------------------------------------------------------------------------------+
```
*Hình 1.8: So sánh quy trình thanh toán chuyển khoản truyền thống và thanh toán tự động VietQR Napas 247*

#### B. Tích hợp VietQR trong AgriSense Platform
Trong module `apps/cart_orders/vietqr.py`, hàm `get_vietqr_url()` tự động khởi tạo URL ảnh mã QR theo giao thức chuẩn mở:
```python
def get_vietqr_url(order, template='compact2'):
    bank_id = getattr(settings, 'VIETQR_BANK_ID', 'MB')
    account_no = getattr(settings, 'VIETQR_ACCOUNT_NO', '0922334455')
    account_name_raw = getattr(settings, 'VIETQR_ACCOUNT_NAME', 'NGUYEN HONG HOANG')
    
    amount = int(order.final_amount)
    memo = order.order_code
    account_name = quote(account_name_raw)
    encoded_memo = quote(memo)
    
    return (
        f"https://img.vietqr.io/image/{bank_id}-{account_no}-{template}.png"
        f"?amount={amount}&addInfo={encoded_memo}&accountName={account_name}"
    )
```
Mã QR này được hiển thị đồng bộ tại hai vị trí trọng yếu: trên trang chi tiết đơn hàng thanh toán của người dùng và gửi trực tiếp dưới dạng hình ảnh tương tác ngay trong khung chat của Chatbot AI khi khách hàng thực hiện lệnh đặt hàng qua giọng nói hoặc văn bản tự nhiên.

---

### Kết luận Chương 1

Chương 1 đã hoàn thành việc xây dựng nền tảng lý luận khoa học và khảo sát kỹ thuật toàn diện cho đề tài **AgriSense Platform**:
1. Làm rõ tính cấp thiết của việc số hóa chuỗi cung ứng nông sản sạch tại Việt Nam theo định hướng mô hình "Từ nông trại đến bàn ăn", đồng thời chỉ ra khoảng trống công nghệ của các nền tảng thương mại điện tử hiện tại trong việc minh bạch hóa nguồn gốc và cá nhân hóa trải nghiệm.
2. Thiết lập cơ sở công nghệ vững chắc dựa trên ngăn xếp **Python 3.14**, **Django Framework 6.1.2**, **MySQL Server 26.7.0**, bảo đảm các tiêu chuẩn công nghiệp về kiến trúc MVT, cơ chế ORM chống lỗi SQL Injection và giao dịch nguyên tử ACID bảo vệ tính toàn vẹn của kho hàng.
3. Nghiên cứu sâu sắc phương pháp luận ứng dụng Trí tuệ nhân tạo: từ nguyên lý Transformer của mô hình ngôn ngữ lớn (LLM), thiết kế kiến trúc Chatbot đàm thoại chốt đơn tự động kết hợp bộ luật Fallback Regex dự phòng, đến giải thuật phân khúc khách hàng RFM và động cơ gợi ý Content-based Filtering theo trọng số hành vi.
4. Hệ thống hóa cơ sở kỹ thuật của mã QR hai chiều theo chuẩn quốc tế ISO/IEC 18004 phục vụ truy xuất nguồn gốc nông sản và quy chuẩn thanh toán số không tiền mặt VietQR Napas 247 theo chuẩn EMVCo.

Toàn bộ hệ thống cơ sở lý thuyết và công nghệ được tổng hợp trong chương này chính là kim chỉ nam vững chắc để nhóm tiến hành công tác **Phân tích yêu cầu và Thiết kế hệ thống AgriSense Platform** một cách bài bản, chặt chẽ trong **Chương 2**.

---

# CHƯƠNG 2. PHÂN TÍCH YÊU CẦU VÀ THIẾT KẾ HỆ THỐNG AGRISENSE PLATFORM

## 2.1. Phân tích hiện trạng và khảo sát thực tế quy trình mua bán nông sản
Qua khảo sát thực tế quy trình mua bán nông sản sạch giữa khách hàng, hộ nông dân và quản trị viên, nhóm xác định quy trình nghiệp vụ số bao gồm 4 luồng chính: Luồng duyệt và kiểm tra thông tin nông sản (kèm truy xuất mã QR); Luồng đặt hàng và thanh toán không tiền mặt qua VietQR; Luồng tư vấn và chốt đơn tự động qua Chatbot AI; và Luồng quản trị kho bãi, lô hàng cùng báo cáo doanh số.

## 2.2. Đặc tả yêu cầu bài toán (Yêu cầu chức năng và Yêu cầu phi chức năng)
- **Yêu cầu chức năng**: Quản lý đăng ký, đăng nhập và phân quyền 3 cấp (Customer, Staff, Admin); Quản lý danh mục và nông sản (hình ảnh, giá cả, tồn kho, xuất xứ, mùa vụ, chứng nhận); Giỏ hàng, đặt hàng và hủy đơn tự động hoàn kho; Cổng thanh toán VietQR Napas 247; Sinh mã QR lô hàng; Ghi nhận hành vi và phân nhóm RFM; Gợi ý nông sản cá nhân hóa; Chatbot AI tư vấn và lên đơn trực tiếp; Dashboard quản trị có biểu đồ Chart.js và tính năng xuất file Excel (`.xlsx`).
- **Yêu cầu phi chức năng**: Thời gian phản hồi trang danh sách < 1.5 giây; Hỗ trợ hiển thị mượt mà trên cả máy tính và điện thoại di động (Responsive); Bảo mật thông tin người dùng bằng mật khẩu mã hóa PBKDF2 và cơ chế chống tấn công CSRF; Chatbot có cơ chế Fallback Regex phản hồi tức thì dưới 1 giây kể cả khi API ngoài bị gián đoạn.

## 2.3. Thiết kế kiến trúc tổng thể hệ thống (Django MVT & Service Layer)
AgriSense được cấu trúc theo mô hình kiến trúc MVT hướng dịch vụ (Service-Oriented MVT), bao gồm 8 phân hệ ứng dụng (`apps`) độc lập nhưng liên kết chặt chẽ: `accounts`, `products`, `cart_orders`, `behavior`, `recommendation`, `chatbot`, `traceability`, `dashboard`.

## 2.4. Thiết kế các sơ đồ UML (Use Case, Activity, Class, Sequence Diagram)
- **Sơ đồ Use Case**: Đặc tả các tác nhân Guest, Customer, Staff, Admin và AI System tương tác với các phân hệ chức năng.
- **Sơ đồ Activity**: Mô tả tiến trình đặt hàng có trừ kho nguyên tử (`@transaction.atomic`) và tiến trình phân nhóm khách hàng định kỳ.
- **Sơ đồ Class Diagram**: Mô tả cấu trúc các lớp Model Django, các thuộc tính, phương thức và mối quan hệ 1-N, N-N giữa các thực thể.
- **Sơ đồ Sequence Diagram**: Mô tả trình tự luồng gọi từ người dùng đến Chatbot View, gọi API LLM và chuyển hướng sang Fallback Regex khi xảy ra sự cố mạng.

## 2.5. Thiết kế cơ sở dữ liệu quan hệ (12 Model, 26 bảng MySQL, ERD)
Cơ sở dữ liệu `nongsan_db` được thiết kế chuẩn hóa bậc 3 (3NF) gồm 12 Model nghiệp vụ cốt lõi:
- **Nhóm Tài khoản**: `accounts_user` (kế thừa AbstractUser, thêm role, segment, phone), `accounts_useraddress` (sổ địa chỉ).
- **Nhóm Sản phẩm**: `products_category`, `products_supplier`, `products_product`, `products_productreview`.
- **Nhóm Giỏ hàng & Đơn hàng**: `cart_orders_cart`, `cart_orders_cartitem`, `cart_orders_order`, `cart_orders_orderitem`.
- **Nhóm Hành vi & AI**: `behavior_userevent`, `behavior_usersegment`, `chatbot_chatsession`, `chatbot_chatmessage`.
- **Nhóm Truy xuất nguồn gốc**: `traceability_productbatch`, `traceability_traceabilityrecord`.

### Kết luận Chương 2
Chương 2 đã hoàn thành trọn vẹn giai đoạn phân tích và thiết kế hệ thống, xác định rõ các sơ đồ kiến trúc UML và cấu trúc 12 Model CSDL MySQL. Đây là cơ sở cốt lõi để tiến hành hiện thực hóa mã nguồn trong Chương 3.

---

# CHƯƠNG 3. HIỆN THỰC HÓA HỆ THỐNG, KẾT QUẢ THỰC NGHIỆM VÀ KIỂM THỬ

## 3.1. Hiện thực hóa các phân hệ chức năng cốt lõi (Tài khoản, Sản phẩm, Đơn hàng)
Nhóm đã hiện thực hóa toàn bộ các phân hệ chức năng cốt lõi:
- **Phân hệ Tài khoản (`apps/accounts`)**: Đăng ký, đăng nhập bảo mật Django Auth, quản lý hồ sơ và sổ địa chỉ linh hoạt.
- **Phân hệ Sản phẩm (`apps/products`)**: Hiển thị danh mục trực quan, bộ lọc đa năng, tìm kiếm từ khóa tiếng Việt không dấu và đánh giá sao.
- **Phân hệ Giỏ hàng & Đặt hàng (`apps/cart_orders`)**: Quản lý giỏ hàng theo session/database, tính phí giao hàng thông minh (30.000đ, miễn phí từ 500.000đ), trừ tồn kho an toàn trong giao dịch `@transaction.atomic`, hủy đơn hoàn tồn kho tự động.

## 3.2. Hiện thực hóa phân hệ AI (Chatbot đàm thoại lên đơn, RFM và Gợi ý cá nhân hóa)
- **Theo dõi hành vi (`apps/behavior`)**: `BehaviorTrackingMiddleware` tự động ghi nhận các sự kiện xem và tìm kiếm; phân loại khách hàng theo 5 nhóm RFM qua command `python manage.py update_segments`.
- **Động cơ gợi ý (`apps/recommendation`)**: Tính điểm sở thích danh mục theo trọng số tương tác, loại trừ sản phẩm đã mua và tự động đề xuất lên khối "Gợi ý cho bạn" trên trang chủ.
- **Chatbot AI & Đặt hàng đàm thoại (`apps/chatbot`)**: Tích hợp Gemini 1.5 Flash / Groq LLM + Fallback Regex tiếng Việt chuyên sâu; hỗ trợ đặt hàng bằng câu lệnh tự nhiên (ví dụ: *"Tôi muốn mua 2kg cà chua bi giao về Cầu Giấy Hà Nội"*), tự động trừ kho và gửi mã VietQR thanh toán tức thì ngay trong khung chat.

## 3.3. Hiện thực hóa phân hệ Truy xuất nguồn gốc QR và Cổng thanh toán VietQR Napas 247
- **Truy xuất nguồn gốc (`apps/traceability`)**: Tự động sinh file ảnh QR chuẩn PNG cho từng lô hàng, liên kết tới URL `http://127.0.0.1:8000/trace/<batch_code>/` hiển thị thông tin nông trại, ngày thu hoạch, chứng nhận VietGAP/GlobalGAP công khai.
- **Cổng VietQR Napas 247**: Tích hợp sinh mã VietQR động theo chuẩn ngân hàng MBBank, hiển thị trực quan trên trang chi tiết đơn hàng và trong khung chat AI.

## 3.4. Hiện thực hóa Dashboard Quản trị kinh doanh Chart.js và trích xuất Excel (.xlsx)
Xây dựng trang Dashboard quản trị riêng biệt tại `/dashboard/` được bảo vệ bằng `@method_decorator(staff_member_required)`:
- **Biểu đồ đường (Line Chart)**: Xu hướng biến động doanh số bán hàng trong 30 ngày gần nhất.
- **Biểu đồ tròn (Doughnut Chart)**: Tỷ lệ phân bổ cơ cấu nhóm khách hàng AI (`new`, `interested`, `loyal`, `at_risk`, `normal`).
- **Biểu đồ cột (Bar Chart)**: Top 5 nông sản có sản lượng tiêu thụ cao nhất.
- **Xuất file báo cáo Excel (`.xlsx`)**: Ứng dụng thư viện `openpyxl` xuất danh sách đơn hàng có định dạng tiêu đề màu thương hiệu, đóng khung ô và định dạng tiền tệ chuyên nghiệp.

## 3.5. Kết quả thực nghiệm dữ liệu mẫu (Seed Data) và Kiểm thử tự động (43 Tests PASS)
- **Lệnh khởi tạo dữ liệu mẫu (`python manage.py seed_data`)**: Tạo thành công 6 danh mục, 7 nhà cung cấp, 32 sản phẩm, 24 người dùng mẫu, 52 đơn hàng, 11 lô hàng có mã QR và 165 sự kiện tương tác.
- **Bộ kiểm thử tự động (Unit Tests)**: Viết và thực thi 43 kiểm thử tự động với `TestCase` trên tất cả các phân hệ: Kết quả đạt **43/43 tests PASS** (100% thành công, 0 errors, 0 failures).

### Kết luận Chương 3
Chương 3 đã chứng minh hệ thống AgriSense Platform được hiện thực hóa đầy đủ, chính xác và vận hành ổn định 100% trên môi trường thực tế, vượt qua toàn bộ các ca kiểm thử tự động và đáp ứng xuất sắc các mục tiêu đã đề ra.

---

# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 1. Những kết quả và đóng góp chính đã đạt được
1. Xây dựng hoàn chỉnh nền tảng web thương mại điện tử chuyên biệt cho nông sản (AgriSense Platform) với kiến trúc MVT hướng dịch vụ chuẩn hóa gồm 8 phân hệ và 12 Model cơ sở dữ liệu quan hệ MySQL.
2. Ứng dụng thành công Trí tuệ nhân tạo vào thực tiễn: Chatbot đàm thoại lên đơn hàng trực tiếp, phân nhóm khách hàng theo mô hình RFM và gợi ý sản phẩm cá nhân hóa theo thuật toán Content-based Filtering.
3. Minh bạch hóa chuỗi cung ứng nông sản thông qua mã QR truy xuất nguồn gốc lô hàng chuẩn ISO và tích hợp cổng thanh toán số VietQR Napas 247 tiện lợi.
4. Xây dựng bảng điều khiển quản trị Dashboard trực quan với biểu đồ tương tác Chart.js và tính năng trích xuất báo cáo doanh số Excel (`.xlsx`) chuyên nghiệp.
5. Toàn bộ hệ thống được bảo vệ bằng 43 Unit Tests tự động đạt tỷ lệ thành công 100%.

## 2. Hạn chế còn tồn tại
- Hệ thống mới vận hành trên môi trường máy chủ cục bộ (Localhost), chưa triển khai lên hạ tầng Cloud thực tế.
- Thuật toán gợi ý sản phẩm dừng lại ở mức Content-based Filtering, chưa mở rộng sang Collaborative Filtering do dữ liệu tương tác người dùng ban đầu còn giới hạn.

## 3. Hướng nghiên cứu và phát triển tiếp theo
- Nghiên cứu tích hợp mô hình học sâu (Deep Learning) và lọc cộng tác (Collaborative Filtering) để nâng cao độ chính xác của động cơ gợi ý.
- Phát triển ứng dụng di động đa nền tảng (Flutter / React Native) đồng bộ với hệ thống Backend Django REST Framework.
- Mở rộng tích hợp công nghệ Blockchain vào nhật ký truy xuất nguồn gốc để bảo đảm tính bất biến tuyệt đối của dữ liệu canh tác nông sản.

---

# TÀI LIỆU THAM KHẢO

- [1] Django Software Foundation (2026), *Django Documentation (Version 6.1)*, https://docs.djangoproject.com/.
- [2] Oracle Corporation (2026), *MySQL 26.7 Reference Manual*, https://dev.mysql.com/doc/.
- [3] Mark Lutz (2013), *Learning Python (5th Edition)*, O'Reilly Media.
- [4] Aurélien Géron (2022), *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (3rd Edition)*, O'Reilly Media.
- [5] Google AI (2024), *Gemini API Documentation & Prompt Engineering Guide*, https://ai.google.dev/.
- [6] VietQR Standard (2023), *Hướng dẫn kỹ thuật chuẩn kết nối thanh toán VietQR Napas 247*, https://vietqr.net/.
- [7] Bộ Nông nghiệp và Phát triển Nông thôn (2022), *Tiêu chuẩn Quốc gia TCVN 11892-1:2017 về Thực hành Nông nghiệp Tốt (VietGAP) - Trồng trọt*.
- [8] Ian Sommerville (2015), *Software Engineering (10th Edition)*, Pearson.

---

# PHỤ LỤC

### Phụ lục 1: Mẫu phiếu khảo sát nhu cầu người tiêu dùng nông sản sạch
Khảo sát gồm 10 câu hỏi trắc nghiệm đánh giá mức độ quan tâm của khách hàng đối với thông tin truy xuất nguồn gốc qua mã QR, sự tiện lợi của thanh toán VietQR và mức độ hài lòng khi được Chatbot AI tư vấn trực tuyến.

### Phụ lục 2: Cấu hình biến môi trường và tài khoản thử nghiệm
Hệ thống quản lý cấu hình thông qua file biến môi trường bảo mật `.env`:
- Tài khoản Quản trị tối cao (Admin Demo): `demo_admin` / Mật khẩu: `Admin@123`
- Tài khoản Khách hàng trải nghiệm (Customer Demo): `demo_customer` / Mật khẩu: `Demo@123`
- Cấu hình VietQR: Ngân hàng Quân Đội (MBBank) - STK: `0922334455` - Chủ TK: `NGUYEN HONG HOANG`.

---

# TIẾN ĐỘ THỰC HIỆN ĐỒ ÁN

### Bảng 4.1. Tiến độ thực hiện đề tài

| TT | Nội dung thực hiện | Tiến độ thực hiện |
| :---: | :--- | :--- |
| **1** | Xây dựng đề cương | Từ 14/10/2026 đến 15/10/2026 |
| **2** | Nộp đề cương | Từ 15/10/2026 đến 16/10/2026 |
| **3** | Bảo vệ đề cương | Từ 16/10/2026 đến 19/10/2026 |
| **4** | Viết các nội dung của Bài tập lớn | Từ 20/10/2026 đến 30/11/2026 |
| **5** | Hoàn thiện các nội dung của Bài tập lớn theo ý kiến của giảng viên | Từ 30/11/2026 đến 07/12/2026 |
| **6** | Nộp Báo cáo | Từ 07/12/2026 |
| **7** | Thi vấn đáp | Theo lịch Khảo thí |

<br>

| | NHÓM TRƯỞNG SINH VIÊN THỰC HIỆN |
| :--- | :---: |
| | *(Ký ghi rõ họ tên)* |
| | <br><br>**Nguyễn Hồng Hoàng** |
