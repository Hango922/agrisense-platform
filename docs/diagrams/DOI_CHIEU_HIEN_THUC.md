# Đối chiếu mô hình nghiệp vụ với mã nguồn AgriSense

Ngày rà soát: 13/11/2026. Phiên bản mô hình: 2.0. Mã nền được đọc: commit `92bdac6` cùng trạng thái workspace tại thời điểm rà soát.

Tài liệu này phân biệt yêu cầu đích trong sơ đồ với hành vi hiện tại. Đây là rà soát tĩnh mã nguồn và kiểm tra cấu trúc tài liệu; không phải chứng nhận kiểm thử chạy hệ thống. Không có bản sửa mã ứng dụng trong công việc này.

## Các chênh lệch cần giải trình

| Mã | Use case | Quy tắc trong mô hình | Hiện thực đã quan sát / nguồn | Hệ quả và hướng xử lý |
|---|---|---|---|---|
| GAP01 | O06 | Chỉ tra đơn của tài khoản đang đăng nhập | `apps/chatbot/fallback.py:199` tìm bằng order_code, thiếu lọc user; nhánh đơn gần nhất ở dòng 220 có lọc user | Có khả năng lộ thông tin đơn bằng mã. Cần kiểm tra đăng nhập và sở hữu trên mọi nhánh trước khi trả dữ liệu |
| GAP02 | O08–O11 | Cưỡng chế ma trận trạng thái; chỉ hủy pending | `apps/dashboard/views.py:219` nhận target_status, dòng 260 gán trực tiếp; hoàn kho ở dòng 225 chỉ chạy khi trạng thái cũ pending | Có thể đổi trái quy trình; hủy sau pending không tương đương luồng hủy chuẩn. Cần dịch vụ chuyển trạng thái dùng chung cho web/Admin/bulk |
| GAP03 | O01/O02/O05/O11/S01 | Không bán vượt kho; hủy hoàn kho đúng một lần; chống gửi lặp | `apps/cart_orders/services.py:22`, `:73`, `:91` dùng atomic nhưng thao tác đọc/sửa stock không có khóa dòng/idempotency | atomic không tự chống mất cập nhật/hai yêu cầu đồng thời. Cần khóa/điều kiện cập nhật nguyên tử và chống tạo/hủy lặp |
| GAP04 | Q04/O08/O12 | Chỉ xác nhận VietQR sau kiểm tra giao dịch thật | `apps/dashboard/views.py:232` chấp nhận chứng từ hiện có hoặc tải lên; `apps/cart_orders/admin.py:49`, `:124`, `:144` có nhánh tự sinh ảnh đối soát | Có ảnh không chứng minh tiền về. Cần lưu kết quả đối soát, người, thời điểm/tham chiếu; không coi ảnh tạo nội bộ là xác minh tự động |
| GAP05 | Q02/Q05 | Chỉ nộp cho đơn VietQR pending, tệp hợp lệ | `apps/cart_orders/views.py:173` kiểm tra chủ đơn + pending + có tệp, chưa kiểm tra payment_method và validation tệp đầy đủ tại endpoint | Cần kiểm tra phương thức, định dạng/nội dung/dung lượng. Quyền truy cập URL media chứng từ cũng cần kiểm thử khi triển khai; kiểm tra trang đơn chưa chứng minh media được bảo vệ |
| GAP06 | C02/C03/O01 | Số lượng và thông tin giao hàng/phương thức hợp lệ | `apps/cart_orders/views.py:32`, `:62` dùng int trực tiếp; thêm giỏ chưa chặn số không dương; `:101` nhận dữ liệu POST và chuyển cho service | Cần form/serializer validation; từ chối số sai, phương thức ngoài tập cho phép, thông tin trống; kiểm tra lại sản phẩm đang bán khi chốt |
| GAP07 | T05 | QR luôn khớp mã lô hiện hành | `apps/traceability/models.py:37` chỉ sinh khi thiếu qr_code, điều kiện ở dòng 40 | Đổi batch_code có thể giữ QR cũ. Chọn mã lô bất biến hoặc tái tạo QR khi đổi dữ liệu URL |
| GAP08 | T07/T08 | Chỉ nói có lịch sử đã ghi, không hứa tự ghi mọi thay đổi | `apps/traceability/models.py:50` định nghĩa TraceabilityRecord; `apps/traceability/admin.py:27` quản trị riêng; ProductBatch.save không tự tạo record mỗi lần sửa | Muốn nhật ký đầy đủ cần cơ chế ghi tự động và chính sách bất biến. Hiện sơ đồ chỉ mô tả xem/hiệu chỉnh bản ghi |
| GAP09 | A10 và các use case staff | Phân quyền theo nhiệm vụ; quyền cấp nhóm thuộc admin | `apps/dashboard/views.py:29` và các view Dashboard dùng staff_member_required; `apps/accounts/admin.py:11` kế thừa BaseUserAdmin, chưa có hạn chế field riêng cho chính sách A10 | Staff gate không bằng quyền model từng nghiệp vụ. Cần rà quyền Dashboard, trường groups/user_permissions/is_superuser và chống tự nâng quyền |
| GAP10 | R01/R05 | Thuật toán và nhật ký phải mô tả đúng | `apps/recommendation/engine.py:37` loại sản phẩm trong mọi đơn của user (kể cả cancelled), không lấp đầy nhánh cá nhân hóa; `apps/behavior/admin.py` có RecommendationLog nhưng engine không ghi mỗi lần trả gợi ý | Đặc tả giữ đúng hành vi hiện có; không nói đã có log gợi ý đầy đủ hoặc tối ưu theo lịch sử mua thành công |
| GAP11 | D03/R01 | Không coi mọi kênh đều có đủ event | `apps/cart_orders/views.py:115` ghi purchase sau checkout; `apps/cart_orders/services.py:91` tạo trực tiếp không ghi purchase; `apps/chatbot/views.py:21` lưu chat nhưng không tạo UserEvent chat | Thống kê và phân nhóm có thể thiếu event của kênh chat. Cần thống nhất điểm ghi sự kiện; phân biệt ChatMessage với UserEvent |
| GAP12 | R03 | Giải thích đúng tập người dùng và tập đơn | `apps/behavior/segmentation.py:17` tính mọi đơn không cancelled; `:44` duyệt mọi active user và chỉ ghi lịch sử khi nhóm thay đổi | Không gọi đây là đếm riêng đơn delivered. Có cả staff; không có bằng chứng scheduler được cấu hình. Cần quyết định chính sách chính thức nếu muốn khác |
| GAP13 | D01/D02 | Nêu đúng nghĩa KPI và phạm vi xuất | `apps/dashboard/views.py:40` cộng đơn không cancelled; `:46` top sản phẩm chưa loại cancelled; `:183` có tổng delivered riêng; `:432` xuất tất cả đơn | Không gọi toàn bộ các số này là tiền đã thu. Danh sách ở `:203`/`:358` giới hạn 100; export không theo bộ lọc trang |
| GAP14 | D04 | Bảo trì dữ liệu phụ trợ không vượt quy trình bán hàng | `apps/cart_orders/admin.py:20`, `:77`; `apps/chatbot/admin.py`; `apps/behavior/admin.py` đăng ký Admin với quyền theo model và inline chỉ đọc | Admin có thể cho sửa/xóa dữ liệu rộng hơn nghiệp vụ đích. Không quảng cáo raw CRUD như cách xử lý đơn chuẩn; cần hạn chế trường/quyền và kiểm tra ảnh hưởng |
| GAP15 | A11 | Địa chỉ mặc định nhất quán | `apps/accounts/models.py` UserAddress.is_default là Boolean; không có ràng buộc duy nhất theo user; `apps/cart_orders/views.py:97` lấy địa chỉ mặc định đầu tiên | Có thể tồn tại nhiều địa chỉ mặc định. Cần quy tắc chọn duy nhất nếu yêu cầu nghiệp vụ đòi hỏi |
| GAP16 | O01 | Phản hồi tạo đơn và ghi event không gây đặt trùng | `apps/cart_orders/views.py:115` ghi event sau khi create_order_from_cart trả về; giao dịch service đã kết thúc | Lỗi event có thể xảy ra sau khi đơn đã commit. Cần xử lý hậu xử lý/idempotency để người dùng không gửi lại và tạo trùng |
| GAP17 | P04 | Chỉ công khai sản phẩm theo chính sách đã xác định | `apps/products/views.py:85` ProductDetailView không lọc is_active trong queryset mặc định, trong khi list/search có lọc | Cần quyết định việc truy cập URL trực tiếp sản phẩm đã tắt; không suy ra ẩn trên danh sách đồng nghĩa không xem được chi tiết |

