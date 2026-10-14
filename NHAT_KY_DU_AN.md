# NHẬT KÝ DỰ ÁN (PROJECT LOG)
## Đề tài: Xây dựng website bán nông sản tích hợp AI nhận diện hành vi khách hàng, Chatbot tư vấn và QR truy xuất nguồn gốc (AgriSense)
- **Sinh viên thực hiện**: Nguyễn Hồng Hoàng
- **Mã sinh viên**: 20234070 — **Lớp**: N09 — **Nhóm**: 2
- **Thời gian thực hiện**: 14/10/2026 – 07/12/2026 (8 tuần)

---

### TUẦN 1 (14/10/2026 – 20/10/2026) | GIAI ĐOẠN 1: KHỞI ĐỘNG & THIẾT LẬP MÔI TRƯỜNG
- **Mục tiêu**:
  - Chốt phạm vi dự án, kế hoạch WBS và tiêu chí SMART.
  - Thiết lập môi trường kỹ thuật: Python 3.14.3, MySQL Server 26.7.0, Django 6.1.2, PyMySQL 1.2.3, Scikit-learn, Pandas.
  - Khởi tạo cấu trúc dự án Django MVT với 8 ứng dụng phân hệ theo thiết kế hệ thống.
  - Cấu hình file biến môi trường `.env`, `.env.example`, `requirements.txt`.
  - Kết nối thành công Django ORM với cơ sở dữ liệu `nongsan_db` trên MySQL 26.7.0 thông qua PyMySQL adapter.
- **Kết quả đạt được**:
  - [x] Tạo cơ sở dữ liệu MySQL `nongsan_db` (bảng mã `utf8mb4_unicode_ci` / `utf8mb4_0900_ai_ci`).
  - [x] Cài đặt đầy đủ các gói thư viện vào môi trường Python 3.14: Django, PyMySQL, python-dotenv, qrcode, Pillow, pandas, scikit-learn, requests.
  - [x] Thiết lập `pymysql.install_as_MySQLdb()` trong `nongsan_project/__init__.py` để khắc phục triệt để vấn đề tương thích mysqlclient trên Python 3.14.
  - [x] Khởi tạo cấu trúc 8 apps nghiệp vụ trong `apps/`: accounts, products, cart_orders, behavior, recommendation, chatbot, traceability, dashboard.
  - [x] Khởi tạo `apps/accounts/models.py` với Custom User Model `User(AbstractUser)` hỗ trợ 3 nhóm vai trò (customer, staff, admin) và cấu hình `AUTH_USER_MODEL = 'accounts.User'`.
  - [x] Chạy lệnh `python manage.py check` thành công: `System check identified no issues (0 silenced)`.
- **Đánh giá tiến độ Tuần 1**: Hoàn thành 100% mục tiêu Giai đoạn 1 đúng hạn.

---

### TUẦN 2 (21/10/2026 – 28/10/2026) | GIAI ĐOẠN 2: THIẾT KẾ CƠ SỞ DỮ LIỆU & MIGRATION
- **Mục tiêu**:
  - Xây dựng 12 bảng cơ sở dữ liệu cốt lõi chia theo 7 nhóm nghiệp vụ (Accounts, Products, Cart_orders, Behavior, Chatbot, Traceability).
  - Khởi tạo Custom User Model `User(AbstractUser)` tích hợp thuộc tính phân nhóm khách hàng (`segment`), sổ địa chỉ (`UserAddress`).
  - Thiết lập mối quan hệ giữa các bảng: Category, Supplier, Product, ProductReview, Cart, CartItem, Order, OrderItem, UserEvent, UserSegment, RecommendationLog, ChatSession, ChatMessage, ProductBatch, TraceabilityRecord.
  - Đăng ký toàn bộ Model vào Django Admin với bộ lọc, tìm kiếm và inline trực quan.
  - Thực thi `makemigrations` và `migrate` tạo thành công 26 bảng dữ liệu trong MySQL `nongsan_db`.
  - Khởi tạo tài khoản quản trị tối cao `demo_admin` / `Admin@123`.
- **Kết quả đạt được**:
  - [x] Tạo đầy đủ 12 model nghiệp vụ trong 6 app theo chuẩn đặc tả.
  - [x] Đăng ký giao diện Django Admin cho tất cả các app.
  - [x] Chạy migration thành công 100% trên MySQL Server 26.7.0.
  - [x] Kiểm tra `SHOW TABLES;` trong `nongsan_db`: Đã tạo 26 bảng dữ liệu.
  - [x] Kiểm tra đăng nhập tài khoản quản trị `demo_admin` vào `/admin/`: Status 200, hiển thị đầy đủ các phân hệ.
