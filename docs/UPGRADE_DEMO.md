# AgriSense - Ban nang cap demo

Ngay: 19/11/2026. Muc tieu: demo do an, giao dien nhat quan va luong nghiep vu co the kiem chung.

## Chay ban demo

```powershell
.venv/Scripts/python.exe manage.py migrate --settings=nongsan_project.demo_settings
.venv/Scripts/python.exe manage.py seed_showcase --settings=nongsan_project.demo_settings
.venv/Scripts/python.exe manage.py runserver 127.0.0.1:8001 --settings=nongsan_project.demo_settings
```

Mo http://127.0.0.1:8001/. Tai khoan rieng trong database demo:

| Vai tro | Username | Password |
| --- | --- | --- |
| Khach hang | demo_customer | Demo@123 |
| Quan tri | demo_admin | Admin@123 |

Demo dung `demo.sqlite3`, media trong `media/demo`, QR tro ve cong 8001. Du lieu la minh hoa; khong chuyen tien that. Lenh seed tu choi settings thong thuong, khong reset du lieu, khong doi mat khau tai khoan da co. Co 12 san pham, 3 combo, lo hang con han/can han, canh bao ton thap va don cho xu ly. Anh duoc tai su dung tu anh san pham co san; ban thu gon nam trong `static/images/showcase` de clone du an van demo duoc.

SQLite phuc vu trinh dien local. Kiem thu dong thoi thuc hien tren MySQL; khong dung SQLite de khang dinh khoa hang trong production.

## Kich ban trinh bay 5-7 phut

1. Trang chu: giao dien xanh la, nen kem, anh nong san, nut di cho thong minh.
2. Dang nhap khach, vao `/products/planner/`, nhap `300k mua rau cu cho 2 nguoi trong 3 ngay`. Xem gia, phi giao hang va ngan sach con lai. Tang so luong vuot ngan sach de minh hoa nut bi khoa; sau do chon giua cac mon va them vao gio.
3. Dat hang voi chuyen khoan mo phong. Trang don hien dung cac lo da xuat. Bam **Mo phong thanh toan thanh cong** de chuyen sang da xac nhan, khong hien QR ngan hang that.
4. Mo link lo da xuat de xem nguon goc; quay lai don va chon **Mua lai don nay**, he thong kiem tra ton/gia hien tai.
5. Vao `/products/combos/`, them gio theo mua. Combo la goi san pham theo gia hien tai, chua co chiet khau rieng.
6. Dang nhap admin, vao dashboard va **Viec can xu ly**: lo can han, lo qua han, hang co the ban duoi 10 don vi, don cho qua 24 gio. Vao **Nhap kho theo lo** de ghi nhan lo moi.
7. Thu tren man hinh dien thoai: bo loc, gio hang, checkout, tien do don va dashboard.

## Pham vi cac nang cap

- Kho theo lo: `remaining_quantity`, uu tien han gan nhat (FEFO), chia mot dong don qua nhieu lo neu can, khoa hang trong transaction, chan lo het han, huy hoan dung lo mot lan. QR tren don tro ve lo da xuat, khong lay lo moi nhat cua san pham.
- Chuyen du lieu cu: khong tu gan nguon goc cho ton cu. Chon **Phan bo ton kho hien co** va nhap so luong bang ton hien tai. Can xu ly xong don cu dang pending truoc khi chuyen; tranh hoan kho cu vao san pham da chuyen lo ma khong biet lo goc. Sau khi bat quan ly lo, sua ton san pham trong Django Admin bi khoa; nhap them qua form nhap lo.
- Lo qua han: bi loai khoi hang co the ban, van giu ton vat ly de kiem ke. Chua co quy trinh huy lo/ghi nhan hao hut hay thu hoi hang.
- Di cho thong minh: nhan dang ngan sach, so nguoi, so ngay, uu tien rau cu/trai cay bang quy tac tieng Viet; tinh gio bang gia va ton kho thuc te, gom phi giao hang. Day la fallback xac dinh, khong phai mo hinh dinh duong hay goi API LLM moi. Chatbot co the tra gio goi y va dan sang trang chinh sua. Gio chi duoc them sau thao tac cua nguoi dung; khong tu tao don. Token goi y het han sau 15 phut, kiem tra lai gia/ton/ngan sach va ngan them lap.
- Combo: quan ly qua Django Admin > Seasonal combos, chon san pham va so luong. Mua lai/Combo giu san pham da co trong gio, kiem tra tat ca truoc khi them; loi mot mon thi khong them do dang.
- Dashboard: canh bao theo du lieu hien tai, lien ket xu ly, responsive cho mobile. Gia tri don hang trong KPI giu dinh nghia hien co (khong phai doanh thu tien da thu).
- UI: trang chu, danh sach/bo loc/sap xep, giỏ theo mua, planner va quan tri dung phong cach thong nhat; font Be Vietnam Pro/Lora, focus ban phim, reduced-motion, anh lazy-load.

## Hop dong thanh toan tu dong

Endpoint: `POST /cart/payments/webhook/`.

Mac dinh tat. Dat `PAYMENT_WEBHOOK_SECRET` trong moi truong, toi thieu 32 ky tu ngau nhien. Khong commit khoa. He thong chua gan voi mot nha cung cap ngan hang cu the: can adapter tin cay chuyen thong bao da xac thuc cua nha cung cap ve hop dong duoi day.

```json
{"transaction_id":"unique-gateway-id","order_code":"ORD123456789012","amount":"255000","currency":"VND"}
```

Headers:

- `X-Payment-Timestamp`: Unix timestamp giay, trong khoang 5 phut.
- `X-Payment-Signature`: HMAC-SHA256 hex voi secret, du lieu ky la `timestamp + '.' + raw_body_bytes`.

Chi chap nhan don VietQR pending, dung VND va dung tong tien. Ma giao dich unique theo provider. Gui lai cung giao dich/don/so tien duoc chap nhan ma khong ghi nhan lan hai; ma giao dich cho don khac bi tu choi. Payload khong hop le 400, sai chu ky/thoi gian 403, khong co don 404, xung dot giao dich 409, chua cau hinh 503. Thanh toan demo khong the xac nhan don that va nguoc lai.

Chua kiem chung webhook tu nha cung cap that, giao dich ngan hang that, hoan tien, thong bao thieu/thua tien hay deployment production. Khong coi mo phong la da nhan tien that.

## Chay ung dung thong thuong

```powershell
.venv/Scripts/python.exe manage.py migrate
.venv/Scripts/python.exe manage.py runserver
```

Migration chi them bang/truong, khong gan lo cho don cu. Database MySQL hien tai da duoc migrate trong phien nang cap. Du lieu combo/lo demo chi nam o database demo; tao combo va nhap lo that qua quan tri khi can.

## Kiem thu

```powershell
.venv/Scripts/python.exe manage.py check
.venv/Scripts/python.exe manage.py makemigrations --check --dry-run
.venv/Scripts/python.exe -m coverage run --branch --source=apps,nongsan_project --omit="*/tests/*,*/migrations/*" manage.py test --settings=nongsan_project.test_settings --noinput
.venv/Scripts/python.exe -m coverage report --precision=2
```

Bao cao PASS/FAIL va cac gioi han: [UPGRADE_VERIFICATION.md](UPGRADE_VERIFICATION.md).