## Những khác biệt là lựa chọn mô hình, không tự động là lỗi mã

- Chức năng đặt/tra đơn qua hội thoại thuộc F3; giao diện nằm trong chatbot không làm nó thành trách nhiệm chính của F7.
- Dashboard là một kênh thao tác. Tra cứu sản phẩm/đơn/lô vẫn thuộc F2/F3/F5; F8 chịu trách nhiệm chỉ số, báo cáo, phân tích và bảo trì phụ trợ.
- 32 nhánh chức năng không cần tương ứng một-một với 70 mục tiêu. Ví dụ 5.3 cung cấp QR là chức năng hỗ trợ nằm trong T02/T04/T05.
- R01 xuất hiện ở hai trang nhưng chỉ có một ID, một chủ sở hữu F6. H05 xuất hiện trong trang quản trị nhưng thuộc F7.
- “Quản lý” không mặc nhiên nghĩa là có đủ CRUD; phạm vi từng mục được ghi trong đặc tả và ma trận.
- Lọc P02 có thể mô hình như hành vi bên trong P01 ở một phong cách trình bày khác. Bản này chủ động tách extend với điều kiện và điểm mở rộng rõ ràng, không dùng extend để biểu thị mọi nhánh if.
- S01 được tách vì O05 và O11 cùng cần hoàn kho trong luồng thành công. Các bước tính tiền, lưu CSDL, kiểm tra tồn không tách thành mục tiêu người dùng.
- Tác nhân là vai trò tương tác với biên hệ thống, không phải mọi danh từ trong dữ liệu. Supplier là dữ liệu do staff quản trị; chưa có cổng nhà cung cấp. Người giao hàng chưa có giao diện trong phạm vi. Bộ máy gợi ý, fallback, CSDL và Django ở trong hệ thống.
- Không có chức năng quên mật khẩu tự phục vụ, sửa hồ sơ/địa chỉ trên storefront được xác định; A08/A11 là quản trị. Đăng ký có đăng nhập tự động.

