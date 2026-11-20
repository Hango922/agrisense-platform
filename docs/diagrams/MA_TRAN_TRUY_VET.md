# Ma trận truy vết AgriSense v2

Ngày: 13/11/2026. 70 mục tiêu, 1 use case hỗ trợ, 21 trang. Mỗi mục tiêu có đúng một nhóm nghiệp vụ sở hữu, một nhánh chức năng chính và một mục tiêu tổng quát SG. Việc lặp cùng mã trên nhiều trang chỉ là tham chiếu.

## Nhóm sở hữu

| Mã | Nhóm | Nguồn đối chiếu |
|---|---|---|
| F1 | Tài khoản và quyền | apps/accounts/views.py; apps/accounts/forms.py; apps/accounts/admin.py |
| F2 | Thông tin nông sản | apps/products/views.py; apps/products/admin.py; apps/dashboard/views.py |
| F3 | Giỏ và đơn hàng | apps/cart_orders/views.py; apps/cart_orders/services.py; apps/cart_orders/admin.py; apps/chatbot/order_assistant.py; apps/chatbot/fallback.py; apps/dashboard/views.py |
| F4 | Thanh toán và đối soát | apps/cart_orders/vietqr.py; apps/cart_orders/views.py; apps/cart_orders/admin.py; apps/dashboard/views.py |
| F5 | Truy xuất nguồn gốc | apps/traceability/views.py; apps/traceability/models.py; apps/traceability/admin.py; apps/traceability/qr_generator.py |
| F6 | Cá nhân hóa và phân nhóm | apps/recommendation/engine.py; apps/behavior/segmentation.py; apps/behavior/admin.py; apps/dashboard/views.py |
| F7 | Tư vấn và hội thoại | apps/chatbot/views.py; apps/chatbot/services.py; apps/chatbot/fallback.py; apps/chatbot/admin.py |
| F8 | Giám sát và báo cáo | apps/dashboard/views.py; apps/behavior/admin.py; apps/cart_orders/admin.py; apps/chatbot/admin.py |

## 32 nhánh phân cấp

| Nhánh | Chức năng | Mã use case / bước được phục vụ |
|---|---|---|
| 1.1 | Xác thực tài khoản | A01, A02, A03 |
| 1.2 | Xem hồ sơ cá nhân | A04 |
| 1.3 | Quản trị người dùng | A05, A06, A07, A08, A09 |
| 1.4 | Quản trị địa chỉ và quyền | A10, A11 |
| 2.1 | Khám phá và đánh giá | P01, P02, P03, P04, P05, P16 |
| 2.2 | Quản trị sản phẩm, tồn kho | P06, P07, P08, P09 |
| 2.3 | Quản trị danh mục | P10, P11, P12 |
| 2.4 | Quản trị nhà cung cấp | P13, P14, P15 |
| 3.1 | Quản lý giỏ cá nhân | C01, C02, C03, C04 |
| 3.2 | Tiếp nhận đơn từ web/chat | O01, O02 |
| 3.3 | Theo dõi đơn cá nhân | O03, O04, O06 |
| 3.4 | Xử lý và hủy đơn | O05, O07, O08, O09, O10, O11, O12, S01 |
| 4.1 | Cung cấp thông tin VietQR | Q01 |
| 4.2 | Tiếp nhận chứng từ | Q02, Q05 |
| 4.3 | Xem chứng từ thanh toán | Q03 |
| 4.4 | Ghi nhận đối soát | Q04 |
| 5.1 | Tra cứu nguồn gốc công khai | T01, T02 |
| 5.2 | Quản trị thông tin lô | T03, T04, T05, T06 |
| 5.3 | Cung cấp QR truy xuất | Bước sinh/hiển thị QR của T04, T05 và kênh khởi tạo T02; không đếm thêm mục tiêu |
| 5.4 | Quản trị nhật ký lô | T07, T08 |
| 6.1 | Gợi ý nông sản | R01 |
| 6.2 | Tra cứu phân nhóm khách | R02 |
| 6.3 | Cập nhật phân nhóm | R03 |
| 6.4 | Tra cứu lịch sử và gợi ý | R04, R05 |
| 7.1 | Tư vấn nông sản | H01 |
| 7.2 | Xem lịch sử hội thoại | H02, H03 |
| 7.3 | Bắt đầu hội thoại mới | H04 |
| 7.4 | Tra cứu hội thoại quản trị | H05 |
| 8.1 | Theo dõi chỉ số kinh doanh | D01 |
| 8.2 | Phân tích hành vi | D03 |
| 8.3 | Xuất báo cáo đơn hàng | D02 |
| 8.4 | Bảo trì dữ liệu quản trị | D04 |

## Tổng quát đến chi tiết