- **Đánh giá tiến độ Tuần 2**: Hoàn thành 100% mục tiêu Giai đoạn 2 đúng hạn.

---

### TUẦN 3 (29/10/2026 – 04/11/2026) | PHÂN HỆ TÀI KHOẢN & QUẢN LÝ SẢN PHẨM
- **Mục tiêu**:
  - Xây dựng chức năng xác thực người dùng: Đăng ký tài khoản mới, mã hóa mật khẩu, đăng nhập, đăng xuất.
  - Quản lý sổ địa chỉ giao hàng (`UserAddress`) với chức năng thiết lập địa chỉ mặc định.
  - Xây dựng các view duyệt danh mục (`Category`), tìm kiếm nông sản và lọc sản phẩm theo mức giá, danh mục.
  - Xây dựng trang chi tiết nông sản với hình ảnh, xuất xứ, mùa vụ, hướng dẫn bảo quản và đánh giá sao từ khách hàng.
- **Kết quả đạt được**:
  - [x] Triển khai `apps/accounts/views.py` (RegisterView, LoginView, ProfileView, LogoutView).
  - [x] Triển khai `apps/products/views.py` (ProductListView, ProductDetailView, ProductSearchView).
  - [x] Thiết lập `apps/products/models.py` với `ProductReview` cho phép khách hàng gửi phản hồi và chấm điểm chất lượng.
  - [x] Kiểm thử luồng tài khoản và duyệt sản phẩm hoạt động trơn tru.
- **Đánh giá tiến độ Tuần 3**: Hoàn thành 100% mục tiêu đúng hạn.

---

### TUẦN 4 (05/11/2026 – 11/11/2026) | PHÂN HỆ GIỎ HÀNG & ĐẶT HÀNG THANH TOÁN COD
- **Mục tiêu**:
  - Xây dựng giỏ hàng lưu trữ Database gắn với từng tài khoản (`Cart`, `CartItem`).
  - Hỗ trợ thêm vào giỏ, cập nhật số lượng, xóa sản phẩm khỏi giỏ với xác thực tồn kho tức thời.
  - Xây dựng dịch vụ đặt hàng COD (`apps.cart_orders.services.create_order_from_cart`):
    + Kiểm tra tồn kho trước khi đặt.
    + Tính toán phí giao hàng thông minh: 30.000đ cho đơn dưới 500.000đ, miễn phí giao hàng cho đơn từ 500.000đ trở lên.
    + Giảm trừ số lượng tồn kho tự động trong giao dịch an toàn `@transaction.atomic`.
  - Hỗ trợ xem lịch sử đơn hàng và chi tiết đơn hàng theo mã đơn `ORDxxxxxxxx`.
  - Hỗ trợ hủy đơn hàng khi ở trạng thái 'Chờ xác nhận' (`cancel_order`) và tự động hoàn trả tồn kho.
- **Kết quả đạt được**:
  - [x] Triển khai `apps/cart_orders/services.py` với các hàm nghiệp vụ chuẩn hóa.
  - [x] Triển khai `apps/cart_orders/views.py` (CartView, CheckoutView, OrderHistoryView, OrderDetailView, CancelOrderView).
  - [x] Xây dựng context processor giỏ hàng hiển thị số lượng mặt hàng trên thanh điều hướng.
  - [x] Kiểm thử tự động: Đặt hàng thành công, trừ tồn kho chính xác, hủy đơn hoàn tồn kho an toàn.
- **Đánh giá tiến độ Tuần 4**: Hoàn thành 100% mục tiêu đúng hạn.

---

### TUẦN 5 (12/11/2026 – 18/11/2026) | GIAO DIỆN BOOTSTRAP 5.3 & MIDDLEWARE THEO DÕI HÀNH VI
- **Mục tiêu**:
  - Thiết kế hệ thống giao diện HTML5 Responsive hiện đại với Bootstrap 5.3.3 và Bootstrap Icons.
  - Xây dựng bố cục dùng chung `base.html`, trang chủ `home.html`, trang lỗi `404.html` và `500.html`.
  - Triển khai `BehaviorTrackingMiddleware` tự động ghi nhận các tương tác tìm kiếm (`search`) và xem sản phẩm (`view`).
  - Tối ưu hóa trải nghiệm người dùng trên cả giao diện máy tính và thiết bị di động.
