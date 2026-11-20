# Kiểm chứng bản vận hành Windows — 19/11/2026

**Kết luận: NOT READY cho vận hành thật.** Hạ tầng chạy local và kiểm thử chức
năng đã đạt, nhưng kết nối Gemini thực tế, thông tin bảo mật và kiểm tra chất
lượng toàn dự án còn vấn đề. Không dùng báo cáo demo cũ để thay thế kết quả này.

| Hạng mục | Kết quả | Bằng chứng |
| --- | --- | --- |
| Django check | PASS | Không có lỗi cấu hình |
| Migration | PASS | Migration RequestQuota đã áp dụng; makemigrations --check không phát hiện thay đổi |
| Static/templates | PASS | collectstatic thành công; toàn bộ template biên dịch được |
| Dependencies | PASS | pip check: No broken requirements found |
| Tests | PASS | 145/145, 86,596 giây; MySQL test database riêng, đã xóa sau kiểm thử |
| Coverage | PASS | 81,41%, đo cả nhánh, source apps/nongsan_project; loại tests/migrations |
| Types | FAIL | Pyright 74 lỗi toàn dự án với interpreter .venv |
| Lint | FAIL | Ruff còn 89 lỗi; đã áp dụng các sửa tự động an toàn |
| Diff whitespace | PASS | git diff --check |
| Quét mẫu khóa trong mã | PASS giới hạn | Không khớp mẫu Gemini/Groq/OpenAI; .env được Git ignore; không thay thế security audit |
| Bảo mật vận hành | FAIL | Hai admin có mật khẩu demo đã biết; SECRET_KEY bị Django cảnh báo; DB user là root |
| Gemini thực tế | FAIL | List models HTTP 200; generateContent gemini-2.5-flash HTTP 404; thử model thay thế timeout/503 |
| Thanh toán thật | CHƯA KIỂM TRA | Chưa chọn/tích hợp nhà cung cấp ngân hàng; không thực hiện giao dịch tiền thật |

Log chi tiết trong thư mục `logs/` (được Git ignore):
`operational-tests-final.txt`, `operational-coverage-final.txt`,
`operational-types-final.json`, `operational-lint-final.json`,
`operational-deploy.txt`, `operational-focused.txt`, `operational-startup-gate.txt`.

## Nghiệm thu môi trường đích

Windows hiện tại, Python 3.14, Django 6.1.2, Waitress 3.0.2, WhiteNoise 6.9.0.
Smoke test local **VERIFIED ở phạm vi đã chạy**: `/health/`, `/`, `/products/`,
`/accounts/login/`, `/static/css/market.css` trả 200 trên 127.0.0.1:8000;
truy cập bill không đăng nhập chuyển sang đăng nhập. Chrome mở trang login
thành công và không hiển thị bảng tài khoản demo.

Sau smoke test đã dừng tiến trình Waitress thử nghiệm. Bản cuối thêm preflight:
khởi động bị chặn đúng thiết kế vì tài khoản `admin`, `demo_admin` còn mật khẩu
demo. Không có tiến trình bản vận hành đang nghe cổng 8000 khi kết thúc kiểm tra.
Demo cổng 8001 được giữ riêng. **Nghiệm thu vận hành tổng thể: FAILED** cho đến
khi cấu hình bảo mật và Gemini được xử lý, rồi chạy lại kiểm tra trên bản cuối.

`check --deploy` còn 5 cảnh báo: SECRET_KEY và 4 cấu hình HTTPS/cookie/HSTS.
HTTP loopback chưa cung cấp HTTPS; không dùng cấu hình này để public website.
SECRET_KEY là vấn đề cần sửa ngay cả khi chạy local.

## Thay đổi chính

- Waitress loopback, WhiteNoise/static manifest, log xoay vòng, giới hạn upload.
- Giới hạn đăng nhập/đăng ký/chat bằng bộ đếm database, có lệnh dọn bộ đếm cũ.
- Logout bằng POST/CSRF; ẩn credential demo; chặn seed dữ liệu mẫu khi vận hành.
- Chỉ phục vụ ảnh sản phẩm/QR công khai; bill vẫn cần xác thực.
- Khóa Gemini nằm trong header; lỗi AI không ghi nội dung exception có thể chứa khóa.
- Kiểm tra Gemini bằng prompt tổng hợp, không gửi dữ liệu khách hàng.
- Bỏ QR cá nhân cố định; thiếu cấu hình ngân hàng thì backend từ chối VietQR
  và giao diện checkout ẩn lựa chọn này trong chế độ vận hành.
- Script khởi động và kiểm tra mật khẩu quản trị trước khi mở listener.

## Việc còn phải xử lý

1. Đổi mật khẩu `admin`, `demo_admin` tại terminal; thay SECRET_KEY, thu hồi khóa
   Gemini đã chia sẻ và đặt khóa mới trong .env. Không gửi khóa/mật khẩu vào chat.
2. Dùng DB user riêng và kiểm tra quyền tối thiểu. Xác nhận tài khoản ngân hàng
   cấu hình thuộc cửa hàng trước khi nhận chuyển khoản.
3. Kiểm tra lại quyền/model/quota Gemini bằng `check_integrations`; chỉ công nhận
   thành công khi generateContent nhận phản hồi có nội dung.
4. Xử lý 74 lỗi kiểu (chủ yếu thuộc tính ORM động, admin decorators, Optional,
   form/upload types) và 89 lint (class mutable defaults Django, broad exception,
   biến thừa, nối chuỗi và test style). Không tắt toàn bộ rule để làm xanh báo cáo.
5. Chưa kiểm thử Windows Service/khởi động lại máy, backup/restore, tải dài hạn,
   HTTPS/public host, webhook ngân hàng thật, giao dịch tiền thật, thao tác mua
   hàng qua trình duyệt trên database vận hành. Luồng đặt hàng đã được kiểm thử
   tự động trên database test; không tạo đơn thật để thử trên dữ liệu người dùng.
6. Cần quy trình đối soát bill thủ công, xử lý đơn treo giữ tồn và lô hết hạn
   trong thời gian chờ giao. Chưa coi các quy trình này là tự động hoàn chỉnh.

Hướng dẫn sửa cấu hình và chạy: [OPERATIONS.md](OPERATIONS.md).
