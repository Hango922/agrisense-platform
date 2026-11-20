# AgriSense - Bộ sơ đồ chức năng và use case

Ngày đối chiếu: 12/11/2026. Mã nguồn tham chiếu: commit `92bdac6` và các file hiện có trong workspace.

## Mở bộ sơ đồ

- `AGRISENSE_USE_CASE_DAY_DU.drawio`: bản chính gồm 24 trang; trang mở đầu là sơ đồ phân rã phân cấp chức năng.
- `AGRISENSE_PHAN_CAP_CHUC_NANG.drawio`: bản riêng của trang 01.
- `AGRISENSE_USE_CASE_TONG_QUAT.drawio`: bản riêng của trang 02.
- Hai ảnh PNG cùng tên dùng để chèn vào báo cáo.

Sơ đồ phân cấp có 3 mức: hệ thống, 8 phân hệ, 32 nhóm chức năng con. Bộ use case có 112 mã mục tiêu/nghiệp vụ con; các mã lặp ở nhiều trang chỉ là tham chiếu đến cùng một nghiệp vụ.

## Mục lục

| Trang | Nội dung |
| --- | --- |
| 01 | PHÂN RÃ PHÂN CẤP CHỨC NĂNG |
| 02 | USE CASE TỔNG QUÁT TOÀN HỆ THỐNG |
| 03 | Tác nhân và quan hệ kế thừa |
| 04 | Tài khoản và hồ sơ |
| 05 | Khám phá và đánh giá nông sản |
| 06 | Giỏ hàng |
| 07 | Đặt hàng từ giỏ |
| 08 | Chi tiết nghiệp vụ tạo đơn |
| 09 | Theo dõi và hủy đơn |
| 10 | Thanh toán VietQR |
| 11 | Chat tư vấn |
| 12 | Chat đặt hàng |
| 13 | Chat lịch sử và tra cứu đơn |
| 14 | Truy xuất nguồn gốc công khai |
| 15 | Dashboard và báo cáo |
| 16 | Danh mục và tồn kho |
| 17 | Xử lý đơn quản trị |
| 18 | Đối soát thanh toán |
| 19 | Người dùng và phân quyền |
| 20 | Quản trị lô hàng |
| 21 | Hành vi và phân nhóm |
| 22 | Gợi ý cá nhân hóa |
| 23 | Quản trị dữ liệu hỗ trợ |
| 24 | Ký hiệu UML và hướng dẫn đọc |

## Tác nhân và quyền

| Tác nhân | Phạm vi |
| --- | --- |
| Khách vãng lai | Duyệt, tìm, xem sản phẩm; xem gợi ý phổ biến; đăng ký/đăng nhập; truy xuất nguồn gốc; chat tư vấn và quản lý phiên chat của mình. |
| Khách hàng đã đăng nhập | Chức năng công khai, hồ sơ/sổ địa chỉ, đánh giá, giỏ, đặt hàng, xem/hủy đơn cá nhân, VietQR/bill, lịch sử chat và đặt hàng qua chat. |
| Nhân viên | Dashboard yêu cầu active + is_staff. Các thao tác Django Admin cần thêm quyền model tương ứng. Tài khoản cũng có thể sử dụng chức năng mua sắm. |
| Quản trị viên | Nhân viên có is_superuser; kế thừa quyền nhân viên và toàn quyền quản trị. |
| Người vận hành | Có quyền chạy lệnh trên máy chủ; chạy update_segments. Quyền này không tự sinh từ cờ is_staff của tài khoản web. |
| API AI Gemini/Groq | Cung cấp phản hồi tư vấn khi nhà cung cấp được cấu hình và khả dụng. |
| Dịch vụ ảnh VietQR | Cung cấp ảnh QR ngân hàng chứa thông tin thanh toán theo đơn. |

Nhà cung cấp đang là dữ liệu do quản trị quản lý. Mã nguồn chưa có cổng đăng nhập nhà cung cấp hoặc shipper, chưa tích hợp callback ngân hàng. Do đó những đối tượng này không được gán các thao tác trực tiếp lên phần mềm trong sơ đồ hiện trạng. Thuật toán RFM, gợi ý và fallback là thành phần nội bộ, không phải tác nhân ngoài.

## Quy tắc mô hình hóa

