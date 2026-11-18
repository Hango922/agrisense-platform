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
- **Thanh toán nhanh VietQR (Napas 247)**: Sinh QR theo tài khoản nhận tiền cấu hình trong `VIETQR_*`, số tiền và mã đơn hàng (`ORDxxxxxxxx`). Nhân viên đối soát và xác nhận thủ công; hệ thống chưa tự xác minh giao dịch ngân hàng.
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
- Mã QR trỏ đến `<QR_BASE_URL>/trace/<batch_code>/`; cấu hình URL trước khi tạo lô hàng.
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
| **Hệ điều hành** | Windows | Bộ dependency đã kiểm chứng trên Windows; Linux/macOS cần kiểm tra riêng |
| **Ngôn ngữ** | Python 3.14.3 | Đã kiểm thử và chạy ổn định |
| **Web Framework** | Django 6.1.2 | Kiến trúc MVT, ORM, CSRF protection |
| **Cơ sở dữ liệu** | MySQL Server 26.7.0 | Port 3306, mã hóa `utf8mb4_0900_ai_ci` |
| **Database Driver**| PyMySQL 1.2.3 | Tích hợp qua `pymysql.install_as_MySQLdb()` |
| **Frontend UI** | Bootstrap 5.3.3, Bootstrap Icons | CDN responsive cho Desktop và Mobile |
| **Thư viện biểu đồ** | Chart.js 4.4 | Biểu đồ đường, tròn, cột tương tác |
| **Báo cáo Excel** | openpyxl 3.1.5 | Xuất file báo cáo đơn hàng định dạng `.xlsx` |
| **Xử lý dữ liệu** | Pandas, Scikit-learn, NumPy | Hỗ trợ phân tích hành vi và phân cụm |
| **Mã QR & Hình ảnh**| qrcode 8.2, Pillow 12.2.0 | Sinh mã QR PNG tự động |
| **Cổng thanh toán** | VietQR Napas 247 | Sinh mã QR ngân hàng thanh toán tự động |
| **Chatbot AI** | Google Gemini API / Groq API | Tích hợp fallback regex thông minh |

---

## ⚙️ Hướng dẫn cài đặt & Chạy dự án

### Bước 1: Clone kho mã nguồn từ GitHub
```bash
git clone https://github.com/Hango922/agrisense-platform.git
cd agrisense-platform
```

### Bước 2: Tạo môi trường ảo Python 3.14
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell không cho kích hoạt, dùng trực tiếp `.\.venv\Scripts\python.exe` thay cho `python` trong các lệnh bên dưới. Không cần thay đổi execution policy của máy.

### Bước 3: Cài đặt các thư viện cần thiết
```powershell
python -m pip install -r requirements.txt
python -m pip check
```

`requirements.in` ghi các dependency trực tiếp; `requirements.txt` khóa cả dependency gián tiếp cho Python 3.14 trên Windows. Cặp đã kiểm chứng là Django 6.1.2 và PyMySQL 1.2.3. Không dùng PyMySQL 1.1.1 với bộ Django này: backend MySQL từ chối phiên bản tương thích mà driver công bố.

Khi chủ động cập nhật dependency: sửa `requirements.in`, tạo virtualenv trống, chạy `python -m pip install -r requirements.in`, rồi dùng `python -m pip freeze` để tạo lại `requirements.txt`. Chỉ cài `requirements-dev.txt` sau khi xuất lock để không đưa công cụ test vào dependency chạy ứng dụng. Kiểm tra diff và chạy lại các bước kiểm chứng trước khi dùng lock mới.

### Bước 4: Tạo cơ sở dữ liệu MySQL
Mở MySQL Command Line Client hoặc MySQL Workbench và thực hiện:
```sql
CREATE DATABASE nongsan_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
```

### Bước 5: Cấu hình biến môi trường `.env`
> [!IMPORTANT]
> File `.env` chứa thông tin riêng và được `.gitignore` bỏ qua. Giữ nguyên file nếu đã cấu hình; chỉ sao chép mẫu khi cài mới.

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Điền khóa vừa tạo vào `SECRET_KEY`; cấu hình `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` theo MySQL của bạn. Giữ `DEBUG=True` và `ALLOWED_HOSTS=127.0.0.1,localhost` cho chạy local.

Hai API key AI trong mẫu để trống: chatbot sẽ dùng fallback, không cần tài khoản AI để khởi động. Điền các biến `VIETQR_*` bằng tài khoản nhận tiền phù hợp trước khi dùng thanh toán; mẫu chỉ có placeholder, không phải thông tin nhận tiền thật. `CHATBOT_TIMEOUT` là timeout từng lần gọi API, chưa phải giới hạn tổng thời gian.

