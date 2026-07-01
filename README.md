# 📈 Price Tracker

REST API service for tracking Wildberries product prices and notifying users about price changes via email.

---

## 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | Async web framework |
| **SQLAlchemy** | ORM |
| **Alembic** | Database migrations |
| **Pydantic** | Data validation and serialization |
| **PostgreSQL 16** | Database |
| **Celery** | Periodic background tasks |
| **Redis** | Message broker |
| **curl_cffi** | Bypassing anti-bot protection |
| **JWT** | Authentication |

---

## ✨ Features

- User registration and JWT authorization
- Add Wildberries products by URL for tracking
- Automatic price parsing via Wildberries CDN API
- Daily price checks via Celery Beat
- Email notifications when price changes
- Full product CRUD

---

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed

### Steps

1. Clone the repository
```bash
git clone https://github.com/nozilis/price-tracker.git
cd price-tracker
```

2. Create `.env` file from example
```bash
cp .env.example .env
```

3. Fill in the required environment variables (see below)

4. Run the application
```bash
docker-compose up --build
```

5. Apply database migrations
```bash
docker-compose exec web alembic upgrade head
```

The API will be available at `http://localhost:8000`

---

## 🔐 Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/price_tracker
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=price_tracker

# Security
SECRET_KEY=your_secret_key

# Redis
BROKER_URL=redis://redis:6379/0

# Email
MAIL_FROM=your@email.com
MAIL_PASSWORD=your_app_password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
```

> See `.env.example` for the full list of required variables.

---

## 📋 API Endpoints

### Auth
| Method | URL | Description | Auth |
|---|---|---|---|
| POST | `/user/register` | Register new user | No |
| POST | `/user/login` | Login, returns JWT token | No |
| PATCH | `/user/{user_id}` | Update profile | ✅ |
| DELETE | `/user/{user_id}` | Delete account | ✅ |

### Products
| Method | URL | Description | Auth |
|---|---|---|---|
| POST | `/products/` | Add product by URL | ✅ |
| GET | `/products/` | Get all tracked products | ✅ |
| DELETE | `/products/{product_id}` | Stop tracking product | ✅ |

### Interactive Docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🏗 Architecture

```
FastAPI (web)
    │
    ├── PostgreSQL — stores users, products, price history
    │
    └── Redis ──── Celery Worker — executes tasks
              └─── Celery Beat  — schedules daily price check
```

**Price check flow:**
```
Celery Beat (daily) → fetch all products → parse price via WB CDN
→ save to PriceHistory → if price changed → update current_price → send email
```

---

## ⚠️ Known Limitations

- Wildberries CDN table is periodically updated — approximately 40% of products are successfully parsed. This is an ongoing improvement area.
- Access token lifetime is 5 minutes — refresh by logging in again.
