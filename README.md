سامانه مدیریت موجودی (FastAPI + SQLAlchemy)






معرفی پروژه

این پروژه یک سامانه کامل مدیریت موجودی است که با FastAPI و SQLAlchemy ساخته شده و APIهایی برای مدیریت موارد زیر ارائه می‌دهد:

محصولات: بازی‌ها، کنسول‌ها، مانیتورها، هدست‌ها و غیره

تأمین‌کنندگان: ثبت، ویرایش و پیگیری عملکرد تأمین‌کنندگان

سفارشات خرید: ایجاد سفارش، مدیریت وضعیت و بروزرسانی موجودی پس از دریافت

فروش: سیستم چک‌اوت با بررسی موجودی و ثبت جزئیات فروش

کاربران: نقش‌های admin و customer با احراز هویت JWT

گزارشات: داشبورد شامل تعداد محصولات، موجودی کم، آمار فروش، پرفروش‌ترین محصولات و وضعیت سفارشات

این پروژه همچنین با Docker آماده اجرا است.

ویژگی‌ها
۱. محصولات

ایجاد، ویرایش و حذف محصولات

جستجو و فیلتر بر اساس نام، SKU، دسته‌بندی و قیمت

مرتب‌سازی و صفحه‌بندی

فیلتر بر اساس دسته‌بندی و محدوده قیمت

۲. تأمین‌کنندگان

افزودن تأمین‌کننده جدید

ویرایش اطلاعات تأمین‌کننده

غیرفعال‌سازی تأمین‌کننده (soft delete)

امتیازدهی تأمین‌کننده بر اساس سرعت تحویل سفارش‌ها

۳. سفارشات خرید

ایجاد سفارش با چندین آیتم

مدیریت وضعیت سفارش: Draft، Sent، Received، Closed

بروزرسانی خودکار موجودی هنگام دریافت سفارش

بروزرسانی امتیاز تأمین‌کننده بر اساس زمان تحویل

۴. فروش

چک‌اوت با بررسی موجودی

کسر خودکار موجودی از انبار

ثبت جزئیات کامل فروش

۵. کاربران و احراز هویت

ثبت‌نام و ورود (JWT)

نقش‌ها: admin و customer

اعتبارسنجی رمز عبور (حداقل ۸ کاراکتر شامل حروف و عدد)

۶. گزارشات

داشبورد شامل:

تعداد کل محصولات

تعداد محصولات با موجودی کم

تعداد کل سفارشات خرید و فروش

پرفروش‌ترین محصولات

تعداد سفارش‌ها بر اساس وضعیت

زمان تولید گزارش

فناوری‌های استفاده شده

Python 3.11

FastAPI

SQLAlchemy ORM

SQLite (قابل جایگزینی با MySQL/PostgreSQL)

Docker

JWT Authentication

Pydantic Schemas

Uvicorn (ASGI server)

نصب و اجرا
۱. کلون کردن پروژه
git clone https://github.com/alijafari895/TERM_PROJECT.git
cd TERM_PROJECT

۲. ساخت فایل .env

یک فایل .env بر اساس .env.example بسازید:

cp .env.example .env


مقادیر کلیدها را با مقادیر واقعی خود پر کنید.

۳. نصب وابستگی‌ها
pip install -r requirements.txt

۴. اجرای پروژه با Uvicorn
uvicorn main:app --reload


API در آدرس http://127.0.0.1:8000 در دسترس خواهد بود.

۵. اجرای پروژه با Docker (اختیاری)
docker build -t inventory_app .
docker run -p 8000:8000 inventory_app

مستندات API

پس از اجرای سرور، می‌توانید مستندات تعاملی را مشاهده کنید:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

مسیرهای اصلی API:

منبع	Prefix
کاربران	/users
محصولات	/products
تأمین‌کنندگان	/suppliers
سفارشات خرید	/purchase-orders
فروش	/sales
گزارشات	/reports
متغیرهای محیطی (.env)
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///./database.db
ACCESS_TOKEN_EXPIRE_MINUTES=60


SECRET_KEY: برای تولید JWT

DATABASE_URL: رشته اتصال به دیتابیس

ACCESS_TOKEN_EXPIRE_MINUTES: زمان انقضای توکن

مدل‌های دیتابیس

User: id, username, email, full_name, hashed_password, role

Product: id, name, sku, price, category, quantity, min_threshold, image_url

Supplier: id, name, email, phone, delivery_days, rating, rating_count, is_active

PurchaseOrder: id, supplier_id, status, created_at, received_at, delivery_time_days

PurchaseOrderItem: id, order_id, sku, name, quantity

Sale: id, customer_id, total, created_at

SaleItem: id, sale_id, sku, quantity, price

نحوه محاسبه امتیاز تأمین‌کننده

هر سفارش دریافتی امتیاز تأمین‌کننده را به‌روزرسانی می‌کند:

𝑠
𝑐
𝑜
𝑟
𝑒
=
𝑚
𝑎
𝑥
(
0
,
𝑚
𝑖
𝑛
(
5
,
5
−
(
𝑑
𝑒
𝑙
𝑖
𝑣
𝑒
𝑟
𝑦
_
𝑑
𝑎
𝑦
𝑠
/
7
)
)
)
score=max(0,min(5,5−(delivery_days/7)))

امتیاز نهایی میانگین پویا تمام سفارشات است.

لایسنس

این پروژه تحت MIT License منتشر شده است.

💡 نکته ارائه:

می‌توانید نموداری از جریان سفارش → موجودی → فروش → گزارشات رسم کنید تا در جلسه ارائه بهتر نمایش داده شود.

نقش‌ها و احراز هویت JWT را توضیح دهید و نشان دهید چگونه دسترسی به API مدیریت می‌شود.