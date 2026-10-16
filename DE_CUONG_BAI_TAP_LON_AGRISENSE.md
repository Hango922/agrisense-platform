| BỘ GIÁO DỤC VÀ ĐÀO TẠO  TRƯỜNG ĐẠI HỌC CÔNG NGHỆ ĐÔNG Á  https://upload.wikimedia.org/wikipedia/vi/a/a1/Logo_%C4%90%E1%BA%A1i_h%E1%BB%8Dc_C%C3%B4ng_ngh%E1%BB%87_%C4%90%C3%B4ng_%C3%81.png  ĐỀ CƯƠNG BÀI TẬP LỚN  Môn: Đồ án chuyên ngành Công nghệ phần mềm  TÊN ĐỀ BÀI TẬP LỚN  (Cỡ chữ 16)  Mã sinh viên   | Tên sinh viên   | Lớp hành chính   |
| :--- | :--- | :--- |
|  |  |  |
|  |  |  |
|  |  |  |

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
  - [1.2. Khảo sát các công trình liên quan và những vấn đề còn tồn tại](#12-khảo-sát-các-công-trình-liên-quan-và-những-vấn-đề-còn-tồn-tại)
  - [1.3. Tổng quan nền tảng công nghệ phát triển hệ thống (Python, Django MVT, MySQL Server)](#13-tổng-quan-nền-tảng-công-nghệ-phát-triển-hệ-thống-python-django-mvt-mysql-server)
  - [1.4. Cơ sở lý thuyết về Trí tuệ nhân tạo (AI/LLM, Phân nhóm RFM, Gợi ý Content-based)](#14-cơ-sở-lý-thuyết-về-trí-tuệ-nhân-tạo-aillm-phân-nhóm-rfm-gợi-ý-content-based)
  - [1.5. Công nghệ mã QR truy xuất nguồn gốc và cổng thanh toán tự động VietQR Napas 247](#15-công-nghệ-mã-qr-truy-xuất-nguồn-gốc-và-cổng-thanh-toán-tự-động-vietqr-napas-247)
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

- **Bảng 1.1**: Thông số môi trường và công nghệ phát triển hệ thống AgriSense
- **Bảng 2.1**: Đặc tả 12 Model cơ sở dữ liệu cốt lõi phân theo nhóm nghiệp vụ
- **Bảng 2.2**: Đặc tả các quy tắc phân nhóm khách hàng theo mô hình RFM
- **Bảng 3.1**: Kết quả thống kê khởi tạo dữ liệu mẫu (Seed Data)
- **Bảng 3.2**: Tổng hợp kết quả kiểm thử tự động 43 Unit Tests theo phân hệ
- **Bảng 4.1**: Kế hoạch tiến độ thực hiện đề tài Đồ án chuyên ngành

---

# DANH MỤC CÁC HÌNH VẼ

- **Hình 1.1**: Sơ đồ kiến trúc phân tầng hệ thống AgriSense Platform (MVT & Services)
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
Thương mại điện tử (E-Commerce) nông nghiệp là quá trình ứng dụng công nghệ thông tin và truyền thông kỹ thuật số vào mọi khâu từ giới thiệu, tiếp thị, đặt hàng, thanh toán đến truy xuất nguồn gốc nông sản. Đặc thù của nông sản sạch đòi hỏi tính tức thời cao về mặt thông tin chất lượng, ngày thu hoạch và điều kiện bảo quản. Việc áp dụng các chuẩn thực hành nông nghiệp tốt như VietGAP, GlobalGAP đòi hỏi dữ liệu nhật ký canh tác phải được liên kết chặt chẽ với từng lô hàng lưu thông trên thị trường.

## 1.2. Khảo sát các công trình liên quan và những vấn đề còn tồn tại
Khảo sát các nền tảng thương mại điện tử hiện nay (Shopee, Tiki, Lazada, Bách Hóa Xanh online, Sói Biển) cho thấy:
- Các sàn lớn có quy mô rộng nhưng nông sản sạch chỉ là một nhánh nhỏ, thiếu tính năng chuyên biệt về quản lý lô hàng và tra cứu nguồn gốc bằng mã QR động.
- Các website bán nông sản hữu cơ chuyên biệt của doanh nghiệp nhỏ còn đơn sơ, thiếu công cụ AI tư vấn khách hàng tự động 24/7 và giao diện chưa tối ưu trải nghiệm trên thiết bị di động.
- Quy trình thanh toán chuyển khoản ngân hàng đa số thực hiện thủ công (khách tự nhập số tài khoản, số tiền và nội dung), dẫn đến tỷ lệ sai sót và chậm trễ trong xác nhận đơn hàng.

## 1.3. Tổng quan nền tảng công nghệ phát triển hệ thống (Python, Django MVT, MySQL Server)
Hệ thống AgriSense được xây dựng trên nền tảng công nghệ mã nguồn mở mạnh mẽ và hiện đại bậc nhất:
- **Ngôn ngữ Python 3.14.3**: Ngôn ngữ lập trình bậc cao với cú pháp rõ ràng, thư viện phong phú và khả năng tích hợp trí tuệ nhân tạo, xử lý dữ liệu mạnh mẽ.
- **Web Framework Django 6.1.2**: Kiến trúc MVT (Model - View - Template) hoàn chỉnh, tích hợp sẵn hệ thống xác thực người dùng bảo mật, cơ chế ORM tối ưu truy vấn CSDL, bảo vệ CSRF và routing linh hoạt.
- **Hệ quản trị CSDL MySQL Community Server 26.7.0 kết hợp PyMySQL Driver 1.2.3**: Hệ quản trị CSDL quan hệ hàng đầu thế giới, đảm bảo toàn vẹn dữ liệu qua cơ chế khóa và giao dịch ACID (`@transaction.atomic`).
- **Giao diện Bootstrap 5.3.3 & Chart.js 4.4**: Thiết kế Responsive chuẩn hiện đại và trực quan hóa dữ liệu thống kê bằng biểu đồ tương tác.

| Thành phần kỹ thuật | Công nghệ / Phiên bản | Vai trò trong hệ thống |
| :--- | :--- | :--- |
| Hệ điều hành | Windows 11 Pro (64-bit) | Môi trường phát triển chuẩn |
| Ngôn ngữ | Python 3.14.3 | Nền tảng Backend chính |
| Web Framework | Django 6.1.2 | Xử lý nghiệp vụ MVT, ORM, Auth |
| CSDL | MySQL Server 26.7.0 | Lưu trữ dữ liệu quan hệ (utf8mb4) |
| CSDL Driver | PyMySQL 1.2.3 | Tương thích Python 3.14 không cần C++ compiler |
| UI Framework | Bootstrap 5.3.3 | Giao diện Responsive Desktop/Mobile |
| Trực quan hóa | Chart.js 4.4 | 3 biểu đồ tương tác trên Dashboard |
| Xuất báo cáo | openpyxl 3.1.5 | Xuất file Excel (.xlsx) danh sách đơn hàng |
| Mã QR | qrcode 7.4.2 & Pillow 11.0.0 | Tự động sinh ảnh mã QR PNG chuẩn ISO |
| AI / LLM | Gemini 1.5 Flash / Groq | Chatbot đàm thoại và phân tích ngữ cảnh |

## 1.4. Cơ sở lý thuyết về Trí tuệ nhân tạo (AI/LLM, Phân nhóm RFM, Gợi ý Content-based)
- **Mô hình ngôn ngữ lớn (LLM - Gemini 1.5 Flash / Groq)**: Ứng dụng công nghệ Transformer để thấu hiểu câu hỏi tự nhiên của khách hàng về đặc tính nông sản, giá bán, công thức nấu ăn và chuyển đổi thành hành động nghiệp vụ (lên đơn hàng trực tiếp).
- **Mô hình phân loại khách hàng RFM**: Phân nhóm khách hàng định kỳ thành 5 nhóm dựa trên tương tác gần nhất (Recency), tần suất mua hàng (Frequency) và số lượng sự kiện: `new` (mới tạo), `interested` (quan tâm nhiều), `loyal` (khách thân thiết), `at_risk` (nguy cơ rời bỏ), `normal` (tiêu chuẩn).
- **Động cơ gợi ý Content-based Filtering**: Tính toán vector sở thích danh mục của người dùng dựa trên trọng số tương tác (`view: 1.0`, `search: 2.0`, `add_to_cart: 3.0`, `purchase: 5.0`, `review: 4.0`) để đề xuất nông sản phù hợp nhất, kết hợp cơ chế fallback gợi ý sản phẩm bán chạy khi chưa đủ dữ liệu.

## 1.5. Công nghệ mã QR truy xuất nguồn gốc và cổng thanh toán tự động VietQR Napas 247
- **Mã QR truy xuất nguồn gốc**: Sử dụng thư viện `qrcode` và `Pillow` để tự động sinh mã QR PNG chuẩn ISO cho từng lô hàng (`ProductBatch`). Mỗi mã QR gắn với URL công khai duy nhất `http://127.0.0.1:8000/trace/<batch_code>/` giúp bất kỳ ai cũng có thể quét và kiểm tra thông tin canh tác.
- **Cổng thanh toán số VietQR Napas 247**: Tích hợp chuẩn VietQR động với mã ngân hàng MBBank, tự động sinh mã QR chứa số tiền chính xác và nội dung chuyển khoản là mã đơn hàng (`ORDxxxxxxxx`). Khách hàng thanh toán tức thì qua mọi app ngân hàng di động mà không cần nhập thủ công.

### Kết luận Chương 1
Chương 1 đã hệ thống hóa đầy đủ cơ sở lý luận, phân tích các giải pháp công nghệ và phương pháp luận AI áp dụng cho bài toán thương mại điện tử nông sản. Đây là nền tảng vững chắc để nhóm tiến hành phân tích yêu cầu nghiệp vụ và thiết kế kiến trúc hệ thống chi tiết trong Chương 2.

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
| | <br><br>**Nguyễn Văn A** |
