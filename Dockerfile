FROM python:3.11-slim

# تنظیم دایرکتوری کاری
WORKDIR /app

# نصب proxy.py
RUN pip install --no-cache-dir proxy.py

# کپی کردن فایل پلاگین به داخل کانتینر
COPY filter_plugin.py /app/

# باز کردن پورت 443
EXPOSE 443