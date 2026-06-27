# 🧠 MindRise AI – Backend API

Scalable **Django REST API backend** for an AI-powered mobile application focused on user onboarding, personalized experiences, subscription management, and notification systems.

🔗 **GitHub Repository**: https://github.com/TechbyAbrar/mindrise_ai.git
🎨 **Figma Design**: https://www.figma.com/design/OPGlAqtKKmfXaZrIXZVMwG/kalataylor514-%7C%7C-MindRiseAI
🌐 **Live Link**: *(Will be added soon)*

---

## 📌 Overview

MindRise AI is a backend system designed for a **mobile-first AI application** that focuses on:

* personalized onboarding flows
* user engagement
* subscription-based access
* notification systems

The architecture is built to support:

* AI integrations (LLM / recommendation systems)
* scalable mobile APIs
* SaaS-style product growth

---

## 🧠 Core Features

* 🔐 JWT Authentication (SimpleJWT)
* 👤 Custom User Model (`account.UserAuth`)
* 🔑 Multi-login (email / phone / username)
* 🧭 Onboarding System (user journey flows)
* 💳 Subscription Management (Stripe-ready)
* 🔔 Notification Module
* 📧 Email Integration (SMTP)
* 🧾 Logging System (rotating logs)
* ⚡ Static file handling (WhiteNoise)
* 📡 API Documentation (drf-spectacular)

---

## 🏗️ Architecture Overview

Client (Mobile App)
↓
Frontend (Figma-based UI)
↓
Django REST API Backend
↓
-

| Auth Layer (JWT + Custom Backend)      |
| Onboarding & User Flow Engine          |
| Subscription & Access Control          |
| Notification System                   |
| Logging & Monitoring                  |
-----------------------------------------

```
    ↓
```

PostgreSQL Database
↓
External Services:

* Stripe API
* SMTP Email Server

---

## ⚙️ Tech Stack

| Category     | Technology            |
| ------------ | --------------------- |
| Language     | Python 3.11+          |
| Framework    | Django 5.2.x          |
| API          | Django REST Framework |
| Auth         | Simple JWT            |
| Database     | PostgreSQL            |
| Static Files | WhiteNoise            |
| Logging      | Timed Rotating Logs   |
| API Docs     | drf-spectacular       |
| Payments     | Stripe API            |

---

## 📁 Project Structure

```text
core/
account/
onboarding/
privacy/
subscription/
notification/

media/
staticfiles/
logs/

manage.py
requirements.txt
README.md
```

---

## 🔐 Authentication System

Supports login via:

* email
* phone
* username

### JWT Configuration

* Access Token: 15 days
* Refresh Token: 30 days
* Bearer token authentication

---

## 🧭 Onboarding Flow

1. User registers
2. Onboarding steps executed
3. Preferences stored
4. Personalized experience configured

---

## 💳 Subscription Flow

1. User selects plan
2. Stripe session created
3. Payment processed
4. Access granted

---

## 🔔 Notification System

* Designed for user engagement
* Can be extended for:

  * push notifications
  * email triggers
  * in-app alerts

---

## 📊 API Features

* JWT-secured endpoints
* Modular API design
* Schema documentation (Swagger)
* Scalable architecture

---

## 📡 API Documentation

```text
/api/schema/swagger-ui/
```

---

## 🌐 Environment Configuration

Create `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=False

DATABASE_URL=postgres://user:password@host:port/dbname

EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password

STRIPE_SECRET_KEY=your-secret
STRIPE_PUBLIC_KEY=your-public
STRIPE_WEBHOOK_SECRET=your-webhook
```

---

## 🚀 Installation & Setup

```bash
git clone https://github.com/TechbyAbrar/mindrise_ai.git
cd mindrise_ai

python -m venv env
source env/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

## 🚀 Production Deployment (ASGI)

### Run with Gunicorn + Uvicorn

```bash
gunicorn core.asgi:application \
  --worker-class uvicorn.workers.UvicornWorker \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

---

### Debug Mode (Development)

```bash
gunicorn core.asgi:application \
  --worker-class uvicorn.workers.UvicornWorker \
  --workers 1 \
  --bind 0.0.0.0:8000 \
  --log-level debug
```

---

## 🧾 Logging System

* Logs stored in `/logs/app.log`
* Rotates daily (5-day retention)
* Captures:

  * API activity
  * errors
  * system events

---

## 🖼️ Screenshots

```md
![App Preview](assets/images/dashboard.png)
```

---

## 🧪 Future Improvements

* AI integration (LLM-based personalization)
* push notification system
* real-time user activity tracking
* background jobs (Celery)
* Redis caching
* Docker deployment
* recommendation engine

---

## 🔐 Security Notes

* Move `SECRET_KEY` to `.env`
* Avoid `DEBUG=True` in production
* Restrict `ALLOWED_HOSTS`
* Limit CORS origins
* Enable HTTPS

---

## 🤝 Contribution

Pull requests are welcome.

---

## 📄 License

MIT License

---

## 👨‍💻 Author

**Abrar (TechbyAbrar)**
Backend Engineer | Django | FastAPI | AI Systems

🔗 GitHub: https://github.com/TechbyAbrar
