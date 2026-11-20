# Đặc tả use case AgriSense — phiên bản 2.0

Ngày rà soát: 13/11/2026. Đi kèm bộ draw.io 21 trang, 70 mục tiêu nghiệp vụ và 1 use case hỗ trợ S01.

## 1. Phạm vi và cách đọc

Đây là mô hình nghiệp vụ đề xuất được đối chiếu với mã nguồn hiện có. Các từ “phải”, “chỉ”, “đúng một lần” mô tả yêu cầu đích; không đồng nghĩa mã hiện tại đã cưỡng chế đầy đủ. Đọc `DOI_CHIEU_HIEN_THUC.md` trước khi khẳng định một hành vi đã triển khai. Không có thay đổi mã ứng dụng trong lần sửa tài liệu này.

Mỗi mã có một nhóm F1–F8 sở hữu. Các mã lặp trên nhiều trang là cùng một use case. Nhóm SG trên trang tổng quát là mức khái quát; bảng phân rã ở `MA_TRAN_TRUY_VET.md` ánh xạ đủ 70 mục tiêu. S01 là hỗ trợ, không đếm là mục tiêu độc lập.

## 2. Tác nhân và phân quyền

| Mã | Tác nhân | Trách nhiệm / điều kiện |
|---|---|---|
| V | Người truy cập | Vai trò tổng quát cho chức năng công khai |
| G | Khách vãng lai | Chưa đăng nhập; kế thừa V |
| U | Người đã đăng nhập | Vai trò tổng quát; kế thừa V; thao tác dữ liệu cá nhân phải kiểm tra sở hữu |
| C | Khách hàng | Kế thừa U; mua sắm và theo dõi đơn của mình |
| S | Nhân viên được cấp quyền | Kế thừa U; active + is_staff và quyền nghiệp vụ/model phù hợp |
| A | Quản trị viên | Kế thừa S; superuser; A10 dành cho quản trị viên theo chính sách mô hình |
| O | Người vận hành | Có quyền chạy CLI và truy cập môi trường; không tự suy ra từ quyền staff |
| L | Dịch vụ AI | Gemini/Groq được cấu hình; hỗ trợ tư vấn |
| Q | Dịch vụ ảnh VietQR | Cấp ảnh QR theo thông tin chuyển khoản, không xác nhận tiền |

Kế thừa actor biểu thị khả năng tham gia, không cấp quyền truy cập dữ liệu một cách tự động. Admin có các khả năng của staff; staff vẫn dùng chức năng công khai/cá nhân khi đủ tiền điều kiện. Nhóm quyền Django khác nhóm hành vi new/interested/normal/loyal/at_risk.

## 3. Danh mục và hợp đồng của 71 mã

