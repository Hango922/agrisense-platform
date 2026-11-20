# Báo cáo kiểm chứng nâng cấp AgriSense

Ngày 19/11/2026 (Asia/Saigon). Thực hiện theo skill verification-loop.

**Kết luận: chạy được bản demo local; chưa đạt toàn bộ cổng chất lượng để coi là sẵn sàng production.**

| Hạng mục | Kết quả | Bằng chứng / phạm vi |
| --- | --- | --- |
| Django / build | PASS | `manage.py check`, Python compileall, collectstatic; pip check không có dependency hỏng |
| Migration | PASS | Không còn thay đổi model chưa tạo migration; migration đã áp dụng trên MySQL hiện tại và SQLite demo |
| Tests | PASS | 134/134, MySQL test database riêng; gồm 35 test bổ sung so với 99 test ban đầu |
| Coverage | PASS | 82.90% statement + branch, ngưỡng 80%; loại test/migration |
| Type-check phần mới | PASS | 9 module nghiệp vụ/test mới hoặc mở rộng, 0 lỗi/0 cảnh báo |
| Type-check toàn dự án | FAIL | 75 lỗi; bản HEAD trước sửa có 77 lỗi khi dùng cùng interpreter |
| Lint phần mới | PASS | Ruff trên 9 module nghiệp vụ/test mới hoặc mở rộng |
| Lint lỗi thực thi cơ bản | PASS | Ruff `E9,F63,F7,F82` toàn apps/settings/tests |
| Lint đầy đủ | FAIL | 131 cảnh báo/lỗi theo cấu hình hiện tại; bản HEAD trước sửa có 139 |
| Bảo mật trong phạm vi thay đổi | PASS | Không phát hiện mẫu private key/API token trong 50 file nguồn/tài liệu đã quét; test CSRF, quyền sở hữu, chữ ký webhook, số tiền, chống gửi lặp đạt |
| Diff | PASS | `git diff --check`; đã xem thay đổi nghiệp vụ và migration, giữ thư mục diagrams có sẵn của người dùng |
| Nghiệm thu demo local | VERIFIED | Django 6.1.2, localhost:8001, SQLite riêng, dữ liệu minh họa |
| Ngân hàng / production | NOT PERFORMED | Chưa có adapter nhà cung cấp và kiểm chứng giao dịch thật; chưa triển khai production |

## Luồng đã chạy trên trình duyệt

- Trang chủ: 375px, 768px, 1024px, 1440px không tràn ngang; không có ảnh lỗi đã tải và không có console error/warning trong lần kiểm tra cuối. Ảnh lazy-load chưa vào viewport không tính là ảnh lỗi.
- Đăng nhập khách; nhập `300k mua rau củ cho 2 người trong 3 ngày`; hệ thống đề xuất 6 mặt hàng, 225.000đ tiền hàng + 30.000đ phí giao = 255.000đ. Tăng số lượng vượt ngân sách khóa nút thêm; khôi phục số lượng mở lại nút.
- Thêm giỏ gợi ý → checkout → tạo đơn VietQR demo → thấy 6 lô đã phân bổ → mô phỏng nhận tiền → đơn chuyển confirmed, payment_status=demo_paid. Không hiển thị QR ngân hàng thật trên đơn demo.
- Thêm combo vào giỏ: 3 mặt hàng, thông báo thành công.
- Đăng nhập admin → dashboard/việc cần xử lý; sửa lỗi header tràn ngang ở 390px, kiểm tra lại document width=390px. Dashboard hiển thị 3 biểu đồ, không có console error/warning.
- Nhập lô `DEMO-UI-RECEIPT-001` bằng form quản trị: thành công; QR nguồn gốc được tạo.
- Catalog mới: bộ lọc, sắp xếp và 12 thẻ sản phẩm hiển thị ở 390px, không tràn ngang.

## Kiểm thử nghiệp vụ đáng chú ý

