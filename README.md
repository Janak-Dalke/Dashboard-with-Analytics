# 📊 pulse.analytics — AI-Powered Analytics Dashboard

> A full-stack analytics dashboard built with **Streamlit** and **Groq AI (LLaMA 3.3)** that lets you upload any CSV or JSON dataset and instantly generates smart charts, KPIs, and insights — automatically.

---

## 🖥️ Live Demo

```
http://YOUR_EC2_PUBLIC_IP:8501
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 **Overview Dashboard** | 4 KPI cards + 4 interactive Plotly charts with mock business data |
| 🤖 **AI Analysis** | Upload any CSV/JSON — Groq AI analyzes and generates charts automatically |
| 📈 **Dynamic Charts** | Line, Bar, Doughnut, Radar charts generated from your real data |
| 💡 **AI Insights** | Executive summary, 4 key insights, extracted KPIs per dataset |
| 🎨 **Dark UI** | Professional dark theme built with custom CSS + Plotly |
| 🔒 **Secure** | API key stored in `.env` — never hardcoded or exposed |

---

## 🛠️ Tech Stack

```
Frontend + Backend   →   Streamlit (Python)
Charts               →   Plotly
AI Engine            →   Groq API (LLaMA 3.3 70B)
Deployment           →   AWS EC2 (Ubuntu 22.04)
Process Manager      →   systemd
```

---

## 📁 Project Structure

```
pulse-analytics/
├── app.py                  ← Main Streamlit application
├── requirements.txt        ← Python dependencies
├── .env                    ← API keys (NOT uploaded to GitHub)
├── .env.example            ← Template showing required env vars
├── .gitignore              ← Protects secrets from git
└── .streamlit/
    └── config.toml         ← Streamlit dark theme config
```

---

## ⚡ Quick Start (Local)

### 1. Clone the repository
```bash
git clone https://github.com/Janak-Dalke/Dashboard-with-Analytics.git
cd Dashboard-with-Analytics
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root folder:
```env
GROQ_API_KEY=gsk_your_groq_key_here
```
Get your **free** Groq API key at 👉 [console.groq.com/keys](https://console.groq.com/keys)

### 5. Run the app
```bash
streamlit run app.py
```

Open 👉 **http://localhost:8501**

---

## 🚀 AWS EC2 Deployment

### Step 1 — Launch EC2 Instance
- **AMI:** Ubuntu Server 22.04 LTS
- **Instance type:** t2.micro (free tier)
- **Security Group ports:** `22` (SSH), `8501` (Streamlit), `80` (HTTP)

### Step 2 — Connect to Server
```bash
ssh -i "your-key.pem" ubuntu@YOUR_PUBLIC_IP
```

### Step 3 — Install & Setup
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y

git clone https://github.com/Janak-Dalke/Dashboard-with-Analytics.git
cd Dashboard-with-Analytics

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env with your key
echo "GROQ_API_KEY=gsk_your_key_here" > .env
```

### Step 4 — Run as a Service (24/7)
```bash
sudo nano /etc/systemd/system/streamlit.service
```

Paste:
```ini
[Unit]
Description=pulse.analytics Streamlit Dashboard
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Dashboard-with-Analytics
Environment="PATH=/home/ubuntu/Dashboard-with-Analytics/venv/bin"
EnvironmentFile=/home/ubuntu/Dashboard-with-Analytics/.env
ExecStart=/home/ubuntu/Dashboard-with-Analytics/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit
sudo systemctl status streamlit
```

✅ App is live at `http://YOUR_PUBLIC_IP:8501`

---

## 🔧 Useful Commands

```bash
# Check app status
sudo systemctl status streamlit

# Restart after changes
sudo systemctl restart streamlit

# View live logs
sudo journalctl -u streamlit -f

# Pull latest code + restart
git pull && sudo systemctl restart streamlit

# Stop the app
sudo systemctl stop streamlit
```

---

## 📊 How AI Analysis Works

```
1. Upload CSV or JSON file
         ↓
2. Dataset sent to Groq API (LLaMA 3.3 70B)
         ↓
3. AI returns structured JSON with:
   • Executive summary
   • 4 key insights
   • 3–4 KPI metrics
   • 3–5 recommended charts
         ↓
4. Streamlit renders dynamic Plotly charts
```

---

## 🌐 Supported Data Formats

| Format | Example |
|---|---|
| CSV | `sales.csv`, `users.csv` |
| JSON | `data.json`, `kaggle.json` |
| Plain text | Comma-separated `.txt` |
| Paste | Raw CSV/JSON pasted directly |

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | Free key from [console.groq.com/keys](https://console.groq.com/keys) |

---

## 💰 Cost Estimate

| Resource | Cost |
|---|---|
| AWS EC2 t2.micro (12 months) | **FREE** |
| Groq API | **FREE** (14,400 req/day) |
| AWS EC2 t2.micro (after 12 months) | ~$8/month |

---

## 🔒 Security Notes

- ✅ API key stored in `.env` — never committed to git
- ✅ `.gitignore` blocks `.env` from GitHub
- ✅ EC2 port `22` restricted to your IP only
- ⚠️ For production: add HTTPS via Nginx + Let's Encrypt

---

## 📦 Dependencies

```
streamlit==1.35.0
plotly==5.22.0
pandas==2.2.2
requests==2.31.0
python-dotenv==1.0.1
```

---

## 🙋 Troubleshooting

**App not loading on EC2?**
```bash
# Check if port 8501 is open in AWS Security Group
# Check service logs
sudo journalctl -u streamlit -f
```

**Groq API error?**
```bash
# Verify key is set
cat .env
# Get new key at console.groq.com/keys
```

**Module not found?**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 👨‍💻 Author

**Janak Dalke**
- GitHub: [@Janak-Dalke](https://github.com/Janak-Dalke)

---

## 📄 License

MIT License — free to use and modify.

---

<div align="center">
Built with ❤️ using Streamlit + Groq AI + AWS EC2
</div>