| Mã | Mục tiêu | Tác nhân | Tiền điều kiện | Hậu điều kiện thành công |
|---|---|---|---|---|
| A01 | Đăng ký tài khoản | G | Chưa có tài khoản mang tên đăng nhập đó | Tài khoản hợp lệ được tạo, đăng nhập tự động |
| A02 | Đăng nhập | V | Có tài khoản đang hoạt động; có thông tin xác thực | Phiên được xác thực và điều hướng theo vai trò |
| A03 | Đăng xuất | U | Có phiên đăng nhập | Phiên xác thực kết thúc |
| A04 | Xem hồ sơ và sổ địa chỉ | U | Đã đăng nhập | Hiển thị hồ sơ, phân nhóm và địa chỉ của chính mình |
| A05 | Thêm tài khoản người dùng | S | Quyền thêm User | Tạo tài khoản hợp lệ |
| A06 | Sửa thông tin người dùng | S | Quyền sửa User; tài khoản tồn tại | Lưu thông tin đã kiểm tra |
| A07 | Khóa / mở khóa tài khoản | S | Quyền sửa User; tài khoản tồn tại | Đổi is_active theo yêu cầu |
| A08 | Đặt lại mật khẩu người dùng | S | Quyền quản trị mật khẩu của User mục tiêu | Lưu mật khẩu mới dạng băm |
| A09 | Xóa tài khoản người dùng | S | Quyền xóa User; đã kiểm tra liên kết dữ liệu | Xóa theo ràng buộc quan hệ hoặc từ chối rõ lý do |
| A10 | Phân nhóm và cấp quyền truy cập | A | Quản trị viên; đã xác định vai trò cần cấp | Lưu nhóm và quyền truy cập đã chọn |
| A11 | Cập nhật sổ địa chỉ của khách | S | Quyền UserAddress theo thao tác; khách tồn tại | Sổ địa chỉ của đúng khách được cập nhật |
| P01 | Duyệt nông sản đang bán | V | Không cần đăng nhập | Hiển thị nông sản đang bán và còn hàng |
| P02 | Lọc nông sản | V | Đang duyệt P01; người xem yêu cầu lọc | Danh sách đáp ứng bộ lọc hoặc rỗng |
| P03 | Tìm kiếm nông sản | V | Có truy vấn tìm kiếm | Trả kết quả theo tên, mô tả hoặc xuất xứ |
| P04 | Xem chi tiết nông sản | V | Sản phẩm có thể truy cập theo chính sách công khai | Hiển thị thông tin, đánh giá; ghi sự kiện xem |
| P05 | Gửi / cập nhật đánh giá của mình | U | Đã đăng nhập; sản phẩm tồn tại; nội dung hợp lệ | Tạo/cập nhật một đánh giá của mình cho sản phẩm |
| P06 | Tra cứu sản phẩm và tồn kho | S | Quyền xem dữ liệu sản phẩm quản trị | Hiển thị kết quả tra cứu và tồn kho |
| P07 | Thêm nông sản | S | Quyền thêm Product; danh mục/nhà cung cấp phù hợp | Sản phẩm mới được lưu |
| P08 | Cập nhật nông sản và tồn kho | S | Quyền sửa Product; sản phẩm tồn tại | Lưu thông tin, giá, ảnh, tồn kho hoặc trạng thái bán |
| P09 | Xóa nông sản | S | Quyền xóa Product; xem trước ảnh hưởng liên kết | Xóa hợp lệ hoặc báo quan hệ ngăn xóa |
| P10 | Thêm danh mục | S | Quyền thêm Category | Danh mục mới được lưu |
| P11 | Sửa danh mục | S | Quyền sửa Category; danh mục tồn tại | Thông tin danh mục được cập nhật |
| P12 | Xóa danh mục | S | Quyền xóa Category; kiểm tra quan hệ sản phẩm | Xóa hợp lệ hoặc từ chối có lý do |
| P13 | Thêm nhà cung cấp | S | Quyền thêm Supplier | Nhà cung cấp mới được lưu |
| P14 | Sửa nhà cung cấp | S | Quyền sửa Supplier; bản ghi tồn tại | Thông tin nhà cung cấp được cập nhật |
| P15 | Xóa nhà cung cấp | S | Quyền xóa Supplier; kiểm tra quan hệ liên quan | Xóa hợp lệ hoặc từ chối có lý do |
| P16 | Tra cứu và hiệu chỉnh đánh giá | S | Quyền xem/sửa/xóa ProductReview tương ứng | Hiển thị hoặc hiệu chỉnh đúng đánh giá |
| C01 | Xem giỏ hàng | U | Đã đăng nhập | Hiển thị giỏ của mình và tổng tiền dự kiến |
| C02 | Thêm nông sản vào giỏ | U | Đã đăng nhập; sản phẩm đang bán; số lượng nguyên dương | Giỏ tăng số lượng, không trừ tồn kho |
| C03 | Thay đổi số lượng trong giỏ | U | Mặt hàng thuộc giỏ của mình; đầu vào số lượng hợp lệ | Số lượng cập nhật hoặc mặt hàng bị bỏ nếu không dương |
| C04 | Xóa mặt hàng khỏi giỏ | U | Mặt hàng thuộc giỏ của mình | Mặt hàng được bỏ khỏi giỏ |
| O01 | Đặt hàng từ giỏ | U | Đã đăng nhập; giỏ không rỗng; thông tin nhận hàng hợp lệ | Tạo đơn pending, chụp giá, trừ kho và làm rỗng giỏ |
| O02 | Đặt hàng qua hội thoại | U | Đã đăng nhập; có yêu cầu đặt hàng | Tạo đơn trực tiếp pending khi đủ dữ liệu; kết thúc bản nháp |
| O03 | Xem lịch sử đơn của mình | U | Đã đăng nhập | Chỉ hiển thị lịch sử đơn của mình |
| O04 | Xem chi tiết đơn của mình | U | Đã đăng nhập; đơn thuộc mình | Hiển thị chi tiết đúng đơn |
| O05 | Hủy đơn của mình | U | Đã đăng nhập; đơn của mình đang pending | Đơn cancelled và S01 hoàn tồn kho đúng một lần |
| O06 | Tra đơn của mình qua chat | U | Đã đăng nhập; mã đơn hoặc yêu cầu đơn gần nhất thuộc mình | Trả dữ liệu đơn được phép xem, không lộ đơn người khác |
| O07 | Tra cứu đơn toàn hệ thống | S | Nhân viên có quyền xem đơn | Hiển thị kết quả tra cứu đơn toàn hệ thống |
| O08 | Xác nhận đơn hàng | S | Quyền xử lý đơn; đơn pending; VietQR đã đối soát nếu áp dụng | Đơn chuyển confirmed |
| O09 | Ghi nhận bắt đầu giao hàng | S | Quyền xử lý đơn; đơn confirmed | Đơn chuyển shipping |
| O10 | Ghi nhận giao hàng thành công | S | Quyền xử lý đơn; đơn shipping; có thông tin giao thành công | Đơn chuyển delivered |
| O11 | Hủy đơn chờ xác nhận của khách | S | Quyền hủy đơn; đơn pending | Đơn cancelled và hoàn tồn kho đúng một lần |
| O12 | Xác nhận nhiều đơn đã chọn | S | Quyền xác nhận đơn; đã chọn danh sách | Chỉ đơn đủ điều kiện được xác nhận; có kết quả từng đơn |
| S01 | Hoàn tồn kho của đơn hủy | O05/O11 gọi | O05/O11 đã kiểm tra đơn pending; đang trong giao dịch hủy | Hoàn đúng số lượng đã trừ, đồng bộ trạng thái cancelled |
| Q01 | Xem thông tin thanh toán VietQR | U, Q | Đã đăng nhập; đơn VietQR thuộc mình | Hiển thị ngân hàng, tài khoản, số tiền, nội dung và ảnh QR khi có |
| Q02 | Nộp / thay chứng từ chuyển khoản | U | Đơn VietQR của mình đang pending; chứng từ hợp lệ | Lưu/thay chứng từ và thời điểm; không tự xác nhận đã nhận tiền |
| Q03 | Xem chứng từ thanh toán | U, S | Là chủ đơn hoặc nhân viên có quyền xem chứng từ | Hiển thị chứng từ được phép hoặc trạng thái chưa có |
| Q04 | Ghi nhận kết quả đối soát | S | Nhân viên có quyền đối soát; đơn VietQR; kiểm tra ngân hàng thực tế | Ghi nhận kết quả đối soát để quyết định xác nhận đơn |
| Q05 | Nộp chứng từ thay khách | S | Nhân viên có quyền; đơn VietQR pending; chứng từ hợp lệ | Lưu chứng từ thay khách; chưa mặc nhiên xác nhận tiền |
| T01 | Duyệt / tìm kiếm lô hàng | V | Không cần đăng nhập | Hiển thị các lô phù hợp điều kiện tra cứu |
| T02 | Xem nguồn gốc một lô | V | Có mã lô hợp lệ hoặc URL từ QR | Hiển thị nguồn gốc và lịch sử đã ghi nhận của lô |
| T03 | Tra cứu lô hàng để quản trị | S | Quyền xem ProductBatch | Hiển thị các lô trong phạm vi quản trị |
| T04 | Tạo lô nông sản | S | Quyền thêm ProductBatch; sản phẩm tồn tại; mã lô duy nhất | Tạo lô với dữ liệu hợp lệ và QR truy xuất |
| T05 | Cập nhật thông tin lô | S | Quyền sửa ProductBatch; lô tồn tại | Lưu thông tin lô và bảo đảm QR trỏ đúng mã hiện hành |
| T06 | Xóa lô nông sản | S | Quyền xóa ProductBatch; kiểm tra lịch sử liên quan | Xóa lô theo ràng buộc hoặc từ chối |
| T07 | Xem nhật ký nguồn gốc | S | Quyền xem TraceabilityRecord | Hiển thị nhật ký hiện có; không suy diễn lịch sử chưa ghi |
| T08 | Hiệu chỉnh nhật ký nguồn gốc | S | Quyền thêm/sửa/xóa TraceabilityRecord tương ứng | Bản ghi nhật ký được hiệu chỉnh theo thao tác |
| R01 | Xem gợi ý nông sản | V | Truy cập khu vực gợi ý | Trả nông sản còn hàng theo cá nhân hóa hoặc phương án dự phòng |
| R02 | Tra cứu khách theo nhóm hành vi | S | Quyền xem khách và phân nhóm | Hiển thị khách phù hợp nhóm/từ khóa |
| R03 | Chạy cập nhật phân nhóm | O | Có quyền vận hành CLI và truy cập CSDL | Phân loại người dùng active; ghi lịch sử khi nhóm thay đổi |
| R04 | Tra cứu lịch sử phân nhóm | S | Quyền xem UserSegment | Hiển thị lịch sử phân nhóm hiện có |
| R05 | Tra cứu nhật ký gợi ý | S | Quyền xem RecommendationLog | Hiển thị nhật ký gợi ý đã có |
| H01 | Nhận tư vấn nông sản | V, L | Có phiên trình duyệt và câu hỏi hợp lệ | Trả lời tư vấn; lưu hội thoại theo phạm vi phiên |
| H02 | Xem tin nhắn phiên hiện tại | V | Có phiên hiện tại | Hiển thị tin nhắn đúng phiên |
| H03 | Xem lịch sử chat của mình | U | Đã đăng nhập | Hiển thị các hội thoại thuộc tài khoản |
| H04 | Xóa hội thoại để bắt đầu lại | V | Có phiên hội thoại hiện tại | Xóa hội thoại và bản nháp đặt hàng tương ứng |
| H05 | Tra cứu phiên và tin nhắn chat | S | Quyền xem ChatSession/ChatMessage | Trả các phiên/tin nhắn theo bộ lọc quản trị |
| D01 | Xem báo cáo điều hành | S | Quyền xem báo cáo điều hành | Hiển thị KPI với đúng định nghĩa và kỳ tính |
| D02 | Xuất báo cáo đơn hàng Excel | S | Quyền xuất báo cáo đơn hàng | Trả tệp Excel toàn bộ đơn, không ngầm dùng bộ lọc màn hình |
| D03 | Phân tích và tra cứu hành vi | S | Quyền xem UserEvent/báo cáo hành vi | Trả tổng hợp và bản ghi hành vi có sẵn |
| D04 | Hiệu chỉnh dữ liệu quản trị | S | Quyền model và thao tác cụ thể; theo bảng phạm vi bảo trì | Chỉ hiệu chỉnh dữ liệu phụ trợ được phép; giữ ràng buộc nghiệp vụ |