- FEFO chọn lô gần hết hạn trước, tách số lượng qua nhiều lô; rollback toàn đơn khi một dòng không đủ hàng còn hạn.
- Lô hết hạn không được bán; hủy sau khi lô hết hạn hoàn tồn vật lý nhưng không mở lại bán.
- Hai kết nối MySQL mua cùng lúc: chỉ một đơn thành công; hai yêu cầu hủy: chỉ hoàn tồn sản phẩm/lô một lần.
- Không cho chuyển sản phẩm sang quản lý lô nếu còn đơn legacy pending chưa gắn lô.
- Giỏ chỉnh vượt ngân sách, giá đổi, số lượng không hợp lệ, token giả/hết hiệu lực/đã dùng không được thêm.
- Mua lại chỉ áp dụng đơn của chính tài khoản; combo/gợi ý thêm toàn bộ hoặc không thêm gì khi lỗi.
- Webhook xác thực HMAC, thời gian, VND, số tiền, trạng thái đơn; giao dịch gửi lặp không ghi nhận hai lần, không dùng cùng mã để thanh toán đơn khác.
- Chế độ demo tách khỏi đơn thật; không có secret thì webhook trả 503, sai chữ ký trả 403.

## Lỗi cần xử lý tiếp

1. Type-check toàn dự án: khai báo quan hệ động Django còn thiếu (`Cart.items`, địa chỉ User, display methods), kiểu admin/forms chưa khớp stub, xử lý Optional trong chatbot/openpyxl/test. Các module mới đã đạt; không tắt các cảnh báo toàn dự án để tạo kết quả PASS giả.
2. Ruff đầy đủ: chủ yếu `RUF012` (thuộc tính class mutable theo mẫu Django), `I001` (thứ tự import), `RUF059/F401` (biến/import chưa dùng), `BLE001/S110` (bắt/nuốt exception rộng) và một số quy tắc style. Cần phân loại quy tắc dành cho framework và sửa lỗi có ý nghĩa; chưa autofix toàn bộ code cũ ngoài phạm vi nâng cấp.
3. Thanh toán thật: triển khai adapter cho nhà cung cấp, cấu hình secret, xác thực thông báo từ provider và chạy thử giao dịch đầu-cuối. Endpoint hiện tại là hợp đồng HMAC nội bộ đã test, không phải tuyên bố đã tích hợp một ngân hàng cụ thể.

## Phần chưa kiểm chứng / giới hạn

- Chưa gọi Gemini/Groq thật; demo dùng fallback. Giỏ theo ngân sách sử dụng quy tắc tiếng Việt và tính toán xác định; không phải thực đơn dinh dưỡng hay mô hình AI mới được huấn luyện.
- Chưa kiểm tra tiền thật, hoàn tiền, thông báo thiếu/thừa tiền, hoặc callback của một cổng thanh toán cụ thể.
- Chưa nghiệm thu HTTPS, deploy production, tải lớn, backup/restore và audit dependency CVE.
- Responsive đã kiểm tra trong Chromium giả lập; chưa kiểm tra Safari/iOS hoặc thiết bị vật lý. CSS/Bootstrap/icons/fonts còn dùng CDN, chưa nghiệm thu offline hoàn toàn.
- Demo dùng SQLite để tiện chạy; chỉ kết quả test MySQL chứng minh các kiểm tra khóa hàng đồng thời.

## Tái lập và bằng chứng

Hướng dẫn chạy và kịch bản trình diễn: [UPGRADE_DEMO.md](UPGRADE_DEMO.md).

Các log local (thư mục logs được gitignore):

- `logs/coverage-upgrade-tests.txt`: kết quả 134 test cuối cùng.
- `logs/coverage-upgrade.txt`, `logs/coverage-upgrade.json`: coverage.
- `logs/full-types-upgrade.json`, `logs/full-lint-upgrade.json`: toàn bộ lỗi có file/dòng.
- `logs/baseline-types.json`, `logs/baseline-lint.json`: đối chiếu code HEAD trước nâng cấp.
- `logs/security-upgrade.json`: phạm vi quét mẫu secret.

Chạy Pyright bằng đúng virtualenv (`--pythonpath .venv/Scripts/python.exe`, nên dùng đường dẫn tuyệt đối). Chạy không chỉ định interpreter có thể dùng stub khác và tạo nhiều lỗi không tương đương; không dùng lượt đó để so baseline.
