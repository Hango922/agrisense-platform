# Van hanh tren Windows

Ban nay dung MySQL trong `.env`, Waitress va WhiteNoise, DEBUG=False,
chi lang nghe 127.0.0.1. Khong mo port ra Internet/LAN.
Demo rieng van dung `nongsan_project.demo_settings` va SQLite.

## Chuan bi

Chay PowerShell tai thu muc du an:

```powershell
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe manage.py migrate --settings=nongsan_project.operational_settings
.venv/Scripts/python.exe manage.py changepassword admin
.venv/Scripts/python.exe manage.py changepassword demo_admin
```

Nhap mat khau moi trong terminal, khong gui trong chat. Tai khoan khong dung nua
co the duoc vo hieu hoa trong trang quan tri sau khi dang nhap.
Khong chay seed_data tren du lieu van hanh.

Trong `.env`, thay khoa Gemini da chia se bang khoa moi va doi SECRET_KEY
thanh chuoi ngau nhien toi thieu 50 ky tu. Doi SECRET_KEY se dang xuat cac phien
cu va vo hieu hoa cac de xuat gio hang da ky. Co the tao khoa ngay tai may bang:

```powershell
.venv/Scripts/python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Khong dua output len chat/Git. Dung tai khoan MySQL rieng, chi co quyen tren
database cua ung dung; thay DB_USER/DB_PASSWORD trong `.env` sau khi cap quyen.

## Kiem tra va khoi dong

```powershell
.venv/Scripts/python.exe manage.py check_operations --settings=nongsan_project.operational_settings
.venv/Scripts/python.exe manage.py check_integrations --settings=nongsan_project.operational_settings
powershell -ExecutionPolicy Bypass -File .\start-windows.ps1
```

Mo http://127.0.0.1:8000. Ctrl+C de dung. Script kiem tra cau hinh, mat khau
quan tri demo, migration va thu gom static truoc khi chay. `serve.py` cung kiem
tra mat khau khi chay truc tiep. MySQL phai hoat dong truoc.

`check_integrations` gui mot cau hoi thu nghiem ngan, khong gui du lieu khach hang.
HTTP 200 voi noi dung moi duoc tinh PASS; danh sach model hoac fallback khong
duoc tinh la Gemini thanh cong. GEMINI_MODEL mac dinh la gemini-2.5-flash.
GEMINI_API_KEY chi doc tu moi truong, gui trong header, khong nam trong URL/log.
Neu loi, chatbot co the tra loi theo quy tac; day khong phai phan hoi Gemini.

## Thanh toan

COD su dung duoc. VietQR chi hien trong ban van hanh khi co BANK_ID,
ACCOUNT_NO va ACCOUNT_NAME; cau hinh dung cac bien VIETQR_* trong `.env`.
Chu cua hang phai xac nhan tai khoan nhan tien truoc khi cho khach chuyen khoan.
Anh bill do khach tai len khong chung minh ngan hang da nhan tien.
Nhan vien can doi soat thuc te truoc khi xac nhan/giao don.

Webhook HMAC la hop dong tich hop chung, chua phai connector SePay/PayOS.
Khong coi callback mo phong/demo la thanh toan that. Chua co kiem thu giao dich
ngan hang that trong dot nay.

## Van hanh hang ngay

```powershell
.venv/Scripts/python.exe manage.py cleanup_quotas --settings=nongsan_project.operational_settings
.venv/Scripts/python.exe manage.py clearsessions --settings=nongsan_project.operational_settings
```

GET /health/ tra 200 neu database san sang, 503 neu ket noi loi. Log ung dung:
`logs/app.log`, xoay vong 10 MB, giu 5 ban. Theo doi loi 500, fallback AI,
ton kho, lo sap het han va don cho xac nhan trong dashboard.

Sao luu MySQL va thu muc media cung thoi diem khi tam dung ghi du lieu.
Dung MySQL Workbench export vao noi luu rieng co kiem soat truy cap; luu `.env`
trong kho bi mat rieng. Khong commit backup/media/.env. Kiem thu restore tren
database va thu muc media rieng truoc khi dua vao su dung; chua kiem thu restore
trong dot nay. Khong restore de len database dang chay.

## Gioi han

Chua thiet lap Windows Service/tu khoi dong, backup tu dong, HTTPS/public domain,
monitoring ngoai may, thanh toan ngan hang that hay kiem thu tai dai han.
`production_settings` co rang buoc HTTPS/host/DB user; khong tu dong bien ban
loopback thanh website cong khai. Can review proxy, backup, quyen DB va bao mat
truoc khi public. Xem OPERATIONAL_VERIFICATION.md cho ket qua thuc te.
