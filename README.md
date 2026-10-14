# Website Bán Nông Sản Tích Hợp AI (AgriSense Platform)

> **Dự án Bài tập lớn Hệ thống Thông tin / Công nghệ Phần mềm**  
> **Sinh viên thực hiện**: Nguyễn Hồng Hoàng  
> **Mã số sinh viên**: 20234070  
> **Lớp**: N09 — **Nhóm**: 2  
> **Thời gian thực hiện**: 14/10/2026 – 07/12/2026 (8 tuần)

---

## 🌾 Giới thiệu dự án

**AgriSense** là nền tảng thương mại điện tử chuyên biệt dành cho nông sản sạch, nông sản hữu cơ và đặc sản vùng miền Việt Nam. Hệ thống ứng dụng trí tuệ nhân tạo (AI) toàn diện nhằm cá nhân hóa trải nghiệm mua sắm, tối ưu hóa chăm sóc khách hàng và nâng cao tính minh bạch chuỗi cung ứng thông qua:
1. **Phân nhóm hành vi khách hàng tự động**: Tự động phân loại khách hàng theo mô hình RFM rules (`new`, `interested`, `loyal`, `at_risk`, `normal`).
2. **Gợi ý sản phẩm cá nhân hóa**: Đề xuất nông sản phù hợp dựa trên lịch sử tương tác và sở thích danh mục với cơ chế fallback sản phẩm thịnh hành.
3. **Chatbot AI tư vấn thông minh**: Hỗ trợ giải đáp thắc mắc về giá bán, xuất xứ nông sản, cách bảo quản, trạng thái đơn hàng kết hợp giữa mô hình ngôn ngữ lớn (Gemini/Groq) và bộ luật phản hồi Fallback tự động.
4. **Truy xuất nguồn gốc bằng mã QR**: Sinh mã QR chuẩn xác cho từng lô hàng thu hoạch trỏ về trang thông tin công khai không cần đăng nhập.
5. **Dashboard quản trị kinh doanh**: Cung cấp bức tranh toàn cảnh về KPI doanh thu, đơn hàng, khách hàng, biến động hành vi và nguồn gốc lô hàng.

---

## 🚀 Các tính năng chính

### 1. Phân hệ Bán hàng (E-Commerce Core)
- **Quản lý tài khoản**: Đăng ký, đăng nhập, bảo mật mật khẩu Django, quản lý hồ sơ và sổ địa chỉ nhận hàng linh hoạt.
- **Duyệt & Tìm kiếm nông sản**: Tìm kiếm theo từ khóa, lọc theo danh mục, mức giá và phân trang trực quan.
- **Chi tiết nông sản**: Xem hình ảnh, mô tả, xuất xứ nông trại, mùa vụ, hướng dẫn chế biến, cách bảo quản và đánh giá sao từ khách hàng.
- **Giỏ hàng & Đặt hàng COD**: Thêm sản phẩm, cập nhật số lượng, kiểm tra tồn kho thời gian thực, tính phí giao hàng thông minh (30.000đ, miễn phí từ 500.000đ), trừ kho an toàn bằng `@transaction.atomic`.
- **Quản lý đơn hàng**: Theo dõi lịch sử đơn hàng, xem chi tiết tiến độ giao hàng và hỗ trợ hủy đơn hàng khi đang chờ xác nhận (tự động hoàn kho).

### 2. Phân hệ Trí tuệ Nhân tạo (AI Features)
- **Ghi nhận hành vi (Behavior Tracking)**: Middleware và services tự động lưu nhật ký sự kiện `UserEvent` (`view`, `search`, `add_to_cart`, `purchase`, `review`, `chat`).
- **Phân nhóm khách hàng (Customer Segmentation)**:
  - `new`: Khách hàng mới đăng ký trong 7 ngày gần nhất, chưa có đơn hàng.
  - `interested`: Chưa mua hàng nhưng có từ 5 tương tác trở lên.
  - `loyal`: Có từ 3 đơn hàng thành công trong vòng 30 ngày qua.
  - `at_risk`: Khách hàng có nguy cơ rời bỏ (đơn hàng cuối cùng trên 30 ngày).
  - `normal`: Khách hàng mua sắm thông thường.
  - Command định kỳ: `python manage.py update_segments`.
- **Gợi ý sản phẩm (Recommendation Engine)**: Thuật toán lọc nội dung (Content-based filtering) tính điểm trọng số theo danh mục ưa thích, loại bỏ sản phẩm đã mua và tự động chuyển sang sản phẩm bán chạy/bán chạy nhất khi thiếu dữ liệu.
- **Chatbot AI & Fallback Rules**:
  - Tích hợp Gemini 1.5 Flash / Groq LLM API.
  - Bộ từ khóa Fallback regex nhận diện chuẩn xác cả tiếng Việt có dấu và không dấu: giá cả, xuất xứ, bảo quản, tra cứu đơn hàng, fallback mặc định.
  - Giao diện Floating Widget tương tác trực tiếp ở góc dưới website.

