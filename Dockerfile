FROM python:3.11-slim

# تنظیم دایرکتوری کاری
WORKDIR /app

# اضافه کردن دایرکتوری کاری به مسیر ماژول‌های پایتون
ENV PYTHONPATH=/app

# نصب proxy.py
RUN pip install --no-cache-dir proxy.py

# کپی کردن فایل پلاگین به داخل کانتینر
COPY filter_plugin.py /app/

# باز کردن پورت 8443
EXPOSE 8443