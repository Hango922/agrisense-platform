# Website Bán Nông Sản Tích Hợp AI (AgriSense Platform)

> **Dự án Bài tập lớn Hệ thống Thông tin / Công nghệ Phần mềm**  
> **Sinh viên thực hiện**: Nguyễn Hồng Hoàng  
> **Mã số sinh viên**: 20234070  
> **Lớp**: N09 — **Nhóm**: 2  
> **Thời gian thực hiện**: 14/10/2026 – 07/12/2026 (8 tuần)  
> **Repository GitHub**: [https://github.com/Hango922/agrisense-platform.git](https://github.com/Hango922/agrisense-platform.git)

---

## 🌾 Giới thiệu dự án

**AgriSense** là nền tảng thương mại điện tử chuyên biệt dành cho nông sản sạch, nông sản hữu cơ và đặc sản vùng miền Việt Nam. Hệ thống kết hợp kiến trúc web hướng dịch vụ hiện đại với trí tuệ nhân tạo (AI) và công nghệ thanh toán số nhằm cá nhân hóa trải nghiệm mua sắm, tự động hóa bán hàng và nâng cao tính minh bạch chuỗi cung ứng:
1. **Chatbot AI & Lên đơn hàng đàm thoại (Conversational Commerce)**: Tư vấn nông sản (Gemini 1.5 Flash / Groq LLM + Fallback regex) kết hợp tính năng **lên đơn hàng trực tiếp bằng ngôn ngữ tự nhiên** (1-shot hoặc multi-turn), tự động kiểm tra và giảm trừ tồn kho an toàn.
2. **Cổng thanh toán tự động VietQR Napas 247**: Tự động sinh mã VietQR động chứa số tiền chính xác và nội dung chuyển khoản là mã đơn hàng, hiển thị trực quan trên trang đơn hàng và ngay trong khung chat của Chatbot AI.
3. **Phân nhóm hành vi khách hàng tự động**: Tự động phân loại khách hàng theo mô hình RFM rules (`new`, `interested`, `loyal`, `at_risk`, `normal`).
4. **Gợi ý sản phẩm cá nhân hóa**: Đề xuất nông sản phù hợp dựa trên lịch sử tương tác và sở thích danh mục với cơ chế fallback sản phẩm thịnh hành.
5. **Truy xuất nguồn gốc bằng mã QR**: Sinh mã QR chuẩn xác cho từng lô hàng thu hoạch trỏ về trang thông tin công khai không cần đăng nhập.
6. **Dashboard quản trị kinh doanh & Biểu đồ tương tác Chart.js**: Cung cấp bức tranh toàn cảnh về KPI doanh thu, biểu đồ đường xu hướng 30 ngày, biểu đồ tròn cơ cấu nhóm khách hàng AI, biểu đồ cột Top nông sản bán chạy và **tính năng xuất file Excel báo cáo đơn hàng (.xlsx)** chuẩn chỉnh.

---

## 🚀 Các tính năng chính

### 1. Phân hệ Bán hàng & Thanh toán (E-Commerce Core & VietQR)
- **Quản lý tài khoản**: Đăng ký, đăng nhập, bảo mật mật khẩu Django, quản lý hồ sơ và sổ địa chỉ nhận hàng linh hoạt.
- **Duyệt & Tìm kiếm nông sản**: Tìm kiếm theo từ khóa tiếng Việt, lọc theo danh mục, mức giá và phân trang trực quan.
- **Chi tiết nông sản**: Xem hình ảnh, mô tả, xuất xứ nông trại, mùa vụ, hướng dẫn chế biến, cách bảo quản và đánh giá sao từ khách hàng.
- **Giỏ hàng & Đặt hàng COD / Chuyển khoản**: Thêm sản phẩm, cập nhật số lượng, kiểm tra tồn kho thời gian thực, tính phí giao hàng thông minh (30.000đ, miễn phí từ 500.000đ), trừ kho an toàn bằng `@transaction.atomic`.
- **Thanh toán nhanh VietQR (Napas 247)**: Tự động nhúng số tài khoản ngân hàng MBBank, tên chủ tài khoản `NGUYEN HONG HOANG`, số tiền chính xác từng đồng và nội dung chuyển khoản là mã đơn hàng (`ORDxxxxxxxx`). Khách hàng quét mã qua mọi ứng dụng ngân hàng di động mà không lo nhập nhầm.
- **Quản lý đơn hàng**: Theo dõi lịch sử đơn hàng, xem chi tiết tiến độ giao hàng và hỗ trợ hủy đơn hàng khi đang chờ xác nhận (tự động hoàn kho).

### 2. Phân hệ Trí tuệ Nhân tạo & Chatbot (AI & Conversational Ordering)
- **Ghi nhận hành vi (Behavior Tracking)**: Middleware và services tự động lưu nhật ký sự kiện `UserEvent` (`view`, `search`, `add_to_cart`, `purchase`, `review`, `chat`).
- **Phân nhóm khách hàng (Customer Segmentation)**:
  - `new`: Khách hàng mới đăng ký trong 7 ngày gần nhất, chưa có đơn hàng.
  - `interested`: Chưa mua hàng nhưng có từ 5 tương tác trở lên.
  - `loyal`: Có từ 3 đơn hàng thành công trong vòng 30 ngày qua.
  - `at_risk`: Khách hàng có nguy cơ rời bỏ (đơn hàng cuối cùng trên 30 ngày).
  - `normal`: Khách hàng mua sắm thông thường.
  - Command định kỳ: `python manage.py update_segments`.
- **Gợi ý sản phẩm (Recommendation Engine)**: Thuật toán lọc nội dung (Content-based filtering) tính điểm trọng số theo danh mục ưa thích, loại bỏ sản phẩm đã mua và tự động chuyển sang sản phẩm bán chạy/bán chạy nhất khi thiếu dữ liệu.
- **Chatbot AI & Lên đơn hàng đàm thoại**:
  - Hỗ trợ gọi mô hình Gemini 1.5 Flash hoặc Groq Cloud API.
  - Bộ luật Fallback Regex thông minh nhận diện từ khóa tiếng Việt (giá cả, xuất xứ, bảo quản, tra cứu đơn hàng).
  - **Trợ lý lên đơn hàng tự động**: Khách nhắn câu lệnh tự nhiên (ví dụ: *"Tôi muốn mua 2kg cà chua bi, giao về số 15 Hai Bà Trưng Hà Nội, sđt 0987654321"*), Chatbot tự động phân tích sản phẩm, trừ tồn kho, tạo đơn hàng và gửi ảnh mã VietQR thanh toán tức thời ngay trong khung chat.

### 3. Phân hệ Truy xuất nguồn gốc (QR Traceability)
- Tự động sinh mã QR định dạng PNG chuẩn ISO cho từng lô hàng nông sản (`ProductBatch`).
- Mã QR trỏ trực tiếp đến URL tra cứu công khai: `http://127.0.0.1:8000/trace/<batch_code>/`.
- Cung cấp đầy đủ thông tin: Tên sản phẩm, nông trại / vùng trồng, ngày thu hoạch, ngày đóng gói, chứng nhận an toàn (VietGAP, GlobalGAP, Organic), sản lượng và nhật ký kiểm định.

### 4. Phân hệ Quản trị Dashboard (Admin Dashboard & Analytics)
- URL: `http://127.0.0.1:8000/dashboard/`
- Phân quyền nghiêm ngặt bằng `@method_decorator(staff_member_required, name='dispatch')`.
- **Biểu đồ trực quan tương tác Chart.js**:
  - Biểu đồ đường (Line Chart): Xu hướng biến động doanh số theo từng ngày trong 30 ngày qua.
  - Biểu đồ tròn (Doughnut Chart): Tỉ lệ phân bổ các nhóm khách hàng AI.
  - Biểu đồ cột (Bar Chart): Top 5 nông sản bán chạy nhất.
- **Xuất báo cáo bán hàng ra Excel (.xlsx)**:
  - Tải file Excel danh sách đơn hàng được định dạng chuyên nghiệp với tiêu đề màu thương hiệu AgriSense, viền ô sắc nét, căn lề và định dạng số tiền VND tự động thông qua thư viện `openpyxl`.

---

## 🛠️ Yêu cầu môi trường & Công nghệ

| Thành phần | Phiên bản / Công nghệ | Ghi chú |
| :--- | :--- | :--- |
| **Hệ điều hành** | Windows 11 / Linux / macOS | Khuyến nghị Windows 11 theo môi trường phát triển |
| **Ngôn ngữ** | Python 3.14.3 | Đã kiểm thử và chạy ổn định |
| **Web Framework** | Django 6.1.2 | Kiến trúc MVT, ORM, CSRF protection |
| **Cơ sở dữ liệu** | MySQL Server 26.7.0 | Port 3306, mã hóa `utf8mb4_0900_ai_ci` |
| **Database Driver**| PyMySQL 1.2.3 | Tích hợp qua `pymysql.install_as_MySQLdb()` |
| **Frontend UI** | Bootstrap 5.3.3, Bootstrap Icons | CDN responsive cho Desktop và Mobile |
| **Thư viện biểu đồ** | Chart.js 4.4 | Biểu đồ đường, tròn, cột tương tác |
| **Báo cáo Excel** | openpyxl 3.1.5 | Xuất file báo cáo đơn hàng định dạng `.xlsx` |
| **Xử lý dữ liệu** | Pandas, Scikit-learn, NumPy | Hỗ trợ phân tích hành vi và phân cụm |
| **Mã QR & Hình ảnh**| qrcode 7.4.2, Pillow 11.0.0 | Sinh mã QR PNG tự động |
| **Cổng thanh toán** | VietQR Napas 247 | Sinh mã QR ngân hàng thanh toán tự động |
| **Chatbot AI** | Google Gemini API / Groq API | Tích hợp fallback regex thông minh |

---

## ⚙️ Hướng dẫn cài đặt & Chạy dự án

### Bước 1: Clone kho mã nguồn từ GitHub
```bash
git clone https://github.com/Hango922/agrisense-platform.git
cd agrisense-platform
```

### Bước 2: Kích hoạt môi trường ảo Python
```bash
# Trên Windows PowerShell:
python -m venv .venv
.venv\Scripts\activate
```

### Bước 3: Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### Bước 4: Tạo cơ sở dữ liệu MySQL
Mở MySQL Command Line Client hoặc MySQL Workbench và thực hiện:
```sql
CREATE DATABASE nongsan_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
```

### Bước 5: Cấu hình biến môi trường `.env`
> [!IMPORTANT]
> **Lưu ý bảo mật**: File `.env` chứa mật khẩu cơ sở dữ liệu và API Key nhạy cảm nên **đã được cấu hình trong `.gitignore` để không bao giờ bị đẩy lên GitHub**. Trên máy tính cá nhân của bạn, hãy tạo file `.env` từ `.env.example`:

Sao chép `.env.example` thành `.env` và cập nhật thông tin cá nhân của bạn:
```env
DEBUG=True
SECRET_KEY=django-insecure-agrisense-platform-secret-key-2026
DB_NAME=nongsan_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306

# API Key cho Chatbot AI (Tùy chọn: nếu không có, hệ thống tự kích hoạt Rule-based Fallback)
AI_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Cấu hình thanh toán VietQR Napas 247
VIETQR_BANK_ID=MB
VIETQR_ACCOUNT_NO=0922334455
VIETQR_ACCOUNT_NAME=NGUYEN HONG HOANG
VIETQR_BANK_NAME=Ngân hàng Quân Đội (MBBank)
```

### Bước 6: Khởi tạo bảng dữ liệu (Migration)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Bước 7: Khởi tạo dữ liệu mẫu (Seed Data)
```bash
python manage.py seed_data
```
Lệnh sẽ tự động khởi tạo 6 danh mục, 7 nhà cung cấp, 32 sản phẩm, 24 người dùng mẫu, 52 đơn hàng, 11 lô hàng kèm mã QR và 2 tài khoản demo.

### Bước 8: Cập nhật phân nhóm khách hàng AI
```bash
python manage.py update_segments
```

### Bước 9: Khởi động máy chủ phát triển
```bash
python manage.py runserver
```
Truy cập ứng dụng tại: **http://127.0.0.1:8000/**

---

## 🔑 Tài khoản demo hệ thống

| Vai trò | Tên đăng nhập | Mật khẩu | Quyền hạn |
| :--- | :--- | :--- | :--- |
| **Quản trị viên (Admin)** | `demo_admin` | `Admin@123` | Toàn quyền Dashboard & Django Admin |
| **Khách hàng mẫu (Customer)** | `demo_customer` | `Demo@123` | Mua hàng, giỏ hàng, xem đơn, chat AI |

---

## 🌐 Danh sách URL chính

- **Trang chủ nông sản**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Danh sách sản phẩm**: [http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/)
- **Giỏ hàng**: [http://127.0.0.1:8000/cart/](http://127.0.0.1:8000/cart/)
- **Lịch sử đơn hàng**: [http://127.0.0.1:8000/orders/](http://127.0.0.1:8000/orders/)
- **Truy xuất nguồn gốc mẫu**: [http://127.0.0.1:8000/trace/BATCH2026001/](http://127.0.0.1:8000/trace/BATCH2026001/)
- **Dashboard Quản trị**: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
- **Xuất Báo Cáo Excel Đơn Hàng**: [http://127.0.0.1:8000/dashboard/orders/export-excel/](http://127.0.0.1:8000/dashboard/orders/export-excel/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Kiểm thử tự động (Unit Tests)

Chạy toàn bộ 43 bài kiểm thử tự động của hệ thống bao phủ tất cả các phân hệ:
```bash
python manage.py test
```
**Kết quả kiểm thử:**
```text
Creating test database for alias 'default'...
...........................................
----------------------------------------------------------------------
Ran 43 tests in 44.275s

OK (100% PASS - 0 errors, 0 failures)
```

---

## 📁 Cấu trúc thư mục dự án

```text
agrisense-platform/
├── manage.py
├── requirements.txt            # Thư viện phụ thuộc (Django, openpyxl, pandas,...)
├── .env.example                # File mẫu cấu hình biến môi trường (an toàn)
├── .gitignore                  # Bỏ qua .env, virtualenv, logs, pycache
├── README.md                   # Tài liệu hướng dẫn toàn diện dự án
├── NHAT_KY_DU_AN.md            # Nhật ký tiến độ thực hiện theo tuần
├── nongsan_project/            # Cấu hình dự án Django
│   ├── __init__.py             # Cấu hình pymysql.install_as_MySQLdb()
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                       # 8 phân hệ nghiệp vụ MVT
│   ├── accounts/               # Tài khoản, phân nhóm, địa chỉ giao hàng
│   ├── products/               # Danh mục, nhà cung cấp, sản phẩm, đánh giá
│   ├── cart_orders/            # Giỏ hàng, đặt hàng COD, VietQR Napas 247
│   ├── behavior/               # Theo dõi hành vi, phân loại khách hàng RFM
│   ├── recommendation/         # Động cơ gợi ý sản phẩm cá nhân hóa
│   ├── chatbot/                # Chatbot AI & Trợ lý lên đơn hàng đàm thoại
│   ├── traceability/           # Lô hàng nông sản & sinh mã QR truy xuất
│   └── dashboard/              # Trang điều hành quản trị viên & Chart.js
├── static/                     # CSS, JS (chatbot widget, main.js), hình ảnh
├── templates/                  # Giao diện Bootstrap 5.3 theo từng phân hệ
└── tests/                      # Bộ kiểm thử tích hợp hệ thống (Phase 4, Phase 5)
```

---
*© 2026 Nguyễn Hồng Hoàng — MSSV: 20234070 — AgriSense Platform.*