- Phân cấp chức năng: đường nối thể hiện quan hệ cha - con, không thể hiện trình tự thời gian.
- Use case: tác nhân ở ngoài biên AgriSense; hình bầu dục là mục tiêu hoặc nghiệp vụ con.
- Include: hướng từ use case gốc đến phần bắt buộc trong luồng thành công.
- Extend: hướng từ phần mở rộng về use case gốc; điều kiện được ghi trên cạnh.
- Kế thừa tác nhân: tam giác rỗng hướng về vai trò tổng quát.
- Đăng nhập được ghi làm tiền điều kiện ở chức năng cần xác thực, không lặp include đăng nhập ở mọi mục.
- Trang tổng quát gom chức năng để nhìn toàn bài; quyền và điều kiện cụ thể xem trang phân rã.

## Điều kiện nghiệp vụ quan trọng

1. Giỏ và các trang đơn của khách được giới hạn theo chủ sở hữu. Thêm giỏ chưa trừ kho. Tạo đơn thành công mới lưu các mặt hàng, đơn giá, trừ kho và đặt trạng thái pending.
2. Đơn từ giỏ cần giỏ không rỗng và đủ tồn kho. Phí giao hàng 30.000đ; tiền hàng từ 500.000đ miễn phí. Giỏ được xóa sau khi tạo đơn thành công.
3. Chat đặt trực tiếp không đi qua giỏ; hiện chọn sản phẩm khớp đầu tiên, một loại sản phẩm cho mỗi đơn chat. Có đủ thông tin nhận và phương thức có thể tạo ngay. Có thể bổ sung/sửa thông tin nhận hoặc hủy nháp trong hội thoại.
4. Khách chỉ hủy đơn pending, hệ thống hoàn kho. Hủy đơn không đồng nghĩa với hoàn tiền qua ngân hàng.
5. Khách tải/thay bill khi đơn pending. Bill và thời gian tải được lưu; việc tải bill không xác nhận tiền thực tế đã vào tài khoản.
6. VietQR là hỗ trợ thanh toán bằng ảnh QR. Đối soát do người quản trị thực hiện; không có webhook ngân hàng. Có thể dùng bill khách gửi, tải bill thay khách hoặc tạo chứng từ nội bộ khi quản trị xác nhận.
7. Giao diện quản trị có luồng pending → confirmed → shipping → delivered. Backend chưa khóa mọi chuyển trạng thái; hủy sau pending hiện không tự hoàn kho. Các giới hạn này được ghi ngay trên sơ đồ.
8. Đánh giá cần đăng nhập; mỗi người một đánh giá/sản phẩm, gửi lại cập nhật bản cũ. Chưa có kiểm tra phải mua sản phẩm trước.
9. Xem hồ sơ và địa chỉ có ở giao diện khách; chỉnh sửa tài khoản/địa chỉ hiện qua Django Admin. Chưa có luồng tự phục vụ sửa hồ sơ/địa chỉ hoặc quên mật khẩu ở storefront.
10. QR nguồn gốc được sinh khi lưu lô chưa có QR. Trang công khai hiển thị thông tin lô và lịch sử đã có. Chưa có cơ chế tự ghi tất cả thay đổi lô vào bảng lịch sử.
11. Chat lưu tin nhắn và phản hồi theo tài khoản hoặc session khách. Xóa hội thoại cũng xóa đơn nháp. Trang lịch sử tài khoản yêu cầu đăng nhập.
12. Nhánh fallback tra đơn bằng mã hiện chưa kiểm tra chủ đơn; đây là giới hạn phân quyền của hiện trạng, không phải quy tắc nghiệp vụ nên duy trì.
13. Hành vi view, search, add_to_cart, review và purchase từ checkout được ghi trong các view/middleware. Đặt trực tiếp qua chat hiện chưa ghi purchase. Loại sự kiện chat có trong model/thống kê nhưng chưa thấy điểm ghi UserEvent chat trong ChatbotAPIView.
14. update_segments là management command; chưa có cấu hình lịch chạy định kỳ trong dự án. Vòng cập nhật hiện xét tất cả tài khoản active, kể cả tài khoản nhân viên.
15. Dashboard doanh thu 30 ngày loại đơn hủy, không chỉ tính đơn đã giao; trang quản trị đơn có chỉ tiêu riêng cho đơn delivered. Excel xuất toàn bộ đơn, không theo bộ lọc hiện tại.
16. Các bảng RecommendationLog và TraceabilityRecord có quản trị dữ liệu; không suy ra rằng thuật toán hiện tự ghi đầy đủ các nhật ký này.

## Quy tắc phân nhóm thực tế