### 3. Phân hệ Truy xuất nguồn gốc (QR Traceability)
- Tự động sinh mã QR định dạng PNG chuẩn ISO cho từng lô hàng nông sản (`ProductBatch`).
- Mã QR trỏ trực tiếp đến URL tra cứu công khai: `http://127.0.0.1:8000/trace/<batch_code>/`.
- Cung cấp đầy đủ thông tin: Tên sản phẩm, nông trại / vùng trồng, ngày thu hoạch, ngày đóng gói, chứng nhận an toàn (VietGAP, GlobalGAP, Organic), sản lượng và nhật ký kiểm định.

### 4. Phân hệ Quản trị Dashboard (Admin Dashboard)
- URL: `http://127.0.0.1:8000/dashboard/`
- Phân quyền nghiêm ngặt bằng `@method_decorator(staff_member_required, name='dispatch')`.
- Các màn hình báo cáo chuyên biệt:
  - **Tổng quan**: KPI Doanh thu 30 ngày, tổng đơn hàng, khách hàng, số lượng sản phẩm, Top 10 sản phẩm bán chạy và biểu đồ cơ cấu phân nhóm AI.
  - **Sản phẩm**: Quản lý danh mục, tồn kho và trạng thái bày bán.
  - **Đơn hàng**: Danh sách đơn hàng, bộ lọc trạng thái và doanh thu từng đơn.
  - **Khách hàng**: Danh sách khách hàng và nhãn phân nhóm hành vi.
  - **Hành vi**: Thống kê số lượng từng loại sự kiện tương tác.
  - **Lô hàng**: Quản lý thông tin lô hàng và mã QR tải về / in ấn.

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
| **Xử lý dữ liệu** | Pandas, Scikit-learn, NumPy | Hỗ trợ phân tích hành vi và phân cụm |
| **Mã QR & Hình ảnh**| qrcode 7.4.2, Pillow 11.0.0 | Sinh mã QR PNG tự động |
| **Chatbot AI** | Google Gemini API / Groq API | Tích hợp fallback regex thông minh |

---

## ⚙️ Hướng dẫn cài đặt & Chạy dự án

### Bước 1: Mở thư mục dự án
```bash
cd c:\Users\Admin\Desktop\CNPM\agrisense-platform
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
Sao chép `.env.example` thành `.env` và cập nhật thông tin:
```env
DEBUG=True
SECRET_KEY=django-insecure-agrisense-platform-secret-key-2026
DB_NAME=nongsan_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
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
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Kiểm thử tự động (Unit Tests)

Chạy toàn bộ 32 bài kiểm thử tự động của hệ thống:
```bash
python manage.py test
```
**Kết quả kiểm thử:**
```text
Ran 32 tests in 25.472s

OK (100% PASS - 0 errors, 0 failures)
```

---

## 📁 Cấu trúc thư mục dự án

```text
agrisense-platform/
├── manage.py
├── requirements.txt
├── .env / .env.example / .gitignore
├── README.md / NHAT_KY_DU_AN.md
├── nongsan_project/            # Cấu hình dự án Django
│   ├── __init__.py             # Cấu hình pymysql.install_as_MySQLdb()
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                       # 8 phân hệ nghiệp vụ MVT
│   ├── accounts/               # Tài khoản, phân nhóm, địa chỉ giao hàng
│   ├── products/               # Danh mục, nhà cung cấp, sản phẩm, đánh giá
│   ├── cart_orders/            # Giỏ hàng, đặt hàng COD, chi tiết đơn hàng
│   ├── behavior/               # Theo dõi hành vi, phân loại khách hàng RFM
│   ├── recommendation/         # Động cơ gợi ý sản phẩm cá nhân hóa
│   ├── chatbot/                # Chatbot AI (Gemini/Groq + Rule-based fallback)
│   ├── traceability/           # Lô hàng nông sản & sinh mã QR truy xuất
│   └── dashboard/              # Trang điều hành quản trị viên
├── static/                     # CSS, JS (chatbot widget), hình ảnh
├── templates/                  # Giao diện Bootstrap 5.3 theo từng phân hệ
└── tests/                      # Bộ kiểm thử tích hợp hệ thống
```

---
*© 2026 Nguyễn Hồng Hoàng — AgriSense Platform.*