- **Kết quả đạt được**:
  - [x] Hoàn thiện bộ template Bootstrap 5.3 cho tất cả các phân hệ.
  - [x] Tích hợp thẻ meta CSRF Token và xử lý AJAX an toàn.
  - [x] Triển khai `apps/behavior/middleware.py` hoạt động ổn định trong pipeline xử lý request của Django.
  - [x] Kiểm tra hiển thị responsive đạt tiêu chuẩn UI/UX.
- **Đánh giá tiến độ Tuần 5**: Hoàn thành 100% mục tiêu đúng hạn.

---

### TUẦN 6 (19/11/2026 – 25/11/2026) | PHÂN NHÓM KHÁCH HÀNG AI & ĐỘNG CƠ GỢI Ý NÔNG SẢN
- **Mục tiêu**:
  - Xây dựng thuật toán phân loại khách hàng thông minh (`apps/behavior/segmentation.py`) theo 5 nhóm:
    + `new`: Khách hàng mới đăng ký trong vòng 7 ngày, chưa có đơn hàng.
    + `interested`: Chưa mua nhưng có từ 5 lượt tương tác (xem, tìm kiếm, giỏ hàng).
    + `loyal`: Có từ 3 đơn hàng thành công trong vòng 30 ngày qua.
    + `at_risk`: Khách hàng có nguy cơ rời bỏ (đơn hàng cuối cùng trên 30 ngày trước).
    + `normal`: Khách hàng mua sắm thông thường.
  - Xây dựng lệnh quản trị cập nhật định kỳ: `python manage.py update_segments`.
  - Xây dựng động cơ gợi ý sản phẩm cá nhân hóa (`apps/recommendation/engine.py`):
    + Tính vector điểm số sở thích danh mục dựa trên trọng số tương tác (`view: 1.0`, `search: 2.0`, `add_to_cart: 3.0`, `purchase: 5.0`, `review: 4.0`).
    + Loại bỏ sản phẩm khách hàng đã từng mua.
    + Tự động fallback sang danh sách sản phẩm bán chạy/thịnh hành khi khách hàng chưa đủ dữ liệu.
- **Kết quả đạt được**:
  - [x] Triển khai thuật toán phân loại hành vi và kiểm thử logic phân nhóm đạt độ chính xác 100%.
  - [x] Triển khai động cơ gợi ý cá nhân hóa và tích hợp trực tiếp lên phần "Gợi ý dành riêng cho bạn" trên trang chủ.
  - [x] Chạy lệnh `update_segments` thành công, lưu vết lịch sử vào bảng `UserSegment`.
- **Đánh giá tiến độ Tuần 6**: Hoàn thành 100% mục tiêu đúng hạn.

---

### TUẦN 7 (26/11/2026 – 02/12/2026) | CHATBOT AI, QR TRUY XUẤT NGUỒN GỐC & DASHBOARD ADMIN
- **Mục tiêu**:
  - Tích hợp Chatbot AI tư vấn nông sản (`apps/chatbot`):
    + Xây dựng System Prompt chuyên gia tư vấn nông sản sạch.
    + Tích hợp Gemini 1.5 Flash và Groq API có cơ chế timeout an toàn.
    + Xây dựng bộ luật Fallback Rule-based thông minh bằng Regex nhận diện từ khóa (giá, nguồn gốc, bảo quản, đơn hàng, mặc định) cả có dấu và không dấu.
    + Xây dựng giao diện Chatbot Widget nổi tương tác thời gian thực.
  - Tích hợp module truy xuất nguồn gốc bằng mã QR (`apps/traceability`):
    + Hàm sinh mã QR chuẩn PNG (`qr_generator.py`) trỏ về trang công khai `/trace/<batch_code>/`.
    + Hiển thị đầy đủ nguồn gốc lô hàng: nông trại, ngày thu hoạch, chứng nhận an toàn, sản lượng.
  - Xây dựng phân hệ Dashboard Admin chuyên biệt (`apps/dashboard`):
    + Bảo vệ truy cập nghiêm ngặt với `@method_decorator(staff_member_required, name='dispatch')`.
    + 6 màn hình quản trị: Tổng quan KPI 30 ngày, Sản phẩm, Đơn hàng, Khách hàng, Nhật ký hành vi, Lô hàng QR.