| SG | Mục tiêu tổng quát | Mã chi tiết |
|---|---|---|
| SG01 | Sử dụng tài khoản | A01, A02, A03, A04 |
| SG02 | Khám phá và đánh giá nông sản | P01, P02, P03, P04, P05 |
| SG03 | Mua sắm và đặt hàng | C01, C02, C03, C04, O01, O02 |
| SG04 | Theo dõi / hủy đơn cá nhân | O03, O04, O05, O06 |
| SG05 | Thanh toán và gửi chứng từ | Q01, Q02, Q03 |
| SG06 | Tra cứu nguồn gốc | T01, T02 |
| SG07 | Nhận gợi ý nông sản | R01 |
| SG08 | Tư vấn và quản lý hội thoại | H01, H02, H03, H04 |
| SG09 | Quản trị tài khoản và quyền | A05, A06, A07, A08, A09, A10, A11 |
| SG10 | Quản trị nông sản và dữ liệu gốc | P06, P07, P08, P09, P10, P11, P12, P13, P14, P15, P16 |
| SG11 | Xử lý đơn hàng | O07, O08, O09, O10, O11, O12 |
| SG12 | Đối soát thanh toán | Q04, Q05 |
| SG13 | Quản trị lô và nhật ký nguồn gốc | T03, T04, T05, T06, T07, T08 |
| SG14 | Tra cứu phân nhóm và gợi ý | R02, R04, R05 |
| SG15 | Giám sát, báo cáo và bảo trì | D01, D02, D03, D04, H05 |
| SG16 | Cập nhật phân nhóm khách hàng | R03 |

Q03 cũng được nhân viên sử dụng tại trang 15; SG12 tham chiếu Q03 khi đối soát, nhưng Q03 được đếm một lần ở SG05. R01 xuất hiện ở trang khám phá và cá nhân hóa, luôn thuộc F6. H05 nằm ở trang thao tác quản trị nhưng thuộc F7. SG là mức tổng quát, không phải 16 use case bổ sung vào tổng 70.

## Danh mục toàn bộ