## 4. Quy tắc chung của luồng

- Kiểm tra xác thực, quyền thao tác và quyền đối với đối tượng ở phía máy chủ. Ẩn nút không thay thế kiểm tra quyền.
- Với dữ liệu cá nhân: truy vấn theo tài khoản/phiên, không chỉ theo ID hoặc mã đơn do người dùng gửi.
- Đầu vào không hợp lệ hoặc không đủ quyền: không thay đổi dữ liệu nghiệp vụ; trả lỗi có thể hiểu được và không tiết lộ dữ liệu của người khác.
- Lỗi trong giao dịch tạo/hủy đơn: không để trạng thái đơn và kho cập nhật dở dang. Mã hiện tại có điểm chưa bảo đảm, liệt kê riêng.
- Các luồng tra cứu không thay đổi dữ liệu nghiệp vụ; có thể ghi sự kiện xem/tìm nếu được mô tả. Lịch sử/nhật ký chỉ phản ánh bản ghi thực sự tồn tại.
- Nếu một mục dưới đây chứa nhiều mã, mỗi mã có kích hoạt riêng; không bắt buộc người dùng thực hiện toàn bộ các bước của các mã khác.
- Một sơ đồ use case mô tả ai đạt mục tiêu nào, không mô tả thứ tự thời gian; thứ tự và điều kiện nằm trong đặc tả này.

## 5. Luồng chi tiết

### 5.1. A01 — Đăng ký tài khoản

**Kích hoạt:** Khách chọn đăng ký.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. Khách nhập tên đăng nhập, mật khẩu, xác nhận mật khẩu và thông tin biểu mẫu.
2. Hệ thống kiểm tra trường bắt buộc, tên đăng nhập duy nhất và chính sách mật khẩu.
3. Hệ thống tạo tài khoản khách, lưu mật khẩu dạng băm.
4. Hệ thống đăng nhập tự động và chuyển về trang chủ.

**Luồng thay thế / ngoại lệ:**

- 2a. Trùng tên, mật khẩu yếu hoặc không khớp: hiển thị lỗi, giữ các trường không nhạy cảm để sửa; chưa tạo tài khoản.
- 3a. Lưu thất bại: thông báo lỗi; không thông báo đăng ký thành công.

**Quy tắc và giới hạn:** Đăng ký không tự cấp is_staff/is_superuser. Đăng nhập tự động là bước của A01, không cần include A02.

### 5.2. A02 / A03 / A04 — Đăng nhập

**Kích hoạt:** Người truy cập chọn đăng nhập; người đã đăng nhập chọn đăng xuất hoặc hồ sơ.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. A02: nhập tên đăng nhập/mật khẩu; hệ thống xác thực tài khoản còn hoạt động.
2. A02: tạo phiên; ưu tiên URL chuyển tiếp hợp lệ, nếu không có thì staff/admin về Dashboard, khách về trang chủ.
3. A03: kết thúc phiên xác thực và về trang chủ.
4. A04: nạp hồ sơ, nhóm hành vi và sổ địa chỉ chỉ của tài khoản hiện tại.

**Luồng thay thế / ngoại lệ:**

- 1a. Sai thông tin hoặc tài khoản bị khóa: từ chối đăng nhập, không tạo phiên xác thực.
- 4a. Hết phiên: yêu cầu đăng nhập trước khi trả dữ liệu cá nhân.

**Quy tắc và giới hạn:** Ba mục tiêu độc lập; các bước 3 và 4 là luồng riêng theo hành động người dùng. A04 chỉ xem; quản trị địa chỉ là A11. Không có chức năng tự khôi phục mật khẩu được xác định trong phạm vi hiện tại.

### 5.3. P01 / P02 / P03 / P04 / P05 — Duyệt nông sản đang bán

**Kích hoạt:** Người truy cập duyệt/tìm nông sản; người đăng nhập gửi đánh giá.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. P01: lấy danh sách nông sản đang hoạt động, tồn kho lớn hơn 0; hiển thị và phân trang.
2. P02: tại EP-P01, người xem nhập danh mục/khoảng giá; hệ thống lọc lại tập kết quả.
3. P03: nhập từ khóa; tìm theo tên, mô tả, xuất xứ của sản phẩm đang hoạt động.
4. P04: chọn sản phẩm; hiển thị thông tin, đánh giá và nội dung liên quan; ghi sự kiện xem.
5. P05: người đăng nhập nhập điểm và nội dung; hệ thống kiểm tra rồi tạo hoặc cập nhật đánh giá của chính họ.

**Luồng thay thế / ngoại lệ:**

- 1a/2a/3a. Không có kết quả: hiển thị trạng thái rỗng, cho sửa điều kiện.
- 2b. Không yêu cầu lọc: P01 vẫn hoàn thành; không chạy P02.
- 4a. Không tìm thấy/không được công khai: báo không khả dụng.
- 5a. Chưa đăng nhập: yêu cầu xác thực; không lưu đánh giá.
- 5b. Điểm/nội dung không hợp lệ: báo lỗi; không ghi thay đổi.

**Quy tắc và giới hạn:** Các bước mô tả các mục tiêu riêng, không bắt buộc tuần tự. Chỉ P02 extend P01, mũi tên hướng về P01. Một người có một đánh giá trên một sản phẩm; mã hiện tại không yêu cầu chứng minh đã mua. Search có thể trả sản phẩm hết hàng; đừng mô tả nó có cùng tập lọc kho với P01.

### 5.4. C01 / C02 / C03 / C04 — Xem giỏ hàng

**Kích hoạt:** Người đăng nhập mở giỏ hoặc thao tác một mặt hàng.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. C01: nạp/tạo giỏ gắn với tài khoản, hiển thị mặt hàng và tổng tiền dự kiến.
2. C02: nhận sản phẩm và số lượng nguyên dương; kiểm tra sản phẩm đang bán và tổng số lượng sau cộng không vượt tồn kho.
3. C02: thêm dòng mới hoặc cộng số lượng vào dòng hiện có; ghi sự kiện thêm giỏ.
4. C03: kiểm tra dòng thuộc giỏ của mình; cập nhật số lượng nguyên dương không vượt tồn kho.
5. C04: kiểm tra sở hữu; xóa dòng được yêu cầu và tính lại tổng.

**Luồng thay thế / ngoại lệ:**

- 2a/4a. Chuỗi không chuyển được thành số: trả lỗi kiểm tra đầu vào, không phát sinh lỗi máy chủ.
- 2b. Số lượng thêm không dương hoặc vượt tồn: từ chối thay đổi.
- 4b. Số lượng cập nhật không dương: bỏ dòng khỏi giỏ theo hành vi hiện tại; đây là nhánh thay thế, không dùng extend.
- 4c/5a. Dòng không thuộc mình hoặc không tồn tại: từ chối, không sửa giỏ khác.

