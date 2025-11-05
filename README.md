<h1 align="center">🌙 Lofi Radio 24/7 Bot 🎧</h1>

<p align="center">
Bot phát nhạc Lofi Chill 24/7 ✨  
Thư giãn – Tập trung – Code – Học bài 🧠📚  
Hỗ trợ chạy trên VPS / Replit / Render / Docker
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/Streaming-LoFi-blueviolet" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" />
  <img src="https://img.shields.io/github/license/BaoAnh020603/Lofi-Radio-24-7" />
</p>

---

## 🎧 Tính năng

- 🎵 Stream Lofi Chill 24/7 liên tục
- 🔁 Tự động reconnect khi mất kết nối
- 🚀 Hỗ trợ Docker, VPS, Replit, Render
- 🌍 Keep-alive để chạy không ngừng nghỉ
- ✅ Cấu hình dễ dàng, chạy nhanh

---

## 📂 Cấu trúc dự án
📦 Lofi-Radio-24-7
```
┣ 📜 lofi_radio_slash.py -> Code bot chính
┣ 📜 keep_alive.py -> Web keep-alive (Replit/Render)
┣ 📜 requirements.txt -> Python dependencies
┣ 📜 apt-packages.txt -> System packages
┗ 🐳 Dockerfile -> Docker build/deploy
```
---

## ⚙️ Cài đặt
### 1️⃣ Clone repository
```
git clone https://github.com/BaoAnh020603/Lofi-Radio-24-7
cd Lofi-Radio-24-7
```
2️⃣ Cài thư viện
```
pip install -r requirements.txt
```
3️⃣ Tạo file .env
```
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
STREAM_URL=https://your-lofi-stream-url
```
▶️ Chạy bot
```
python lofi_radio_slash.py
Chạy kèm keep-alive (Replit/Render)
python keep_alive.py &
python lofi_radio_slash.py
```
🐳 Docker Deploy
```
docker build -t lofi_radio_bot .
docker run -d --name lofi lofi_radio_bot
```
⚠️ Tôn trọng bản quyền – ưu tiên nguồn stream hợp pháp

🤝 Đóng góp
Pull Requests & Issues được hoan nghênh ❤️
Hãy ⭐ repo để ủng hộ dự án ✨

<p align="center">Made with ☕ + 🌙 for everyone who loves Lofi 🎶</p>