| Mã | Mục tiêu | Nhóm / nhánh | Tác nhân trực tiếp | SG | Trang |
|---|---|---|---|---|---|
| A01 | Đăng ký tài khoản | F1 / 1.1 | Khách vãng lai | SG01 | 04 |
| A02 | Đăng nhập | F1 / 1.1 | Người truy cập (vai trò tổng quát) | SG01 | 04 |
| A03 | Đăng xuất | F1 / 1.1 | Người đã đăng nhập (vai trò tổng quát) | SG01 | 04 |
| A04 | Xem hồ sơ và sổ địa chỉ | F1 / 1.2 | Người đã đăng nhập (vai trò tổng quát) | SG01 | 04 |
| A05 | Thêm tài khoản người dùng | F1 / 1.3 | Nhân viên được cấp quyền | SG09 | 05 |
| A06 | Sửa thông tin người dùng | F1 / 1.3 | Nhân viên được cấp quyền | SG09 | 05 |
| A07 | Khóa / mở khóa tài khoản | F1 / 1.3 | Nhân viên được cấp quyền | SG09 | 05 |
| A08 | Đặt lại mật khẩu người dùng | F1 / 1.3 | Nhân viên được cấp quyền | SG09 | 05 |
| A09 | Xóa tài khoản người dùng | F1 / 1.3 | Nhân viên được cấp quyền | SG09 | 05 |
| A10 | Phân nhóm và cấp quyền truy cập | F1 / 1.4 | Quản trị viên | SG09 | 06 |
| A11 | Cập nhật sổ địa chỉ của khách | F1 / 1.4 | Nhân viên được cấp quyền | SG09 | 06 |
| P01 | Duyệt nông sản đang bán | F2 / 2.1 | Người truy cập (vai trò tổng quát) | SG02 | 07 |
| P02 | Lọc nông sản | F2 / 2.1 | Người truy cập (vai trò tổng quát) | SG02 | 07 |
| P03 | Tìm kiếm nông sản | F2 / 2.1 | Người truy cập (vai trò tổng quát) | SG02 | 07 |
| P04 | Xem chi tiết nông sản | F2 / 2.1 | Người truy cập (vai trò tổng quát) | SG02 | 07 |
| P05 | Gửi / cập nhật đánh giá của mình | F2 / 2.1 | Người đã đăng nhập (vai trò tổng quát) | SG02 | 07 |
| P06 | Tra cứu sản phẩm và tồn kho | F2 / 2.2 | Nhân viên được cấp quyền | SG10 | 08 |
| P07 | Thêm nông sản | F2 / 2.2 | Nhân viên được cấp quyền | SG10 | 08 |
| P08 | Cập nhật nông sản và tồn kho | F2 / 2.2 | Nhân viên được cấp quyền | SG10 | 08 |
| P09 | Xóa nông sản | F2 / 2.2 | Nhân viên được cấp quyền | SG10 | 08 |
| P10 | Thêm danh mục | F2 / 2.3 | Nhân viên được cấp quyền | SG10 | 09 |
| P11 | Sửa danh mục | F2 / 2.3 | Nhân viên được cấp quyền | SG10 | 09 |
| P12 | Xóa danh mục | F2 / 2.3 | Nhân viên được cấp quyền | SG10 | 09 |
| P13 | Thêm nhà cung cấp | F2 / 2.4 | Nhân viên được cấp quyền | SG10 | 09 |
| P14 | Sửa nhà cung cấp | F2 / 2.4 | Nhân viên được cấp quyền | SG10 | 09 |
| P15 | Xóa nhà cung cấp | F2 / 2.4 | Nhân viên được cấp quyền | SG10 | 09 |
| P16 | Tra cứu và hiệu chỉnh đánh giá | F2 / 2.1 | Nhân viên được cấp quyền | SG10 | 08 |
| C01 | Xem giỏ hàng | F3 / 3.1 | Người đã đăng nhập (vai trò tổng quát) | SG03 | 10 |
| C02 | Thêm nông sản vào giỏ | F3 / 3.1 | Người đã đăng nhập (vai trò tổng quát) | SG03 | 10 |
| C03 | Thay đổi số lượng trong giỏ | F3 / 3.1 | Người đã đăng nhập (vai trò tổng quát) | SG03 | 10 |
| C04 | Xóa mặt hàng khỏi giỏ | F3 / 3.1 | Người đã đăng nhập (vai trò tổng quát) | SG03 | 10 |
| O01 | Đặt hàng từ giỏ | F3 / 3.2 | Người đã đăng nhập (vai trò tổng quát) | SG03 | 11 |
| O02 | Đặt hàng qua hội thoại | F3 / 3.2 | Người đã đăng nhập (vai trò tổng quát) | SG03 | 11 |
| O03 | Xem lịch sử đơn của mình | F3 / 3.3 | Người đã đăng nhập (vai trò tổng quát) | SG04 | 12 |
| O04 | Xem chi tiết đơn của mình | F3 / 3.3 | Người đã đăng nhập (vai trò tổng quát) | SG04 | 12 |
| O05 | Hủy đơn của mình | F3 / 3.4 | Người đã đăng nhập (vai trò tổng quát) | SG04 | 12 |
| O06 | Tra đơn của mình qua chat | F3 / 3.3 | Người đã đăng nhập (vai trò tổng quát) | SG04 | 12 |
| O07 | Tra cứu đơn toàn hệ thống | F3 / 3.4 | Nhân viên được cấp quyền | SG11 | 13 |
| O08 | Xác nhận đơn hàng | F3 / 3.4 | Nhân viên được cấp quyền | SG11 | 13 |
| O09 | Ghi nhận bắt đầu giao hàng | F3 / 3.4 | Nhân viên được cấp quyền | SG11 | 13 |
| O10 | Ghi nhận giao hàng thành công | F3 / 3.4 | Nhân viên được cấp quyền | SG11 | 13 |
| O11 | Hủy đơn chờ xác nhận của khách | F3 / 3.4 | Nhân viên được cấp quyền | SG11 | 13 |
| O12 | Xác nhận nhiều đơn đã chọn | F3 / 3.4 | Nhân viên được cấp quyền | SG11 | 13 |
| S01 | Hoàn tồn kho của đơn hủy | F3 / 3.4 | Được O05/O11 gọi | Hỗ trợ | 12, 13 |
| Q01 | Xem thông tin thanh toán VietQR | F4 / 4.1 | Người đã đăng nhập (vai trò tổng quát); Dịch vụ ảnh VietQR | SG05 | 14 |
| Q02 | Nộp / thay chứng từ chuyển khoản | F4 / 4.2 | Người đã đăng nhập (vai trò tổng quát) | SG05 | 14 |
| Q03 | Xem chứng từ thanh toán | F4 / 4.3 | Người đã đăng nhập (vai trò tổng quát); Nhân viên được cấp quyền | SG05 | 14, 15 |
| Q04 | Ghi nhận kết quả đối soát | F4 / 4.4 | Nhân viên được cấp quyền | SG12 | 15 |
| Q05 | Nộp chứng từ thay khách | F4 / 4.2 | Nhân viên được cấp quyền | SG12 | 15 |
| T01 | Duyệt / tìm kiếm lô hàng | F5 / 5.1 | Người truy cập (vai trò tổng quát) | SG06 | 16 |
| T02 | Xem nguồn gốc một lô | F5 / 5.1 | Người truy cập (vai trò tổng quát) | SG06 | 16 |
| T03 | Tra cứu lô hàng để quản trị | F5 / 5.2 | Nhân viên được cấp quyền | SG13 | 17 |
| T04 | Tạo lô nông sản | F5 / 5.2 | Nhân viên được cấp quyền | SG13 | 17 |
| T05 | Cập nhật thông tin lô | F5 / 5.2 | Nhân viên được cấp quyền | SG13 | 17 |
| T06 | Xóa lô nông sản | F5 / 5.2 | Nhân viên được cấp quyền | SG13 | 17 |
| T07 | Xem nhật ký nguồn gốc | F5 / 5.4 | Nhân viên được cấp quyền | SG13 | 17 |
| T08 | Hiệu chỉnh nhật ký nguồn gốc | F5 / 5.4 | Nhân viên được cấp quyền | SG13 | 17 |
| R01 | Xem gợi ý nông sản | F6 / 6.1 | Người truy cập (vai trò tổng quát) | SG07 | 07, 18 |
| R02 | Tra cứu khách theo nhóm hành vi | F6 / 6.2 | Nhân viên được cấp quyền | SG14 | 18 |
| R03 | Chạy cập nhật phân nhóm | F6 / 6.3 | Người vận hành có quyền CLI | SG16 | 18 |
| R04 | Tra cứu lịch sử phân nhóm | F6 / 6.4 | Nhân viên được cấp quyền | SG14 | 18 |
| R05 | Tra cứu nhật ký gợi ý | F6 / 6.4 | Nhân viên được cấp quyền | SG14 | 18 |
| H01 | Nhận tư vấn nông sản | F7 / 7.1 | Người truy cập (vai trò tổng quát); Dịch vụ AI Gemini/Groq | SG08 | 19 |
| H02 | Xem tin nhắn phiên hiện tại | F7 / 7.2 | Người truy cập (vai trò tổng quát) | SG08 | 19 |
| H03 | Xem lịch sử chat của mình | F7 / 7.2 | Người đã đăng nhập (vai trò tổng quát) | SG08 | 19 |
| H04 | Xóa hội thoại để bắt đầu lại | F7 / 7.3 | Người truy cập (vai trò tổng quát) | SG08 | 19 |
| H05 | Tra cứu phiên và tin nhắn chat | F7 / 7.4 | Nhân viên được cấp quyền | SG15 | 20 |
| D01 | Xem báo cáo điều hành | F8 / 8.1 | Nhân viên được cấp quyền | SG15 | 20 |
| D02 | Xuất báo cáo đơn hàng Excel | F8 / 8.3 | Nhân viên được cấp quyền | SG15 | 20 |
| D03 | Phân tích và tra cứu hành vi | F8 / 8.2 | Nhân viên được cấp quyền | SG15 | 20 |
| D04 | Hiệu chỉnh dữ liệu quản trị | F8 / 8.4 | Nhân viên được cấp quyền | SG15 | 20 |

