# 🎯 Quizzly – AI-Powered Quiz Generation from YouTube Videos

A **Django REST Framework** based backend that automatically generates quizzes from YouTube videos.  
Users provide a YouTube URL, the system transcribes the audio using Whisper AI, and generates quiz questions using Google's Gemini AI.  
This project provides a **fully functional REST API** ready to connect to a frontend (e.g. Angular, React, or Vue).

---

## 🚀 Features
- 🔐 User authentication via JWT tokens (login/register with HTTP-only cookies)
- 🎥 YouTube video audio extraction and transcription
- 🤖 AI-powered quiz generation using Google Gemini
- 📝 Automatic creation of multiple-choice questions
- 🧩 RESTful API endpoints for easy integration
- 💾 Quiz storage with questions and answers

---

## 🧰 Requirements

Before starting, make sure you have:

| Requirement | Description |
|--------------|-------------|
| **Python ≥ 3.12** | Required to run Django |
| **pip** | Python's package manager |
| **git** | To clone this repository |
| **ffmpeg** | Required for audio extraction from YouTube videos |
| **virtualenv** *(optional but recommended)* | To isolate project dependencies |
| **Google Gemini API Key** | For AI quiz generation |

---

## 💻 Setup Instructions (All Operating Systems)

The following steps work on **Windows, macOS, and Linux**.

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/Quizzly.git
cd Quizzly_project
```

### 2️⃣ Create a virtual environment
#### 🪟 On Windows
```bash
python -m venv venv
venv\Scripts\activate
```
#### 🍎 On macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Install ffmpeg
#### 🪟 On Windows
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

#### 🍎 On macOS
```bash
brew install ffmpeg
```

#### 🐧 On Linux
```bash
sudo apt install ffmpeg
```

### 5️⃣ Configure environment variables
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_google_gemini_api_key_here
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### 6️⃣ Set up the database
Create all required tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7️⃣ Create a superuser (admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.

### 8️⃣ Run the development server
```bash
python manage.py runserver
```
and open: 
```
http://127.0.0.1:8000/
```
---

## 🧩 Project Structure
```
Quizzly_project/
│
├── quiz_app/                  # Main Django app
│   ├── models.py             # Quiz and Question models
│   ├── api/
│       ├── serializers.py    # Serializers for Quiz and Question
│       ├── views.py          # API logic for quiz generation
│       ├── urls.py           # App-specific routes
│
├── auth_app/                  # Authentication app
│   ├── api/
│       ├── serializers.py    # User registration and login serializers
│       ├── views.py          # JWT authentication with HTTP-only cookies
│       ├── urls.py           # Auth routes
│
├── quizzly_core/             # Main Project settings
│   ├── settings.py           # Global configuration
│   ├── urls.py               # Root URL routes
│
├── manage.py                 # Django management script
├── requirements.txt          # Dependencies list
└── README.md                 # This file
```
---

## 🔑 Authentication
This project uses **JWT Authentication with HTTP-only cookies**.
After registering or logging in, you'll receive tokens stored in secure cookies:
```json
{
  "detail": "Login successfully.",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```
Tokens are automatically included in subsequent requests via cookies.

---

## 🔗 Example API Endpoints

| Method | Endpoint                    | Description                             |
| ------ | --------------------------- | --------------------------------------- |
| `POST` | `/api/auth/register/`       | Register new user                       |
| `POST` | `/api/auth/login/`          | Log in and receive JWT tokens in cookies|
| `POST` | `/api/auth/refresh/`        | Refresh access token                    |
| `POST` | `/api/quizzes/`             | Generate quiz from YouTube URL          |
| `GET`  | `/api/quizzes/`             | List all quizzes                        |
| `GET`  | `/api/quizzes/<id>/`        | Get quiz details with questions         |

---

## 📋 Quiz Generation Flow

1. **User submits YouTube URL** via POST to `/api/quizzes/`
2. **Audio extraction** - yt-dlp downloads audio from YouTube
3. **Transcription** - Whisper AI converts audio to text
4. **Quiz generation** - Google Gemini AI creates 10 questions based on transcript
5. **Storage** - Quiz and questions are saved to database
6. **Response** - Complete quiz with questions returned to user

---

## 🧪 Testing the API

You can test all endpoints using:
- **Postman** - Import the API collection
- **Insomnia** - REST client
- **Django's built-in API browser** - Visit endpoints in your browser
- **cURL** - Command line testing

---

## 🤖 AI Models Used

- **Whisper (faster-whisper)** - Audio transcription (small model for CPU)
- **Google Gemini 2.5 Flash** - Quiz question generation

---

## 📦 Key Dependencies

- Django REST Framework
- djangorestframework-simplejwt
- yt-dlp
- faster-whisper
- google-generativeai

---

## 🛠️ Troubleshooting

**Audio extraction fails:**
- Ensure ffmpeg is installed and in PATH

**Transcription is slow:**
- Consider using GPU acceleration or a smaller Whisper model

**Gemini API errors:**
- Verify your API key is valid and has sufficient quota

---