**Quy tắc và giới hạn:** Đưa vào giỏ không giữ chỗ hoặc trừ kho. Phải kiểm tra kho lại khi đặt hàng. Kiểm tra số nguyên/lower bound chưa đầy đủ ở endpoint hiện tại, xem phụ lục.

### 5.5. O01 — Đặt hàng từ giỏ

**Kích hoạt:** Khách gửi biểu mẫu đặt hàng từ giỏ.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. Nạp giỏ của tài khoản, tên người nhận, số điện thoại, địa chỉ, ghi chú và phương thức COD/VietQR.
2. Kiểm tra giỏ không rỗng, thông tin hợp lệ, mặt hàng được bán, số lượng và tồn kho tại thời điểm chốt.
3. Tính tiền hàng theo giá hiện hành; phí giao 30.000 đồng, miễn phí khi tiền hàng từ 500.000 đồng.
4. Trong một giao dịch, tạo đơn pending và các dòng lưu tên/giá/số lượng tại lúc đặt; trừ kho.
5. Làm rỗng giỏ, ghi sự kiện mua hàng theo dòng đơn; trả mã đơn và trang chi tiết.

**Luồng thay thế / ngoại lệ:**

- 1a. Có địa chỉ mặc định: điền gợi ý; khách có thể nhập thông tin nhận hàng cho đơn này.
- 2a. Giỏ rỗng/thiếu hàng/đầu vào sai: trả lỗi, giữ giỏ, không tạo đơn.
- 4a. Lỗi trong giao dịch tạo đơn: rollback đơn, dòng đơn và tồn kho; không xóa giỏ.
- 5a. Lỗi ghi sự kiện sau khi giao dịch tạo đơn đã commit có thể khiến phản hồi lỗi dù đơn đã tồn tại: cần xử lý/idempotency trong hiện thực, không tự gửi lại gây trùng đơn.

**Quy tắc và giới hạn:** Đây là đặc tả đích: đảm bảo không bán vượt kho, tránh tạo trùng khi gửi lại. atomic hiện tại chưa đủ bảo vệ cạnh tranh; xem GAP03. Giá/kiểm tra kho/tính ship là bước nội bộ, không phải actor hay mục tiêu độc lập.

### 5.6. O02 — Đặt hàng qua hội thoại

**Kích hoạt:** Người dùng gửi yêu cầu mua nông sản qua chat.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. Kiểm tra đăng nhập; nhận ý định đặt hàng, sản phẩm, số lượng và dữ liệu của bản nháp phiên nếu có.
2. Đối sánh sản phẩm, lấy tên người nhận, điện thoại, địa chỉ từ câu chat hoặc dữ liệu tài khoản/địa chỉ; hỏi lại phần chưa đủ.
3. Yêu cầu chọn rõ COD hoặc VietQR nếu chưa chọn; cập nhật bản nháp theo câu trả lời.
4. Khi dữ liệu đã đủ, kiểm tra hợp lệ và kho; gọi tạo đơn trực tiếp với giá chụp và phí giao như O01.
5. Trả mã đơn, tiền hàng, phí giao, phương thức và liên kết chi tiết; kết thúc bản nháp.

**Luồng thay thế / ngoại lệ:**

- 1a. Khách vãng lai: yêu cầu đăng nhập, không tạo đơn.
- 2a. Không tìm được sản phẩm hoặc yêu cầu mơ hồ: thông báo/hỏi lại, không tự tạo đơn từ sản phẩm chưa xác định.
- 2b/3a. Thiếu địa chỉ/điện thoại/phương thức: giữ bản nháp, chờ bổ sung.
- 3b. Người dùng sửa số lượng, địa chỉ hoặc phương thức: cập nhật và kiểm tra lại trước khi tạo.
- 4a. Hết hàng hoặc tạo đơn thất bại: không trả mã thành công; giữ thông tin cần thiết để sửa.

**Quy tắc và giới hạn:** Luồng hiện tại chọn một sản phẩm đối sánh cho cuộc đặt hàng; không mặc định hỗ trợ giỏ nhiều dòng trong chat. Có thể tạo ngay khi câu chat đã cung cấp đủ dữ liệu; không bịa thêm bước xác nhận cuối bắt buộc. Không làm rỗng giỏ web. Không dùng LLM/fallback làm hai use case đặt hàng.

### 5.7. O03 / O04 / O06 — Xem lịch sử đơn của mình

**Kích hoạt:** Người đăng nhập mở lịch sử/chi tiết hoặc hỏi trạng thái đơn trong chat.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. Xác định tài khoản hiện tại; nhận mã đơn nếu người dùng cung cấp.
2. O03: lọc danh sách theo user hiện tại. O04: truy vấn đồng thời mã đơn và chủ đơn.
3. O06: nếu có mã thì kiểm tra mã và chủ đơn; nếu hỏi đơn gần nhất thì lấy đơn mới nhất của chính tài khoản.
4. Trả trạng thái và thông tin đơn được phép; không suy đoán tình trạng giao hàng ngoài dữ liệu đã ghi.

**Luồng thay thế / ngoại lệ:**

- 1a. Chưa đăng nhập: yêu cầu đăng nhập trước khi trả dữ liệu đơn.
- 2a/3a. Mã sai hoặc thuộc người khác: thông báo không tìm thấy đơn có quyền xem; không tiết lộ chủ đơn, địa chỉ hay số tiền.
- 3b. Chưa có đơn: báo lịch sử rỗng.

**Quy tắc và giới hạn:** O06 là quy tắc đích đã sửa về mô hình. fallback.py hiện còn nhánh truy mã không lọc user; sơ đồ không hợp thức hóa quyền xem đơn của người khác.

### 5.8. O05 / O11 / S01 — Hủy đơn của mình

**Kích hoạt:** Chủ đơn hoặc nhân viên có quyền yêu cầu hủy đơn pending.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. Kiểm tra quyền: O05 yêu cầu chủ đơn; O11 yêu cầu quyền xử lý đơn.
2. Đọc lại trạng thái và đảm bảo vẫn pending trong cùng giao dịch hủy.
3. Thực hiện S01: với mỗi dòng đơn, cộng lại đúng số lượng đã trừ vào sản phẩm liên quan.
4. Đổi trạng thái cancelled và commit cùng việc hoàn kho; trả kết quả hủy.

**Luồng thay thế / ngoại lệ:**

- 1a. Sai chủ đơn/thiếu quyền: từ chối; không thay đổi kho.
- 2a. Đơn confirmed/shipping/delivered/cancelled: từ chối hủy theo luồng này.
- 2b. Hai yêu cầu hủy đồng thời: chỉ một yêu cầu được hoàn kho; yêu cầu còn lại nhận trạng thái hiện hành.
- 3a. Lỗi lưu kho hoặc cập nhật đơn: rollback toàn giao dịch.

**Quy tắc và giới hạn:** O05 include S01 và O11 include S01. S01 không có actor khởi động độc lập. Hoàn tồn kho khác hoàn tiền; hệ thống chưa có nghiệp vụ hoàn tiền tự động. Bảo đảm đồng thời/đúng một lần là yêu cầu đích, chưa được kiểm chứng bằng khóa dòng trong mã.