- **Kết quả đạt được**:
  - [x] Triển khai toàn bộ backend và UI Chatbot AI, kiểm thử 100% các tình huống fallback thành công.
  - [x] Triển khai sinh mã QR và xem trang truy xuất nguồn gốc công khai không cần đăng nhập.
  - [x] Hoàn thiện 6 màn hình Dashboard Admin với số liệu thống kê doanh thu, đơn hàng và biểu đồ phân nhóm AI.
  - [x] Kiểm thử tự động `tests/test_phase4.py` và `tests/test_phase5.py` đạt 100% PASS.
- **Đánh giá tiến độ Tuần 7**: Hoàn thành 100% mục tiêu đúng hạn.

---

### TUẦN 8 (03/12/2026 – 07/12/2026) | GIAI ĐOẠN CUỐI: SEED DATA, KIỂM THỬ HỆ THỐNG & BÀN GIAO
- **Mục tiêu**:
  - Xây dựng lệnh `python manage.py seed_data` tự động tạo kho dữ liệu thực tế:
    + 6 danh mục, 7 nhà cung cấp, 32 sản phẩm nông sản phong phú.
    + 24 người dùng mẫu đại diện đầy đủ các nhóm hành vi AI.
    + 165 sự kiện tương tác hành vi người dùng.
    + 52 đơn hàng với các trạng thái phân bố thực tế.
    + 11 lô hàng kèm mã QR truy xuất lưu trữ hợp lệ.
    + 2 tài khoản demo: `demo_admin` / `Admin@123` và `demo_customer` / `Demo@123`.
  - Xây dựng hệ thống Unit Tests toàn diện với `django.test.TestCase` cho tất cả các phân hệ:
    + `apps/cart_orders/tests/test_orders.py` (Bao gồm kiểm thử logic đặt hàng, tồn kho, tính phí ship và sinh mã VietQR Napas 247)
    + `apps/chatbot/tests/test_fallback.py` & `apps/chatbot/tests/test_ordering.py` (Kiểm thử fallback AI và đặt hàng đàm thoại trực tiếp)
    + `apps/accounts/tests/test_accounts.py`
    + `apps/behavior/tests/test_behavior.py`
    + `apps/traceability/tests/test_traceability.py`
    + `apps/products/tests/test_products.py`
    + `tests/test_phase4.py` & `tests/test_phase5.py` (Kiểm thử phân quyền, dữ liệu Chart.js và xuất file Excel .xlsx)
  - Thực hiện bộ kiểm thử toàn diện: `python manage.py test`.
  - Nâng cấp các tính năng cao cấp: Cổng thanh toán VietQR Napas 247, Chatbot AI lên đơn hàng tự động, Dashboard biểu đồ Chart.js và Xuất báo cáo Excel.
  - Hoàn thiện tài liệu kỹ thuật `README.md`, kiểm tra `.gitignore` bảo vệ file `.env` và đóng gói bàn giao.
- **Kết quả đạt được**:
  - [x] Tạo file `apps/products/management/commands/seed_data.py` và chạy thành công trên cơ sở dữ liệu `nongsan_db`.
  - [x] Chạy lệnh `update_segments` phân bổ đủ 5 nhóm: `new`, `interested`, `loyal`, `at_risk`, `normal`.
  - [x] Triển khai thành công Cổng thanh toán VietQR động trên trang đơn hàng và trong khung chat AI.
  - [x] Tích hợp 3 biểu đồ tương tác Chart.js (đường, tròn, cột) và chức năng xuất file Excel (`.xlsx`) vào Dashboard.
  - [x] Chạy `python manage.py test`: **43/43 tests đạt 100% PASS** (0 errors, 0 failures).
  - [x] Hoàn thiện tài liệu `README.md` và `NHAT_KY_DU_AN.md`.
  - [x] Đảm bảo file bí mật `.env` nằm trong `.gitignore` không bao giờ bị đẩy lên GitHub, lưu trữ an toàn trên máy cục bộ.
- **Đánh giá tổng kết**: Đồ án hoàn thành xuất sắc 100% toàn bộ mục tiêu đề ra và tích hợp các tính năng nâng cấp vượt trội, sẵn sàng bảo vệ đồ án đạt kết quả cao nhất.