Áp dụng theo thứ tự trong `apps/behavior/segmentation.py`; đơn tính là đơn không cancelled.

| Điều kiện | Nhóm |
| --- | --- |
| Chưa có đơn và đăng ký trong 7 ngày | new |
| Chưa có đơn, đăng ký trước 7 ngày và từ 5 sự kiện | interested |
| Chưa có đơn và chưa thỏa hai nhánh trên | new |
| Có từ 3 đơn trong 30 ngày | loyal |
| Có đơn, đơn gần nhất cũ hơn 30 ngày | at_risk |
| Còn lại | normal |

Chỉ lưu UserSegment mới khi nhãn nhóm thay đổi.

## Quy tắc gợi ý thực tế

Hành vi 30 ngày có trọng số: view=1, search=2, add_to_cart=3, purchase=5, review=4. Hành vi phải gắn danh mục hoặc sản phẩm để đóng góp vào vector. Nếu không có vector hoặc tổng điểm dưới 3, dùng sản phẩm bán chạy/mới nhất. Nhánh cá nhân hóa ưu tiên tối đa 3 danh mục, loại sản phẩm đã mua và chỉ lấy hàng active còn kho. Nhánh này hiện chưa tự bù kết quả thiếu bằng dự phòng. Sản phẩm mua trong đơn hủy vẫn bị loại do truy vấn purchased_ids chưa lọc trạng thái.

## Bảng đối chiếu mã use case