## Kênh tương tác và độ phủ

| Kênh đã đọc | Use case |
|---|---|
| accounts: register, login, logout, profile | A01–A04 |
| Django Admin User / Group / UserAddress | A05–A11; quyền cấp nhóm A10 là chính sách đề xuất |
| products: list, search, detail, add_review | P01–P05; R01 được nhúng vào trang, không có endpoint riêng trong recommendation/urls.py |
| Dashboard products + Admin Product/Category/Supplier/ProductReview | P06–P16 |
| Cart, AddToCart, UpdateCartItem, RemoveCartItem | C01–C04 |
| Checkout, OrderHistory, OrderDetail, CancelOrder | O01, O03–O05; S01 qua dịch vụ hủy |
| chatbot:send + order_assistant / fallback | O02, O06, H01 |
| Dashboard orders/update_order_status + Admin Order/actions | O07–O12, Q03–Q05 |
| Thông tin VietQR trên chi tiết đơn + UploadPaymentProof | Q01–Q03 |
| traceability:trace_index, public_trace | T01–T02 |
| Dashboard traceability + Admin ProductBatch / TraceabilityRecord | T03–T08 |
| Home / ProductList / engine | R01 |
| Dashboard customers + Admin UserSegment / RecommendationLog | R02, R04, R05 |
| management command update_segments | R03 |
| chatbot:messages, history, clear + Admin ChatSession/ChatMessage | H02–H05 |
| Dashboard home, behavior, export_orders_excel | D01–D03 |
| Admin dữ liệu phụ trợ: phạm vi cụ thể trong đặc tả | D04 |

Các bảng dữ liệu, Django, thuật toán nội bộ, bộ lập lịch chưa cấu hình không phải tác nhân. Nhà cung cấp và người giao hàng không có kênh tương tác trong phạm vi mã nguồn đã đọc. Chuyển tiền thực tế diễn ra ngoài AgriSense; chỉ dịch vụ ảnh QR là tác nhân phần mềm tích hợp. Đây là độ phủ theo phạm vi dự án đang có, không phải cam kết bao trùm mọi yêu cầu chưa được cung cấp.