## Câu trả lời có căn cứ khi bảo vệ

| Câu hỏi | Cách giải thích |
|---|---|
| Vì sao sơ đồ đầu là cây, không có actor? | Đây là phân rã chức năng mức 0–1–2. Sơ đồ use case bắt đầu từ trang 2; hai loại sơ đồ có mục đích khác nhau |
| Vì sao tổng quát không chứa 70 ellipse? | Trang 2 dùng 16 mục tiêu tổng quát SG; ma trận phân rã đủ 70 mục tiêu chi tiết giúp đọc được và kiểm tra độ phủ |
| Vì sao có hai vai trò tổng quát V/U nhưng tổng quát nói 7 tác nhân? | 7 tác nhân cụ thể là khách vãng lai, khách hàng, staff, admin, operator, dịch vụ AI và ảnh VietQR; V/U gom khả năng dùng chung trên trang kế thừa |
| Nộp bill đã là thanh toán xong chưa? | Chưa. Bill là chứng từ do người dùng nộp, nhân viên phải đối soát ngân hàng thực tế |
| Mô hình đã khớp mã 100% chưa? | Đây là mô hình đích có đối chiếu; bảng GAP chỉ rõ chỗ mã đang thiếu hoặc khác. Không dùng sơ đồ để khẳng định mã đã sửa |
| Có chắc không thiếu yêu cầu nào không? | Đã đối chiếu các kênh và nhóm nghiệp vụ trong repository; chưa thể xác nhận yêu cầu ngoài phạm vi hoặc tiêu chí riêng chưa được cung cấp |

## Giới hạn kiểm chứng

Đã đọc các view, service, model, Admin và URL liên quan; đã kiểm tra hình của 21 trang và tính nhất quán ID/quan hệ/độ phủ qua tệp xuất. Chưa chạy thử hệ thống, chưa kiểm thử tải đồng thời, chưa kiểm tra cấu hình production/media hoặc dịch vụ AI/ngân hàng thực tế. Các gợi ý sửa mã trong bảng GAP chưa được thực hiện.