| Mã | Mục tiêu / nghiệp vụ con | Trang |
| --- | --- | --- |
| A01 | Đăng ký tài khoản | 04 |
| A02 | Đăng nhập | 04 |
| A03 | Đăng xuất | 04 |
| A04 | Xem hồ sơ cá nhân | 04 |
| A05 | Xem sổ địa chỉ nhận hàng | 04 |
| A06 | Kiểm tra dữ liệu đăng ký | 04 |
| A07 | Xác thực tài khoản | 04 |
| B01 | Ghi nhận lượt tìm kiếm | 05 |
| B02 | Ghi nhận lượt xem | 05 |
| B03 | Ghi nhận đánh giá | 05 |
| B04 | Ghi nhận thêm vào giỏ | 06 |
| B05 | Xem thống kê hành vi 30 ngày | 21 |
| B06 | Tìm / lọc sự kiện gần nhất | 21 |
| B07 | Chạy cập nhật phân nhóm | 21 |
| B08 | Phân loại tài khoản đang active | 21 |
| B09 | Lưu nhóm và lịch sử thay đổi | 21 |
| B10 | Quản lý sự kiện / lịch sử nhóm | 21 |
| B11 | Ghi nhận hành vi mua hàng | 08 |
| C01 | Xem giỏ hàng và tạm tính | 06 |
| C02 | Thêm sản phẩm vào giỏ | 06 |
| C03 | Cập nhật số lượng | 06 |
| C04 | Xóa mặt hàng khỏi giỏ | 06 |
| C05 | Kiểm tra tồn kho | 06, 08 |
| D01 | Xem KPI tổng quan 30 ngày | 15 |
| D02 | Xem biểu đồ doanh thu | 15 |
| D03 | Xem cơ cấu nhóm khách hàng | 15 |
| D04 | Xem sản phẩm bán chạy | 15 |
| D05 | Xuất báo cáo đơn hàng Excel | 15 |
| D06 | Tìm / lọc và xem đơn hàng | 17 |
| D07 | Xác nhận đơn hàng | 17 |
| D08 | Chuyển đơn sang đang giao | 17 |
| D09 | Đánh dấu đã giao hàng | 17 |
| D10 | Hủy đơn hàng | 17 |
| D11 | Duyệt nhiều đơn đã chọn | 18 |
| D12 | Đáp ứng điều kiện bill | 17, 18 |
| D13 | Dùng bill khách đã nộp | 18 |
| D14 | Tải bill thay khách | 18 |
| D15 | Xác nhận đã đối soát thủ công | 18 |
| D16 | Sinh chứng từ đối soát nội bộ | 18 |
| H01 | Hỏi đáp và tư vấn nông sản | 11 |
| H02 | Nhận tư vấn qua LLM | 11 |
| H03 | Nhận trả lời theo luật | 11 |
| H04 | Lưu tin nhắn / phản hồi | 11 |
| H05 | Xem lại tin nhắn phiên hiện tại | 11 |
| H06 | Xóa hội thoại, bắt đầu lại | 11 |
| H07 | Xóa đơn nháp đang soạn | 11 |
| H08 | Xem lịch sử chat của tài khoản | 13 |
| H09 | Đặt nông sản qua chat | 12, 13 |
| H10 | Nhận diện sản phẩm / số lượng | 12 |
| H11 | Bổ sung thông tin nhận hàng | 12 |
| H12 | Chọn phương thức thanh toán | 12 |
| H13 | Hủy yêu cầu đặt hàng nháp | 12 |
| H14 | Hỏi thông tin đơn theo mã | 13 |
| H15 | Hỏi đơn gần nhất của mình | 13 |
| H16 | Sửa thông tin nhận trong nháp | 13 |
| M01 | Theo dõi và tìm / lọc tồn kho | 16 |
| M02 | Quản lý sản phẩm | 16 |
| M03 | Quản lý danh mục sản phẩm | 16 |
| M04 | Quản lý nhà cung cấp | 16 |
| M05 | Quản lý đánh giá sản phẩm | 16 |
| M06 | Sửa giá, ảnh, kho, bật / tắt bán | 16 |
| O01 | Đặt hàng từ giỏ | 07, 08 |
| O02 | Cung cấp thông tin nhận hàng | 07 |
| O03 | Chọn COD hoặc VietQR | 07 |
| O04 | Kiểm tra giỏ và tồn kho | 07 |
| O05 | Tính tiền và phí giao hàng | 07, 08 |
| O06 | Tạo đơn và trừ tồn kho | 07, 08, 12 |
| O07 | Xem lịch sử đơn hàng | 09 |
| O08 | Xem chi tiết và trạng thái | 09, 10 |
| O09 | Hủy đơn chờ xác nhận | 09 |
| O10 | Hoàn trả tồn kho | 09, 17 |
| O11 | Lưu mã đơn, người nhận, mục đơn | 08 |
| O12 | Cập nhật số lượng tồn kho | 08 |
| P01 | Xem trang chủ | 05 |
| P02 | Duyệt danh sách sản phẩm | 05 |
| P03 | Tìm kiếm nông sản | 05 |
| P04 | Xem chi tiết nông sản | 05 |
| P05 | Gửi / sửa đánh giá của mình | 05 |
| P06 | Lọc danh mục / khoảng giá | 05 |
| Q01 | Xem thông tin / mã VietQR | 09, 10, 13 |
| Q02 | Hiển thị ảnh QR theo đơn | 10 |
| Q03 | Xem ảnh bill đã nộp | 10 |
| Q04 | Tải lên / thay bill chuyển khoản | 10 |
| Q05 | Lưu bill và thời điểm nộp | 10 |
| R01 | Xem gợi ý nông sản | 05, 22 |
| R02 | Gợi ý theo sở thích danh mục | 22 |
| R03 | Gợi ý bán chạy / mới nhất | 22 |
| R04 | Tính trọng số hành vi | 22 |
| R05 | Lọc sản phẩm đã mua | 22 |
| R06 | Chọn hàng đang bán và còn kho | 22 |
| T01 | Duyệt danh sách lô hàng | 14 |
| T02 | Tìm lô theo mã / sản phẩm / vùng | 14 |
| T03 | Xem hộ chiếu nông sản | 09, 14 |
| T04 | Xem nguồn gốc, chứng nhận | 14 |
| T05 | Xem ngày thu hoạch / đóng gói | 14 |
| T06 | Xem lịch sử thay đổi lô | 14 |
| T07 | Theo dõi / tìm / lọc lô hàng | 20 |
| T08 | Tạo lô hàng mới | 20 |
| T09 | Sửa thông tin / chứng nhận lô | 20 |
| T10 | Xóa lô hàng | 20 |
| T11 | Quản lý lịch sử truy xuất | 20 |
| T12 | Sinh ảnh QR trỏ tới lô | 20 |
| U01 | Tìm / lọc khách theo nhóm | 19 |
| U02 | Thêm / sửa / xóa tài khoản | 19 |
| U03 | Đổi mật khẩu / khóa tài khoản | 19 |
| U04 | Quản lý nhóm và quyền truy cập | 19 |
| U05 | Quản lý sổ địa chỉ của khách | 19 |
| X01 | Quản trị giỏ hàng / xem mục giỏ | 23 |
| X02 | Quản trị đơn / xem mục đơn | 23 |
| X03 | Quản trị phiên hội thoại | 23 |
| X04 | Quản trị / tìm / lọc tin nhắn | 23 |
| X05 | Quản trị nhật ký gợi ý | 23 |

