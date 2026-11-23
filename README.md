# AgriSense — Nền tảng mua sắm nông sản tích hợp AI

> **Cập nhật ngày 20/11/2026:** giao diện mua sắm mới, trợ lý AI đi chợ theo ngân sách, combo mùa vụ, mua lại đơn hàng, quản lý tồn kho theo lô và dashboard vận hành. Xem [kiểm chứng AI planner](docs/AI_PLANNER_VERIFICATION.md) để biết kết quả tích hợp AI và các giới hạn còn lại.

> **Chạy thử:** xem [hướng dẫn demo](docs/UPGRADE_DEMO.md) (SQLite, cổng 8001) hoặc [hướng dẫn vận hành Windows](docs/OPERATIONS.md) (MySQL, Waitress). Thanh toán demo là mô phỏng; dự án chưa đạt nghiệm thu triển khai production. Các vấn đề vận hành được ghi tại [báo cáo kiểm chứng](docs/OPERATIONAL_VERIFICATION.md).

> **Dự án Bài tập lớn Hệ thống Thông tin / Công nghệ Phần mềm**  
> **Sinh viên thực hiện**: Nguyễn Hồng Hoàng  
> **Mã số sinh viên**: 20234070  
> **Lớp**: N09 — **Nhóm**: 2  
> **Thời gian thực hiện**: 14/10/2026 – 07/12/2026 (8 tuần)  
> **Repository GitHub**: [https://github.com/Hango922/agrisense-platform.git](https://github.com/Hango922/agrisense-platform.git)

---

## 🌾 Giới thiệu dự án

**AgriSense** là ứng dụng web bán nông sản Việt Nam, kết nối trải nghiệm mua sắm của khách hàng với hoạt động quản lý đơn hàng, tồn kho và nguồn gốc sản phẩm của cửa hàng. Dự án được xây dựng bằng **Python, Django và MySQL**, phục vụ bài tập lớn Hệ thống Thông tin / Công nghệ Phần mềm.

Với khách hàng, AgriSense hỗ trợ tìm kiếm nông sản, xem thông tin vùng trồng, lựa chọn combo theo mùa, đặt hàng và theo dõi đơn. Điểm nhấn là **trợ lý đi chợ theo ngân sách**: người dùng nhập nhu cầu, số người và số ngày để nhận danh sách sản phẩm cùng gợi ý món ăn. AI đề xuất từ danh mục hiện có; máy chủ kiểm tra lại giá, tồn kho và tổng tiền gồm phí giao hàng trước khi người dùng thêm vào giỏ. Chatbot hỗ trợ tư vấn, tra cứu đơn của người dùng và đặt hàng qua hội thoại.

Với cửa hàng, hệ thống quản lý tồn kho theo từng lô, ưu tiên xuất lô gần hết hạn (**FEFO**) và liên kết mã QR truy xuất với lô thực tế đã giao. Dashboard tập hợp đơn chờ xử lý, hàng tồn thấp, lô sắp hết hạn, thống kê bán hàng và báo cáo Excel. Dữ liệu tương tác còn được dùng để phân nhóm khách hàng theo quy tắc và gợi ý sản phẩm phù hợp.

Các năng lực nổi bật:

- **Mua sắm trọn luồng:** tài khoản, địa chỉ nhận hàng, danh mục, giỏ hàng, combo mùa vụ, đặt hàng và mua lại đơn cũ.
- **AI hỗ trợ lựa chọn:** tích hợp Gemini hoặc Groq cho planner và chatbot; có phương án trả lời theo quy tắc khi dịch vụ AI không khả dụng.
- **Kho và nguồn gốc:** nhập kho theo lô, kiểm tra hạn sử dụng, phân bổ tồn khi đặt hàng và hoàn kho khi hủy đơn hợp lệ.
- **Thanh toán:** COD, mã VietQR theo đơn, thanh toán mô phỏng trong bản demo và webhook có chữ ký HMAC để phục vụ tích hợp.
- **Quản trị và phân tích:** dashboard vận hành, biểu đồ bán hàng, phân nhóm hành vi và xuất báo cáo `.xlsx`.

**Phạm vi hiện tại:** ứng dụng phục vụ học tập và trình diễn trên môi trường local. AI hỗ trợ gợi ý mua sắm, chưa được kiểm chứng như công cụ tư vấn dinh dưỡng. VietQR tạo thông tin chuyển khoản; webhook chưa kết nối nhà cung cấp ngân hàng thực tế, nên không đồng nghĩa hệ thống đã tự động đối soát tiền nhận.

---

## 🚀 Các tính năng chính

### 1. Phân hệ Bán hàng & Thanh toán (E-Commerce Core & VietQR)
- **Quản lý tài khoản**: Đăng ký, đăng nhập, bảo mật mật khẩu Django, quản lý hồ sơ và sổ địa chỉ nhận hàng linh hoạt.
- **Duyệt & Tìm kiếm nông sản**: Tìm kiếm theo từ khóa tiếng Việt, lọc theo danh mục, mức giá và phân trang trực quan.
- **Chi tiết nông sản**: Xem hình ảnh, mô tả, xuất xứ nông trại, mùa vụ, hướng dẫn chế biến, cách bảo quản và đánh giá sao từ khách hàng.
- **Giỏ hàng & Đặt hàng COD / Chuyển khoản**: Thêm sản phẩm, cập nhật số lượng, kiểm tra tồn kho thời gian thực, tính phí giao hàng thông minh (30.000đ, miễn phí từ 500.000đ), trừ kho an toàn bằng `@transaction.atomic`.
- **Thanh toán nhanh VietQR (Napas 247)**: Sinh QR theo tài khoản nhận tiền cấu hình trong `VIETQR_*`, số tiền và mã đơn hàng (`ORDxxxxxxxx`). Nhân viên đối soát và xác nhận thủ công; hệ thống chưa tự xác minh giao dịch ngân hàng.
- **Quản lý đơn hàng**: Theo dõi lịch sử đơn hàng, xem chi tiết tiến độ giao hàng và hỗ trợ hủy đơn hàng khi đang chờ xác nhận (tự động hoàn kho).
- **Combo mùa vụ & Mua lại đơn**: Thêm nhóm sản phẩm vào giỏ theo giá và tồn kho hiện tại; kiểm tra toàn bộ trước khi thêm. Combo chưa có cơ chế chiết khấu riêng.

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
  - Hỗ trợ Gemini hoặc Groq Cloud API; chọn nhà cung cấp và mô hình qua biến môi trường. Planner có cấu hình `PLANNER_GEMINI_MODEL` riêng với chatbot (`GEMINI_MODEL`).
  - Bộ luật Fallback Regex thông minh nhận diện từ khóa tiếng Việt (giá cả, xuất xứ, bảo quản, tra cứu đơn hàng).
  - **Trợ lý lên đơn hàng tự động**: Khách nhắn câu lệnh tự nhiên (ví dụ: *"Tôi muốn mua 2kg cà chua bi, giao về số 15 Hai Bà Trưng Hà Nội, sđt 0987654321"*), Chatbot tự động phân tích sản phẩm, trừ tồn kho, tạo đơn hàng và gửi ảnh mã VietQR thanh toán tức thời ngay trong khung chat.

### 3. Đi chợ theo ngân sách (AI Planner)
- Nhập nhu cầu bằng tiếng Việt, ngân sách, số người, số ngày và nhóm thực phẩm ưu tiên tại `/products/planner/`.
- AI đề xuất sản phẩm từ danh mục đang bán, giải thích lựa chọn và gợi ý món ăn; khi lỗi hoặc thiếu khóa API, giao diện thông báo rõ việc dùng gợi ý theo quy tắc.
- Máy chủ kiểm tra mã sản phẩm, số lượng, giá, tồn kho và ngân sách gồm phí giao hàng. Giỏ chỉ được thêm sau thao tác của người dùng; đề xuất có thời hạn và cơ chế ngăn thêm lặp.
- Kết quả tích hợp, kiểm thử và giới hạn: [AI_PLANNER_VERIFICATION.md](docs/AI_PLANNER_VERIFICATION.md).

### 4. Thẩm định Nông sản & Độ tươi thông minh (Gemini Multimodal Vision Inspector)
- URL: `http://127.0.0.1:8000/products/inspect/`
- Tải ảnh hoặc chụp trực tiếp rau, củ, quả (hỗ trợ JPG, PNG, WEBP tối đa 10MB và camera di động).
- Sử dụng mô hình Gemini Multimodal Vision (`gemini-3.1-flash-lite` thông qua SDK `google-genai` mới) để:
  - **Nhận diện chính xác** tên nông sản và phân loại nhóm thực phẩm (Rau lá, Củ quả, Trái cây, Nấm...).
  - **Đánh giá thang điểm độ tươi mới** (0 - 100%) và xếp loại phẩm cấp (Loại 1, Loại 2, Cần dùng sớm, Hỏng).
  - **Phân tích cảm quan & khuyết tật**: kiểm tra độ căng bóng, màu sắc, tai cuống và phát hiện sớm dấu hiệu thâm dập, sâu bệnh hoặc nấm mốc.
  - **Hướng dẫn bảo quản chuẩn khoa học**: nhiệt độ, độ ẩm tối ưu và ước tính thời gian sử dụng an toàn còn lại.
  - **Gợi ý món ăn ngon**: đề xuất 2-3 món ăn chuẩn vị Việt Nam phù hợp với tình trạng nông sản.
  - **Liên kết kho hàng AgriSense**: tự động gợi ý và hiển thị các sản phẩm sạch tương ứng đang có sẵn trong kho hàng kèm giá và tồn kho thời gian thực.
- Hỗ trợ ảnh mẫu thử nghiệm 1-click và chế độ dự phòng ngoại tuyến (offline fallback) an toàn khi chưa cấu hình API key hoặc mất kết nối mạng.

### 5. Quản lý lô hàng & Truy xuất nguồn gốc (FEFO / QR)
- Nhập kho theo lô, theo dõi lượng còn lại và ưu tiên xuất lô gần hết hạn; lô quá hạn không được tính vào lượng có thể bán.
- Đơn hàng lưu phân bổ lô thực tế; hủy đơn hợp lệ hoàn lại đúng lô, tránh hoàn kho nhiều lần.
- Tự động sinh mã QR định dạng PNG chuẩn ISO cho từng lô hàng nông sản (`ProductBatch`).
- Mã QR trỏ đến `<QR_BASE_URL>/trace/<batch_code>/`; cấu hình URL trước khi tạo lô hàng.
- Cung cấp đầy đủ thông tin: Tên sản phẩm, nông trại / vùng trồng, ngày thu hoạch, ngày đóng gói, chứng nhận an toàn (VietGAP, GlobalGAP, Organic), sản lượng và nhật ký kiểm định.

### 6. Phân hệ Quản trị Dashboard (Admin Dashboard & Analytics)
- URL: `http://127.0.0.1:8000/dashboard/`
- Phân quyền nghiêm ngặt bằng `@method_decorator(staff_member_required, name='dispatch')`.
- **Việc cần xử lý**: Theo dõi đơn chờ lâu, hàng tồn thấp, lô cận hạn/quá hạn và truy cập chức năng nhập kho theo lô.
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
| **Thanh toán** | COD, VietQR, webhook HMAC | Sinh QR theo đơn; chưa tích hợp đối soát ngân hàng thực tế |
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
- **Đi chợ theo ngân sách**: [http://127.0.0.1:8000/products/planner/](http://127.0.0.1:8000/products/planner/)
- **Combo mùa vụ**: [http://127.0.0.1:8000/products/combos/](http://127.0.0.1:8000/products/combos/)
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

Checklist dưới đây ghi lại đợt ổn định luồng ngày 18/11/2026. Các nâng cấp sau đó được mô tả ở phần tính năng và báo cáo kiểm chứng riêng.

- [x] **Giai đoạn 1 — Cài/chạy tái lập được:** khóa dependency, đồng bộ cấu hình/tài liệu, bổ sung test cô lập. Đã cài trên virtualenv thứ hai sạch, migrate database test, seed, cập nhật phân nhóm; 65/65 test đạt và `runserver` trả HTTP 200.
- [x] **Giai đoạn 2 — Quyền và đầu vào:** sửa quyền tra đơn chatbot, CSRF, validation và file bill. Hoàn thành khi request sai không gây HTTP 500, không lưu dữ liệu sai và không lộ đơn tài khoản khác.
- [x] **Giai đoạn 3 — Đơn hàng/tồn kho:** thống nhất chuyển trạng thái, chống gửi lặp và tranh chấp tồn kho. Hoàn thành khi không bán vượt kho, không hoàn kho nhiều lần, không chuyển trạng thái ngoài quy trình.
- [x] **Giai đoạn 4 — Khép kín luồng hiện có:** QR, giới hạn thời gian AI, sự kiện mua hàng, Excel và định nghĩa KPI. Hoàn thành khi các kênh cho kết quả nhất quán theo quy tắc đã chốt.
- [ ] **Giai đoạn 5 — Kiểm chứng/bàn giao:** regression cho các lỗi đã phát hiện, kiểm tra trình duyệt desktop/mobile và nâng coverage. Hoàn thành khi bộ kiểm tra đạt, luồng chính chạy trọn vẹn và tài liệu khớp hiện thực.

Báo cáo hiện tại và checklist nghiệm thu chi tiết: [ổn định luồng hiện có](docs/STABILIZATION.md). Giai đoạn 5 còn type check toàn dự án, E2E trình duyệt có đăng nhập và nghiệm thu môi trường triển khai.

Kết quả đợt ổn định: **99/99 test PASS; coverage 82,89%**. Báo cáo nâng cấp AI ngày 19/11/2026 ghi nhận **162/162 test PASS; coverage 82,22%**, tính cả nhánh và loại test/migration. Gemini đã được kiểm chứng với planner local; chatbot, Groq, lint/type check toàn dự án và nghiệm thu vận hành còn các vấn đề được ghi trong [báo cáo AI planner](docs/AI_PLANNER_VERIFICATION.md). Chưa kiểm chứng giao dịch ngân hàng thật hoặc triển khai production.

Kiểm tra lại ngày **20/11/2026** trước khi cập nhật GitHub: **162/162 test đạt** trên database MySQL test riêng; `manage.py check`, `makemigrations --check --dry-run` và `pip check` đều đạt. Lần kiểm tra này không đo lại coverage hoặc gọi dịch vụ AI/ngân hàng thực tế.

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