### 5.9. O07 / O08 / O09 / O10 / O12 — Tra cứu đơn toàn hệ thống

**Kích hoạt:** Nhân viên tra cứu đơn hoặc yêu cầu chuyển trạng thái/xác nhận hàng loạt.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. O07: nhập từ khóa/bộ lọc và xem đơn trong phạm vi được cấp quyền.
2. O08: kiểm tra pending; nếu VietQR thì đã đối soát thực tế theo Q04; chuyển confirmed.
3. O09: kiểm tra confirmed, có thông tin bắt đầu giao; chuyển shipping.
4. O10: kiểm tra shipping và thông tin giao thành công; chuyển delivered.
5. O12: đọc từng đơn đã chọn, áp dụng điều kiện O08 cho từng đơn; trả số thành công và danh sách bỏ qua/lỗi.

**Luồng thay thế / ngoại lệ:**

- 1a. Không có kết quả: trả danh sách rỗng.
- 2a. Thiếu đối soát hoặc tiền chưa khớp: giữ pending và báo lý do.
- 2b/3a/4a. Trạng thái nguồn không đúng hoặc đã thay đổi: từ chối; không nhảy bước/quay ngược.
- 5a. Có đơn không đủ điều kiện: bỏ qua đơn đó, vẫn báo kết quả từng đơn; không tự tạo chứng từ để lách điều kiện.

**Quy tắc và giới hạn:** Ma trận đích: pending→confirmed→shipping→delivered; pending→cancelled qua O05/O11. Không trừ kho lần hai khi xác nhận/giao hàng. O12 lặp quy tắc O08 nhưng không dùng quan hệ include để thay cho mô tả thuật toán.

### 5.10. Q01 — Xem thông tin thanh toán VietQR

**Kích hoạt:** Khách mở thông tin thanh toán đơn VietQR.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. Kiểm tra đăng nhập, chủ đơn và phương thức.
2. Lấy số tài khoản/ngân hàng/thụ hưởng, số tiền phải trả và nội dung chuyển khoản gắn mã đơn.
3. Tạo URL yêu cầu ảnh VietQR và hiển thị QR cùng thông tin dạng chữ.
4. Khách thực hiện chuyển tiền trên ứng dụng ngân hàng ngoài AgriSense.

**Luồng thay thế / ngoại lệ:**

- 1a. Đơn COD: không khởi tạo luồng thanh toán VietQR cho đơn đó.
- 3a. Dịch vụ ảnh lỗi: vẫn hiển thị thông tin chuyển khoản dạng chữ nếu cấu hình hợp lệ; không thông báo đã thanh toán.
- 2a. Thiếu cấu hình tài khoản: báo chưa thể cung cấp thông tin, không bịa tài khoản.

**Quy tắc và giới hạn:** Dịch vụ VietQR chỉ tạo ảnh. Ngân hàng chưa có API/webhook tích hợp trong phạm vi, không vẽ ngân hàng như actor xác nhận tự động. Bước 4 là hoạt động bên ngoài hệ thống.

### 5.11. Q02 / Q03 / Q05 — Nộp / thay chứng từ chuyển khoản

**Kích hoạt:** Khách/nhân viên nộp hoặc xem chứng từ.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. Q02/Q05: xác thực chủ đơn hoặc quyền nhân viên; kiểm tra đơn VietQR pending.
2. Chọn tệp; kiểm tra loại ảnh, nội dung và giới hạn dung lượng theo cấu hình triển khai.
3. Lưu/thay tệp chứng từ và thời điểm nộp; trả trạng thái chờ đối soát.
4. Q03: kiểm tra quyền xem, rồi trả chứng từ hiện có của đơn.

**Luồng thay thế / ngoại lệ:**

- 1a. Đơn không đúng chủ, không phải VietQR hoặc không pending: từ chối nộp/thay.
- 2a. Thiếu tệp, sai định dạng hoặc vượt giới hạn: giữ chứng từ cũ, yêu cầu chọn lại.
- 3a. Lưu thất bại: không trả thành công và không thay chứng từ cũ bằng tham chiếu hỏng.
- 4a. Chưa có tệp: hiển thị chưa nộp; không diễn giải là chưa chuyển tiền.

**Quy tắc và giới hạn:** Mức giới hạn tải tệp chưa có số cụ thể trong yêu cầu dự án, cần cấu hình rõ khi triển khai. Endpoint hiện mới kiểm tra chủ đơn, pending và có tệp; các kiểm tra đích được liệt kê là chênh lệch. Q05 có thể là thao tác phụ trong màn hình xử lý đơn; không ngầm chuyển trạng thái chỉ vì tải ảnh.

### 5.12. Q04 — Ghi nhận kết quả đối soát

**Kích hoạt:** Nhân viên cần quyết định đơn VietQR đã nhận đủ tiền hay chưa.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. Mở đơn và xác định số tiền, mã tham chiếu, người trả; xem chứng từ nếu có.
2. Nhân viên kiểm tra giao dịch thực tế trên kênh ngân hàng được phép, ngoài AgriSense.
3. Đối chiếu số tiền, nội dung/mã đơn, thời điểm và tránh dùng cùng giao dịch cho nhiều đơn.
4. Ghi nhận kết quả khớp/chưa khớp cùng thông tin đối soát; chỉ kết quả khớp cho phép O08.
5. Nếu đã kiểm tra nhận tiền nhưng thiếu ảnh khách, có thể đính kèm chứng từ xác nhận nội bộ; ghi rõ người và thời điểm.

**Luồng thay thế / ngoại lệ:**

- 2a. Chưa thấy tiền/không truy cập được dữ liệu ngân hàng: giữ trạng thái chờ xác minh.
- 3a. Thiếu/thừa tiền, sai mã, trùng tham chiếu: giữ pending và nêu lý do xử lý thủ công.
- 4a. Không lưu được kết quả: không coi là đã hoàn tất đối soát.

**Quy tắc và giới hạn:** Đối soát là thao tác người thực hiện, không phải nhìn ảnh rồi tự suy ra tiền đã về. Mã nguồn hiện gộp thao tác này với chuyển trạng thái và có thể tạo ảnh xác nhận nội bộ; chưa có sổ đối soát độc lập bảo đảm mọi dữ liệu nêu trên. Không tuyên bố đã có chức năng hoàn tiền.

### 5.13. T01 / T02 — Duyệt / tìm kiếm lô hàng

**Kích hoạt:** Người truy cập tìm lô, chọn liên kết hoặc quét QR.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. T01: nhận từ khóa/bộ lọc và trả danh sách lô phù hợp.
2. T02: nhận mã lô từ URL hoặc QR; tìm lô tương ứng.
3. Hiển thị sản phẩm, vùng trồng, ngày thu hoạch/đóng gói/hạn dùng, chứng nhận và ghi chú đã nhập.
4. Hiển thị các bản ghi lịch sử hiện có của lô.

**Luồng thay thế / ngoại lệ:**

- 1a. Không có lô phù hợp: danh sách rỗng.
- 2a. QR/mã sai hoặc lô đã xóa: báo không tìm thấy.
- 3a/4a. Chưa có chứng nhận/lịch sử: hiển thị chưa có dữ liệu, không tự xác nhận chất lượng.

