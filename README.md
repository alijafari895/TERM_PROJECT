
# Inventory Management System - Complete (AP-Project-1404 compliant)

این نسخه کامل شده و شامل قابلیت‌های زیر است:
- ثبت‌نام با ایمیل، نام کامل، اعتبارسنجی رمز (حداقل 8 کاراکتر با حروف و اعداد)
- JWT شامل username، role، user_id
- محصولات: فیلد category، تصویر (URL)، دسته‌بندی، جستجو، فیلتر، مرتب‌سازی، صفحه‌بندی
- تأمین‌کننده: ثبت، غیرفعال‌سازی و امتیازدهی مبتنی بر زمان تحویل
- سفارش خرید: مراحل Draft, Sent, Received, Closed — هنگام Received، موجودی به‌صورت خودکار افزایش می‌یابد
- سفارش فروش / Checkout: مشتری می‌تواند خرید کند، قبل از خرید موجودی چک شده و پس از خرید کاهش می‌یابد
- گزارشات: داشبورد برای ادمین، کالاهای کم‌موجودی، پرفروش‌ترین کالاها، آمار سفارش‌ها
- فایل `.env.example` اضافه شده

## اجرا
1. محیط مجازی و نصب dependencies:
```
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```
2. (اختیاری) فایل `.env` بساز و متغیرها را از `.env.example` کپی کن
3. اجرای سرور:
```
uvicorn main:app --reload
```