`QR_BASE_URL` mặc định là `http://127.0.0.1:8000`. Để quét từ điện thoại, đặt URL theo IP LAN của máy chủ và thêm IP đó vào `ALLOWED_HOSTS` **trước khi tạo lô/seed QR**, rồi chạy `python manage.py runserver 0.0.0.0:8000`. Điện thoại cần cùng mạng và máy chủ cần cho phép kết nối cổng này. QR đã lưu không tự đổi khi sửa URL cấu hình.

### Bước 6: Khởi tạo bảng dữ liệu (Migration)
```bash
python manage.py migrate
python manage.py check
python manage.py makemigrations --check --dry-run
```

Bản checkout đã có migration; không cần tạo migration mới khi cài đặt. Tài khoản MySQL dùng cho cài đặt cần quyền tạo/sửa bảng trong database đã chọn.

### Bước 7: Khởi tạo dữ liệu mẫu (Seed Data)
```bash
python manage.py seed_data
```
Trên database trống, lệnh tạo 5 danh mục, 5 nhà cung cấp, 30 sản phẩm, 22 tài khoản (gồm 2 tài khoản demo bên dưới), 50 đơn hàng và 10 lô kèm QR. Sự kiện và một số dữ liệu mẫu được tạo ngẫu nhiên. Chỉ dùng lệnh cho database demo; chạy lại có thể thêm sự kiện hành vi.

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

Lệnh khuyến nghị cho toàn bộ bộ test:
```powershell
python manage.py test --settings=nongsan_project.test_settings --noinput
```

Settings test giữ kết nối MySQL từ môi trường, nhưng tạo database `test_agrisense_<mã ngẫu nhiên>` riêng cho mỗi lần chạy và tự xóa khi kết thúc. Tài khoản MySQL cần quyền tạo/xóa database test. File upload/QR test nằm trong bộ nhớ; AI luôn dùng fallback dù `.env` có API key thật. Không dùng settings này để chạy website thường ngày hoặc với `--keepdb`.

Kiểm tra nhanh bootstrap mà không cần database đã migrate:
```powershell
python -m unittest tests.test_environment tests.test_runtime -v
```

Đo coverage (tùy chọn, không cần để chạy website):
```powershell
python -m pip install -r requirements-dev.txt
python -m coverage run --branch --source=apps,nongsan_project --omit="*/tests/*,*/migrations/*" manage.py test --settings=nongsan_project.test_settings --noinput
python -m coverage report
```

Bộ test sau giai đoạn 1 gồm 60 test có sẵn và 5 test bootstrap/cô lập mới. Test đạt không đồng nghĩa các lỗi nghiệp vụ trong checklist bên dưới đã được sửa. Xem bằng chứng RED/GREEN, coverage và kiểm tra môi trường sạch tại [báo cáo giai đoạn 1](docs/PHASE_1_TDD.md).

## Checklist hoàn thiện

Phạm vi hiện tại: ổn định các luồng đã có, chưa mở rộng tính năng. Cập nhật ngày 18/11/2026.

- [x] **Giai đoạn 1 — Cài/chạy tái lập được:** khóa dependency, đồng bộ cấu hình/tài liệu, bổ sung test cô lập. Đã cài trên virtualenv thứ hai sạch, migrate database test, seed, cập nhật phân nhóm; 65/65 test đạt và `runserver` trả HTTP 200.
- [x] **Giai đoạn 2 — Quyền và đầu vào:** sửa quyền tra đơn chatbot, CSRF, validation và file bill. Hoàn thành khi request sai không gây HTTP 500, không lưu dữ liệu sai và không lộ đơn tài khoản khác.
- [x] **Giai đoạn 3 — Đơn hàng/tồn kho:** thống nhất chuyển trạng thái, chống gửi lặp và tranh chấp tồn kho. Hoàn thành khi không bán vượt kho, không hoàn kho nhiều lần, không chuyển trạng thái ngoài quy trình.
- [x] **Giai đoạn 4 — Khép kín luồng hiện có:** QR, giới hạn thời gian AI, sự kiện mua hàng, Excel và định nghĩa KPI. Hoàn thành khi các kênh cho kết quả nhất quán theo quy tắc đã chốt.
- [ ] **Giai đoạn 5 — Kiểm chứng/bàn giao:** regression cho các lỗi đã phát hiện, kiểm tra trình duyệt desktop/mobile và nâng coverage. Hoàn thành khi bộ kiểm tra đạt, luồng chính chạy trọn vẹn và tài liệu khớp hiện thực.

Báo cáo hiện tại và checklist nghiệm thu chi tiết: [ổn định luồng hiện có](docs/STABILIZATION.md). Giai đoạn 5 còn type check toàn dự án, E2E trình duyệt có đăng nhập và nghiệm thu môi trường triển khai.

Kết quả hiện tại: **99/99 test PASS; coverage 82,89%**, tính cả nhánh và loại test/migration, vượt mốc 80% của ECC. Coverage lịch sử sau giai đoạn 1 là 74,49%. Chưa kiểm chứng AI/ngân hàng thật hoặc triển khai production.

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