**Quy tắc và giới hạn:** Quét QR và nhập URL là hai cách khởi động cùng T02. Nhật ký hiện có không đồng nghĩa mọi thay đổi đều đã tự ghi. QR nội bộ sinh bằng thư viện không cần actor dịch vụ ngoài.

### 5.14. T04 / T05 — Tạo lô nông sản

**Kích hoạt:** Nhân viên tạo lô hoặc lưu thay đổi lô.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. Kiểm tra quyền thêm/sửa và sản phẩm tham chiếu; khi sửa, nạp đúng lô.
2. Nhập mã lô duy nhất, vùng trồng, các ngày, chứng nhận, sản lượng và ghi chú; kiểm tra trường bắt buộc và tính hợp lý ngày.
3. T04: lưu lô và sinh QR trỏ đến URL truy xuất mã lô.
4. T05: lưu thay đổi; khi mã lô/URL thay đổi, tái tạo QR hoặc giữ quy tắc mã bất biến để QR luôn đúng.
5. Trả kết quả, kiểm tra liên kết truy xuất của QR.

**Luồng thay thế / ngoại lệ:**

- 2a. Mã trùng hoặc dữ liệu không hợp lệ: yêu cầu sửa, chưa ghi thành công.
- 3a/4a. Sinh/lưu QR thất bại: báo trạng thái chưa hoàn chỉnh và không tuyên bố QR sẵn sàng.
- 4b. Không đổi mã/URL: giữ QR hiện có.

**Quy tắc và giới hạn:** Tự ghi lịch sử mọi lần sửa không được giả định; T08 là quản trị nhật ký hiện có. Mã hiện tại chỉ sinh QR khi thiếu, nên đồng bộ QR khi đổi mã là yêu cầu đích cần sửa.

### 5.15. R01 — Xem gợi ý nông sản

**Kích hoạt:** Người truy cập mở vùng gợi ý nông sản.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. Nếu đã đăng nhập, lấy các sự kiện trong 30 ngày có liên kết danh mục, tính điểm view=1, search=2, add_to_cart=3, purchase=5, review=4.
2. Khi tổng điểm đủ 3, lấy tối đa 3 danh mục điểm cao, chọn sản phẩm active và còn hàng, loại sản phẩm đã xuất hiện trong đơn của người đó.
3. Sắp xếp theo điểm và giới hạn số lượng, trả lý do gợi ý.
4. Nếu khách vãng lai hoặc không đủ điểm, lấy sản phẩm bán chạy trong 30 ngày của đơn confirmed/shipping/delivered rồi bổ sung sản phẩm mới còn hàng khi cần.

**Luồng thay thế / ngoại lệ:**

- 1a. Sự kiện tìm kiếm không có danh mục/sản phẩm: không đóng góp điểm danh mục.
- 2a. Không còn sản phẩm thích hợp: có thể trả ít hoặc không có; nhánh cá nhân hóa hiện không tự lấp đầy bằng bestseller.
- 4a. Không có dữ liệu bán chạy: dùng sản phẩm mới đang bán/còn hàng.
- 2b. Hiện tại tập loại đã mua bao gồm sản phẩm trong đơn đã hủy; phải giải thích đúng quy tắc mã.

**Quy tắc và giới hạn:** Nhánh cá nhân hóa và dự phòng là luồng thay thế của R01, không phải quan hệ extend. R05 xem dữ liệu RecommendationLog hiện có, không chứng minh engine tự ghi mỗi lần gợi ý.

### 5.16. R03 — Chạy cập nhật phân nhóm

**Kích hoạt:** Người vận hành chạy lệnh update_segments.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. Kiểm tra quyền môi trường và kết nối CSDL; chạy lệnh quản trị.
2. Duyệt các tài khoản active; lấy số đơn không cancelled, số đơn 30 ngày, ngày đơn gần nhất và tổng sự kiện.
3. Không có đơn: đăng ký ≤7 ngày→new; nếu lâu hơn và ≥5 sự kiện→interested; còn lại→new.
4. Có đơn: ≥3 đơn trong 30 ngày→loyal; nếu không và đơn gần nhất >30 ngày→at_risk; còn lại→normal.
5. Chỉ khi nhóm thay đổi: cập nhật nhóm/thời điểm và thêm UserSegment với lý do; kết thúc lệnh.

**Luồng thay thế / ngoại lệ:**

- 1a. Thiếu quyền/lỗi CSDL: dừng và báo lỗi; không báo chạy thành công.
- 5a. Nhóm không đổi: không thêm lịch sử mới.
- 5b. Lỗi giữa vòng lặp: mã hiện tại có thể đã cập nhật một phần tài khoản; báo phạm vi thất bại và kiểm tra trước khi chạy lại.

**Quy tắc và giới hạn:** Đếm đơn không bị hủy, không chỉ đơn delivered. Chạy cho mọi user active, có cả staff theo mã hiện tại. Không có bằng chứng cấu hình scheduler; không vẽ tác nhân hẹn giờ. Quyền CLI độc lập với is_staff.

### 5.17. H01 — Nhận tư vấn nông sản

**Kích hoạt:** Người truy cập gửi câu hỏi tư vấn.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. Nhận và kiểm tra câu hỏi, xác định phiên/tài khoản; nạp ngữ cảnh hội thoại phù hợp.
2. Phân loại yêu cầu; nếu là đặt/tra đơn, chuyển xử lý O02/O06 với kiểm tra quyền tương ứng.
3. Với tư vấn, sử dụng dữ liệu sản phẩm/ngữ cảnh để gọi nhà cung cấp AI đã cấu hình.
4. Nhận câu trả lời, lưu tin nhắn và phản hồi; trả kết quả cho người dùng.

**Luồng thay thế / ngoại lệ:**

- 1a. Nội dung rỗng/không hợp lệ: báo cần nhập câu hỏi.
- 3a. Thiếu khóa API, quá thời gian hoặc dịch vụ AI lỗi: dùng phản hồi theo quy tắc/dữ liệu trong hệ thống và ghi dấu fallback.
- 3b. Dữ liệu không đủ trả lời: nói rõ chưa có thông tin; không bịa tình trạng đơn hay chứng nhận.
- 4a. Lỗi lưu hội thoại: báo lỗi phù hợp, không hứa lịch sử đã được lưu.

**Quy tắc và giới hạn:** LLM và fallback là cách thực hiện một mục tiêu. AI là actor hỗ trợ bên ngoài; fallback/thuật toán là nội bộ. Tin nhắn ChatMessage khác sự kiện UserEvent loại chat.

### 5.18. H02 / H03 / H04 — Xem tin nhắn phiên hiện tại

**Kích hoạt:** Người dùng xem tin nhắn, lịch sử hoặc chọn bắt đầu lại.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. H02: xác định khóa phiên và trả tin nhắn đúng phạm vi phiên hiện tại.
2. H03: yêu cầu đăng nhập và lọc các hội thoại theo tài khoản hiện tại.
3. H04: xác định hội thoại hiện tại theo phiên/tài khoản; xóa dữ liệu hội thoại thuộc phạm vi thao tác.
4. Xóa bản nháp đặt hàng của phiên tương ứng và trả trạng thái hội thoại mới.

**Luồng thay thế / ngoại lệ:**

