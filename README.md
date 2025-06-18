# 🧠 SQL Chatbot Project

This is a natural language chatbot that allows users to query a database using plain English. It leverages FastAPI for the backend, LlamaIndex + Groq for generating SQL, and a simple Node.js + HTML frontend.

---

## ⚙️ Technologies Used

- **FastAPI** for serving natural language to SQL chatbot
- **Groq + LlamaIndex** for query generation
- **SQLite** as the sample database
- **Node.js + Express** to serve the frontend
- **Vanilla HTML + JS** UI (optional React-ready)
- **Ngrok** to expose the FastAPI server for public access

---

## 🚀 Quick Setup

> This guide assumes you're using **Google Colab** or a Linux shell.

### 🔧 1. Install Python Dependencies

```bash
# Install LLM-related packages
!pip install -r requirements.txt

# Install Node.js 18
!curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
!apt-get install -y nodejs npm

# Install required Node packages
!npm install express axios dotenv


## 🚦 Run the Full App in Google Colab

After setting up the code and dependencies, run the following commands to:

- ✅ Start FastAPI ()
- ✅ Run Node.js server
- ✅ Expose the app to the internet via `ngrok`

# Start FastAPI server on port 8000 (backend)
!nohup uvicorn app:app --host 0.0.0.0 --port 8000 --reload > fastapi.log 2>&1 &

# Start Node.js server (frontend proxy)
!nohup node /content/server.js > node.log 2>&1 &

### 🔐 Add Your ngrok Auth Token
from pyngrok import ngrok
public_url = ngrok.connect(3000)
print("Access your chatbot at:", public_url)
```

>Now, use the public URL to open the chatbot. 

```bash
!ngrok config add-authtoken "ngrok_authentication_code"
from pyngrok import ngrok
public_url = ngrok.connect(3000)
print("Access your chatbot at:", public_url)