## Nguồn đối chiếu theo phân hệ

| Phân hệ | Nguồn chính |
| --- | --- |
| TÀI KHOẢN VÀ HỒ SƠ | apps/accounts/views.py · forms.py · urls.py · templates/accounts/profile.html |
| DUYỆT, TÌM KIẾM VÀ ĐÁNH GIÁ | apps/products/views.py · apps/behavior/middleware.py · templates/products/* |
| GIỎ HÀNG CÁ NHÂN | apps/cart_orders/views.py · models.py · templates/cart_orders/cart.html |
| ĐẶT HÀNG TỪ GIỎ | apps/cart_orders/views.py:CheckoutView · services.py:create_order_from_cart |
| ĐƠN HÀNG CỦA KHÁCH HÀNG | apps/cart_orders/views.py · services.py:cancel_order · templates/cart_orders/order_detail.html |
| HỖ TRỢ THANH TOÁN VIETQR | apps/cart_orders/vietqr.py · views.py:UploadPaymentProofView · templates/cart_orders/order_detail.html |
| HỘI THOẠI VÀ TƯ VẤN NÔNG SẢN | apps/chatbot/views.py · services.py · fallback.py · static/js/chatbot.js |
| ĐẶT HÀNG BẰNG HỘI THOẠI | apps/chatbot/order_assistant.py:handle_order_conversation · apps/cart_orders/services.py:create_direct_order |
| CHAT: LỊCH SỬ, TRA CỨU VÀ ĐƠN NHÁP | apps/chatbot/views.py:ChatHistoryView · fallback.py:get_fallback_response · order_assistant.py |
| TRUY XUẤT NGUỒN GỐC CÔNG KHAI | apps/traceability/views.py · urls.py · templates/traceability/* |
| ĐIỀU HÀNH KINH DOANH | apps/dashboard/views.py:DashboardHomeView,ExportOrdersExcelView · templates/dashboard/index.html |
| QUẢN TRỊ NÔNG SẢN VÀ TỒN KHO | apps/dashboard/views.py:DashboardProductsView · apps/products/admin.py |
| QUẢN TRỊ VÀ THỰC HIỆN ĐƠN HÀNG | apps/dashboard/views.py:DashboardOrdersView,DashboardUpdateOrderStatusView · templates/dashboard/orders.html |
| ĐỐI SOÁT BILL VÀ DUYỆT ĐƠN | apps/dashboard/views.py:DashboardUpdateOrderStatusView · apps/cart_orders/admin.py · services.py |
| QUẢN TRỊ TÀI KHOẢN VÀ ĐỊA CHỈ | apps/accounts/admin.py · models.py · apps/dashboard/views.py:DashboardCustomersView · Django auth admin |
| LÔ HÀNG, MÃ QR VÀ NHẬT KÝ | apps/traceability/admin.py · models.py:ProductBatch.save · qr_generator.py · apps/dashboard/views.py |
| PHÂN TÍCH HÀNH VI VÀ PHÂN NHÓM | apps/dashboard/views.py:DashboardBehaviorView · apps/behavior/segmentation.py · management/commands/update_segments.py |
| GỢI Ý NÔNG SẢN | apps/recommendation/engine.py · apps/products/views.py:HomeView |
| QUẢN TRỊ DỮ LIỆU VÀ GIÁM SÁT AI | apps/cart_orders/admin.py · apps/chatbot/admin.py · apps/behavior/admin.py |
| NGHIỆP VỤ TẠO ĐƠN DÙNG CHUNG | apps/cart_orders/services.py:create_order_from_cart,create_direct_order · views.py:CheckoutView |

Phạm vi của bộ sơ đồ là chức năng được thể hiện trong mã nguồn và các giao diện quản trị đã đăng ký. Các hạn chế hiện trạng được giữ rõ ràng, không bổ sung giả định như xác nhận ngân hàng tự động, hoàn tiền, mã giảm giá, giỏ khách vãng lai, tích hợp vận chuyển hoặc cổng nhà cung cấp.

## Kiểm tra tệp

Đã kiểm tra thứ tự: phân cấp chức năng ở trang 01, use case toàn hệ thống ở trang 02; cấu trúc XML có 24 trang, không trùng ID trong trang và không có cạnh trỏ tới ô không tồn tại. Sơ đồ được tạo, chỉnh sửa và xuất bằng công cụ draw.io.
