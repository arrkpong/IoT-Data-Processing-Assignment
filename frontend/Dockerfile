# frontend/Dockerfile
# ใช้ Node.js 20 เป็น Base Image
FROM node:20

# กำหนด working directory
WORKDIR /app

# คัดลอกเฉพาะ package.json และ lock file
COPY package*.json ./

# ติดตั้ง dependencies
RUN npm install

# คัดลอกโค้ดทั้งหมด
COPY . .

# เปิดพอร์ต Vite dev server (5173)
EXPOSE 5173

# ให้ Vite รับ request จาก network อื่นได้ (```--host```)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]