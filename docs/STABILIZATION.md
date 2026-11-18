# Kiem chung on dinh luong hien co

Ngay: 18/11/2026. Pham vi: on dinh tinh nang hien co, khong mo rong san pham.

## Thay doi va bang chung TDD

| Luong | Bang chung | Ket qua |
| --- | --- | --- |
| Quyen tra don, CSRF, dau vao, ton kho, QR | RED `852bf94`, GREEN `f5c7973`; `tests/test_regressions.py` | Da sua |
| Bill rieng tu, Excel, retry AI/chat | RED `de091ee`, GREEN `25a8bb3` | Da sua |
| Nhieu phien chat cu | RED: MultipleObjectsReturned trong test them tai `693db72`; GREEN: test don PASS sau chon phien moi nhat | Da sua, giu lich su cu |
| Dang ky tu dong dang nhap | Test tai `25a8bb3`: profile tra 302 thay vi 200; GREEN `638e978`: 4 test account/provider PASS | Chi save form mot lan, giu session hash hop le |
| Menu tablet | RED browser 1024 px: scrollWidth 1070; GREEN `638e978`: scrollWidth 1009, menu mo duoc | Doi breakpoint thu gon sang xl |
| Tranh chap MySQL | `tests/test_concurrency.py`: 2 test PASS | Hai lan mua dong thoi chi mot lan thanh cong; hai lan huy chi hoan kho mot lan |

Test su dung database MySQL ngau nhien va media trong bo nho. Khong seed/xoa du lieu kinh doanh.
Migration `chatbot.0002_chatrequest` chi them bang va unique constraint; da ap dung local.

## Lenh kiem tra

Ket qua cuoi: **99/99 test PASS**, 118,120 giay; coverage **82,89%** gom statement va branch,
loai test va migration. Nguong `--fail-under=80`: PASS. Log local: `tools/stability-tests.log`;
du lieu coverage local: `tools/stability.coverage`. Hai tep nay duoc gitignore.

Chay bang Python cua virtualenv (`.venv/Scripts/python.exe` tren Windows):

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate --check
python -m pip check
python -m coverage run --branch --source=apps,nongsan_project --omit="*/tests/*,*/migrations/*" manage.py test --settings=nongsan_project.test_settings --noinput
python -m coverage report --precision=2 --fail-under=80
node --check static/js/chatbot.js
```

Ruff: `--isolated --select E4,E7,E9,F,I` tren cac file Python thay doi so voi `92bdac6`: PASS.
Compile Python, Django check, dependency check, migration consistency va JavaScript syntax: PASS.
Pyright bon file bootstrap/runtime/test settings: PASS, 0 loi.
Pyright `apps nongsan_project tests`: FAIL, 77 chan doan. Nhieu chan doan lien quan reverse relations,
thuoc tinh model va admin dong cua Django; chua phan loai/chinh sua het. Khong tat cac canh bao de tao PASS gia.

## Browser va bao mat

- Browser local: trang chu desktop, trang chu/san pham/dang nhap 390 px tai duoc; khong tran ngang o cac man hinh da kiem tra sau sua.
- Menu tablet 1024 px dong/mo khong tran ngang; khong thay console error/warning trong cac trang da doc console.
- Chua chay checkout/upload/chat end-to-end bang browser co dang nhap; cac luong nay co test tich hop Django.
- Quet mau khoa API thong dung trong apps, settings, static, templates, tests va .env.example: khong thay ket qua. Day khong phai audit bao mat/CVE toan dien.
- `check --deploy`: 6 canh bao local (DEBUG, secret key, HSTS, SSL redirect, session/CSRF secure cookie). Chua du dieu kien production.
- Chua kiem chung Gemini/Groq that hoac tien vao ngan hang. Test provider dung mock, test thuong dung fallback.

## Quy tac van hanh

- Pending -> confirmed/cancelled; confirmed -> shipping; shipping -> delivered. Huy chi duoc tu pending.
- Duyet VietQR can bill hop le hoac nhan vien chu dong xac nhan da doi soat. Anh bill khong tu chung minh tien da vao tai khoan.
- Django Admin khong cho sua truc tiep gia/tong tien/trang thai/items de bo qua dich vu ton kho. Duyet bang action; chuyen trang thai bang Dashboard.
- Chi chu don hoac staff doc duoc bill qua Django. Reverse proxy **phai chuyen `/media/payment_proofs/` vao Django**, khong phuc vu cong khai thu muc nay. Bill hien tra dang tep tai xuong; can kiem tra preview tren browser muc tieu.
- Chat co request_id chong lap cho nguoi dang nhap; cung ID khac noi dung tra 409. Cac request cung user duoc tuan tu hoa, gom thoi gian cho AI.
- AI chi thu mot model, Groq khong retry. Timeout la timeout I/O cua SDK/HTTP, khong phai cam ket deadline tong the.
- KPI gia tri don tinh don khong bi huy, khong dong nghia doanh thu da thu. Phan nhom khach hang giu chinh sach hien co.
- QR duoc tao lai khi doi ma lo. Tep QR cu duoc giu lai de tranh xoa tep trong transaction rollback.

## Checklist nghiem thu

- [x] Cai/chay: dependency va test isolation, migration local, system check.
- [x] Quyen/dau vao: tra don dung chu, CSRF, so luong/gia/rating, anh bill hop le <= 5 MB.
- [x] Don/ton kho: transaction, khoa dong, chuyen trang thai chung, test MySQL dong thoi.
- [x] Luong lien quan: dang ky session, QR, Excel text, AI fallback, request id, goi y bu thieu.
- [x] Smoke browser: trang cong khai desktop/mobile va menu tablet.
- [x] Regression va coverage: 99 test PASS, 82,89% >= 80%.
- [ ] Type check toan du an: hoan thanh khi 77 chan doan duoc phan loai/sua va lenh Pyright dat.
- [ ] E2E browser dang nhap: checkout COD/VietQR, bill, duyet, huy, chatbot tren database fixture rieng.
- [ ] Nghiem thu moi truong dich: HTTPS, private media, khoa bi mat va AI/ngan hang theo cau hinh thuc te.

Khong tu dong trien khai, khong sua `.env`, khong thay doi `docs/diagrams/` cua nguoi dung.