- 1a/2a. Chưa có tin nhắn: trả trạng thái rỗng.
- 2b. Chưa đăng nhập: không trả lịch sử tài khoản.
- 3a. Không xác định được phiên hợp lệ: không xóa hội thoại của người khác.
- 3b. Không có hội thoại cũ: việc bắt đầu lại vẫn có thể kết thúc với phiên trống.

**Quy tắc và giới hạn:** Bước 4 thuộc H04. Xóa chat không hủy đơn đã tạo; hủy đơn đi qua O05/O11. H04 phải xóa cả draft để lần hội thoại mới không vô tình tiếp tục đơn nháp cũ.

### 5.19. D01 / D02 / D03 — Xem báo cáo điều hành

**Kích hoạt:** Nhân viên mở báo cáo/tra cứu hành vi hoặc chọn xuất Excel.

**Tác nhân, tiền/hậu điều kiện:** dùng từng dòng tương ứng ở mục 3. **Bảo đảm khi thất bại:** áp dụng mục 4; ngoại lệ về commit một phần hoặc tích hợp được chỉ rõ bên dưới.

**Luồng chính:**

1. D01: kiểm tra quyền; lấy KPI và dữ liệu biểu đồ đúng kỳ; hiển thị tên và định nghĩa từng chỉ số.
2. D03: nhận điều kiện tra cứu, lấy các sự kiện đã ghi và tổng hợp hành vi.
3. D02: kiểm tra quyền xuất; truy vấn toàn bộ đơn hàng theo chức năng hiện tại.
4. Tạo tệp Excel với thông tin đơn hàng và gửi cho người yêu cầu.

**Luồng thay thế / ngoại lệ:**

- 1a/2a. Không có dữ liệu: hiển thị 0/danh sách rỗng, không coi là lỗi.
- 3a. Người dùng đang lọc trên màn hình: vẫn xuất toàn bộ đơn; phải ghi rõ phạm vi.
- 4a. Tạo tệp/lấy dữ liệu thất bại: báo lỗi, không trả tệp hỏng như thành công.

**Quy tắc và giới hạn:** KPI 30 ngày cộng đơn không cancelled khác doanh thu đã giao; dashboard đơn có chỉ số delivered riêng. Danh sách đơn/sự kiện có giới hạn 100 trong mã; Excel không bị ràng buộc bởi 100 hàng màn hình. Không hứa dữ liệu theo thời gian thực hoặc nhật ký đầy đủ khi event chưa ghi.

## 6. Đặc tả quản trị dữ liệu và các tra cứu còn lại

### 6.1. A05–A11 — Quản trị tài khoản, địa chỉ và quyền

**Kích hoạt:** nhân viên/quản trị viên chọn thao tác trong Admin. Tiền/hậu điều kiện theo mục 3.

**Luồng chính:**

1. Xác thực tài khoản quản trị, kiểm tra quyền model và quyền của thao tác được chọn.
2. A05: nhập tài khoản mới, kiểm tra duy nhất và mật khẩu; lưu tài khoản. A06: nạp tài khoản, sửa các trường được phép; kiểm tra và lưu.
3. A07: đổi trạng thái active/inactive. A08: nhập và xác nhận mật khẩu mới, kiểm tra chính sách rồi lưu bản băm.
4. A09: hiển thị đối tượng và ảnh hưởng liên kết; người thực hiện xác nhận xóa; hệ thống áp dụng ràng buộc quan hệ.
5. A10: quản trị viên chọn tài khoản, nhóm/quyền; lưu cấu hình quyền sau khi kiểm tra phạm vi được cấp.
6. A11: chọn đúng khách, thêm/sửa/xóa địa chỉ hoặc chọn mặc định; kiểm tra quyền theo từng nhánh và lưu.

**Thay thế/ngoại lệ:**

- 1a. Thiếu quyền: không hiển thị dữ liệu vượt quyền và từ chối thao tác.
- 2a/3a/6a. Dữ liệu không hợp lệ hoặc tham chiếu không tồn tại: giữ bản cũ, hiển thị lỗi để sửa.
- 4a. Người thực hiện hủy xác nhận: không xóa. 4b. Bị ràng buộc quan hệ ngăn xóa: thông báo lý do; không xóa dở dang.
- 5a. Người không phải quản trị viên yêu cầu cấp quyền: từ chối theo chính sách đề xuất; đây là điểm cần kiểm tra thêm so với cấu hình UserAdmin hiện có.

**Giới hạn:** A06 không được dùng để cấp quyền vượt A10. Khóa tài khoản không đồng nghĩa xóa dữ liệu hay hủy toàn bộ đơn. Không mô tả chức năng đặt lại mật khẩu bởi nhân viên thành “quên mật khẩu” tự phục vụ. Chính sách ngăn tự nâng quyền và chỉ một địa chỉ mặc định cần được triển khai nhất quán; không mặc định Django Admin tự đáp ứng mọi chính sách dự án.

### 6.2. P07–P16, T06, T08 — Thêm, sửa, xóa dữ liệu nghiệp vụ

**Kích hoạt:** nhân viên chọn thao tác cụ thể trên đối tượng. Mỗi mã là mục tiêu riêng; không phải mọi lần đều làm đủ CRUD.

| Mã | Đối tượng / thao tác | Kiểm tra riêng |
|---|---|---|
| P07 / P08 / P09 | Thêm / sửa / xóa Product | Giá và tồn kho hợp lệ; danh mục/nhà cung cấp tồn tại; khi xóa phải xem ảnh hưởng đơn/lô/đánh giá |
| P10 / P11 / P12 | Thêm / sửa / xóa Category | Tên/slug và quan hệ sản phẩm theo model; không làm mất liên kết ngoài chính sách |
| P13 / P14 / P15 | Thêm / sửa / xóa Supplier | Thông tin liên hệ, tham chiếu từ sản phẩm |
| P16 | Xem / sửa / xóa ProductReview | Phân biệt view/change/delete; không đồng nhất với P05 viết đánh giá cá nhân |
| T06 | Xóa ProductBatch | Kiểm tra lịch sử liên quan và URL/QR đã phát hành |
| T08 | Thêm / sửa / xóa TraceabilityRecord | Đúng lô, trường thay đổi, giá trị cũ/mới, người thực hiện; thời điểm hệ thống theo model |

**Luồng chính:**

1. Kiểm tra quyền view/add/change/delete tương ứng và nạp đúng đối tượng nếu sửa/xóa.
2. Nhập dữ liệu cho nhánh thêm/sửa; hoặc xem đối tượng và danh sách ảnh hưởng cho nhánh xóa.
3. Kiểm tra dữ liệu, quan hệ tham chiếu và quy tắc của bảng trên.
4. Với xóa: yêu cầu xác nhận. Lưu thay đổi/xóa theo giao dịch thích hợp và trả kết quả.
5. Cập nhật danh sách đang xem; trường chỉ đọc không được sửa qua biểu mẫu.

**Thay thế/ngoại lệ:**

- 1a. Thiếu quyền/bản ghi đã mất: từ chối; không sửa đối tượng khác.
- 3a. Dữ liệu sai, trùng khóa hoặc vi phạm quan hệ: trả lỗi cụ thể, không ghi một phần.
- 4a. Hủy xác nhận: không đổi dữ liệu. 4b. Lỗi lưu: báo thất bại; bảo toàn bản cũ trong phạm vi giao dịch.
- P16 nhánh xem: trả dữ liệu rồi kết thúc, không chạy các bước sửa/xóa.

