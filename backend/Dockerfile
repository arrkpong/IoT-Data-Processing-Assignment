# backend\Dockerfile
# ใช้ Python 3.13.2 เป็น Base Image
FROM python:3.13.2

# กำหนด working directory ใน container
WORKDIR /app

# ติดตั้ง dependencies ที่จำเป็นสำหรับการคอมไพล์และฐานข้อมูล
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# คัดลอก requirements.txt ลงใน container
COPY requirements.txt .

# ติดตั้ง dependencies จาก requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมดไปยัง working directory
COPY . .

# เปิดพอร์ต 8000 สำหรับ Django
EXPOSE 8000

# คำสั่งเริ่มต้นเพื่อรัน Django โดยใช้ development server (ไม่แนะนำใน production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