**Hậu điều kiện:** theo từng mã ở mục 3. Xóa có thể có hành vi CASCADE/PROTECT/SET_NULL tùy quan hệ model; cần đọc danh sách ảnh hưởng, không tuyên bố mọi loại xóa đều giữ lịch sử. T08 là quản trị bản ghi, không phải bằng chứng tự động ghi lịch sử bất biến.

### 6.3. P06, T03, T07, R02, R04, R05, H05 — Tra cứu quản trị

**Kích hoạt:** nhân viên mở danh sách hoặc nhập từ khóa/bộ lọc.

1. Kiểm tra quyền xem model/nghiệp vụ.
2. P06 tìm sản phẩm/tồn kho; T03 tìm lô; T07 tìm lịch sử nguồn gốc; R02 tìm khách/nhóm; R04 tìm lịch sử phân nhóm; R05 tìm nhật ký gợi ý; H05 tìm phiên/tin nhắn.
3. Áp dụng bộ lọc và phân trang/giới hạn thực tế của kênh hiển thị.
4. Trả các bản ghi đã có và cho mở chi tiết nếu được phép.

**Ngoại lệ:** 1a thiếu quyền→từ chối; 2a điều kiện sai→báo để sửa; 3a không có dữ liệu→danh sách rỗng; 4a bản ghi đã bị xóa→báo không tồn tại. Không sửa dữ liệu nghiệp vụ trong các luồng tra cứu. Một bản ghi thiếu không chứng minh hoạt động đó chưa từng xảy ra khi hệ thống chưa ghi log đầy đủ.

### 6.4. D04 — Hiệu chỉnh dữ liệu quản trị phụ trợ

**Kích hoạt:** nhân viên được giao nhiệm vụ bảo trì chọn đúng model và thao tác đã cấp quyền. Tiền/hậu điều kiện ở mục 3.

| Model / giao diện hiện có | Quyền và thao tác được hiểu trong D04 | Giới hạn |
|---|---|---|
| UserEvent | Xem/thêm/sửa/xóa khi có quyền tương ứng | Hiệu chỉnh làm đổi dữ liệu phân tích; không coi dữ liệu sửa tay là dấu vết bất biến |
| UserSegment | Quản trị bản ghi lịch sử khi có quyền | Sửa lịch sử không tự chạy thuật toán, không tự đồng bộ nhóm hiện tại của User |
| RecommendationLog | Quản trị nhật ký có sẵn khi có quyền | Không thay thế R01 và không chứng minh engine tự ghi log |
| ChatSession | Bảo trì phiên theo quyền | Xóa có thể ảnh hưởng tin nhắn; xem trước phạm vi |
| ChatMessage | Bản ghi độc lập có quyền add/change/delete; inline trong ChatSession có các trường chỉ đọc | Phân biệt màn hình độc lập và inline; sửa tay có thể thay đổi ngữ cảnh |
| Cart / CartItem inline | Tra cứu, bảo trì dữ liệu giỏ trong giới hạn Admin | Trường product/quantity/subtotal inline chỉ đọc; không quảng cáo CRUD mọi dòng |
| Order / OrderItem inline | Tham chiếu khi kiểm tra dữ liệu; nghiệp vụ trạng thái/chứng từ thuộc O/Q | Trường dòng đơn inline chỉ đọc; D04 không cho đi vòng kiểm tra kho/đối soát |

**Luồng chính:**

1. Xác nhận nhiệm vụ bảo trì và kiểm tra quyền model + thao tác.
2. Chọn bản ghi, xem dữ liệu hiện tại, các quan hệ bị ảnh hưởng và trường chỉ đọc.
3. Nhập thay đổi được phép hoặc xem trước phạm vi xóa.
4. Kiểm tra ràng buộc; với xóa phải xác nhận rõ đối tượng; lưu thay đổi và trả kết quả.
5. Nếu thay đổi tác động báo cáo/nhóm/gợi ý, thông báo cần kiểm tra các kết quả phụ thuộc; không tự tuyên bố đã tái tính mọi thứ.

**Ngoại lệ:** 1a thiếu quyền→từ chối; 3a thao tác làm sai quy trình bán hàng→chuyển sang O/Q tương ứng hoặc không thực hiện; 4a dữ liệu sai/xóa bị chặn→không ghi thay đổi; 4b người dùng hủy→giữ nguyên.

Quyền kỹ thuật mà Django Admin hiện cho phép có thể rộng hơn phạm vi nghiệp vụ đề xuất. Sự hiện diện của nút xóa/field sửa được không phải lý do mô hình hóa việc chỉnh kho, giá trị đơn hoặc trạng thái tùy ý như luồng bán hàng hợp lệ.

## 7. Quy tắc UML và trạng thái

| Quan hệ | Hướng | Ý nghĩa |
|---|---|---|
| Association | Tác nhân — use case, đường liền | Tham gia; không biểu thị thứ tự thực thi |
| Generalization | Vai trò con → vai trò tổng quát, tam giác rỗng | Kế thừa khả năng tham gia, tiền điều kiện vẫn có hiệu lực |
| include | O05 → S01; O11 → S01 | Hoàn kho bắt buộc trong luồng hủy thành công |
| extend | P02 → P01, [người xem yêu cầu lọc] | Mở rộng tại EP-P01: điều chỉnh tập kết quả; P01 vẫn hoàn chỉnh nếu không lọc |

Đăng nhập thường là tiền điều kiện; không nối include đăng nhập vào mọi chức năng. LLM/fallback, cá nhân hóa/bán chạy, COD/VietQR, thông tin có/thiếu là các nhánh được mô tả trong đặc tả, không tự động trở thành quan hệ extend.

| Trạng thái nguồn | Thao tác | Trạng thái đích | Điều kiện bổ sung |
|---|---|---|---|
| pending | O08 hoặc một đơn trong O12 | confirmed | VietQR đã được đối soát thực tế |
| confirmed | O09 | shipping | Có quyền và thông tin bắt đầu giao |
| shipping | O10 | delivered | Có xác nhận giao thành công |
| pending | O05 / O11 | cancelled | Đúng chủ đơn/quyền; include S01 |
| cancelled / delivered | Yêu cầu đổi tiếp | Từ chối trong phạm vi mô hình | Chưa có luồng trả hàng/hoàn tiền/mở lại đơn |

## 8. Những điều không được khẳng định khi bảo vệ

Không nói “toàn bộ yêu cầu đều đã triển khai” dựa trên sơ đồ. Không nói “AI tự xử lý mọi việc”, “VietQR tự xác nhận nhận tiền”, “mọi đánh giá là từ người đã mua”, “mọi thay đổi lô đều có log”, “phân nhóm chỉ tính đơn đã giao”, hoặc “thêm vào giỏ đã trừ kho”. Phụ lục đối chiếu ghi đúng nguồn và những khoảng trống còn lại.

Phạm vi chưa có trong dự án: cổng nhà cung cấp/shipper, tích hợp vận chuyển, hoàn tiền tự động, trả hàng, mã giảm giá, giỏ khách vãng lai, scheduler phân nhóm đã cấu hình. Nếu đề bài chính thức yêu cầu các mục này, phải bổ sung yêu cầu và mô hình tương ứng; không tự đưa vào như chức năng đã có.
