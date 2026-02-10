# Asset Management API — Cashback Credit Pool

## 📌 Project Overview

This project implements a production-grade backend system for managing limited cashback wallet assets.

The platform issues cashback credits such as:

- Signup rewards  
- Referral bonuses  
- Promotional wallet credits  

Each cashback asset behaves like a financial credit and can only be claimed once by a single authenticated user.

The system is designed to maintain strict data integrity and prevent duplicate ownership even under concurrent claim attempts.

---

## 🧠 Assessment Context

This project was built as part of a technical evaluation.

### Objective

Build an Asset Management API that ensures:

- Secure user authentication  
- Concurrency-safe asset claiming  
- Relational claim history tracking  
- Perfect financial consistency  

---

## 🧩 Tasks Implemented

### 1️⃣ User Authentication

- JWT-based authentication
- User registration & login
- Protected claim APIs
- Role-based access control (Admin / User)

---

### 2️⃣ Concurrency & Data Integrity

To prevent duplicate claims:

- PostgreSQL transactions used
- Row-level locking (`SELECT ... FOR UPDATE`)
- Atomic claim execution
- Ledger-backed audit trail

---

### 3️⃣ Relational Queries

Efficient joins implemented for:

- User claim history
- Global voucher ownership
- Admin audit views

---

### 4️⃣ Admin Asset Lifecycle

Admin can:

- Create assets
- Update unclaimed assets
- Delete unclaimed assets
- Expire assets
- Recreate expired supply
- View voucher ownership

Claimed assets remain immutable to preserve audit integrity.

---

### 5️⃣ Ledger System

Every claim is recorded in an immutable ledger table containing:

- Asset ID
- User ID
- Amount
- Timestamp

This ensures financial traceability.

---

### 6️⃣ Background Expiry Scheduler

Automated expiry jobs mark assets as expired based on `expires_at` timestamps.

---

### 7️⃣ Rate Limiting & Locking (Optional Infra)

The system includes:

- Redis-based distributed locks
- Redis-backed rate limiting

However…

> Redis is **optional** and the system gracefully falls back to in-memory protection if Redis is not installed.

This ensures zero setup friction for reviewers.

---

# 🏗️ Tech Stack

| Layer | Technology |
|------|-------------|
Backend | Flask |
Database | PostgreSQL |
ORM | SQLAlchemy |
Auth | JWT |
Migrations | Alembic |
Scheduler | APScheduler |
Limiter | Flask-Limiter |
Locking | Redis (optional) |
Frontend | Jinja Templates |

---

# 📂 Project Structure
# Asset Management API — Cashback Credit Pool

## 📌 Project Overview

This project implements a production-grade backend system for managing limited cashback wallet assets.

The platform issues cashback credits such as:

- Signup rewards  
- Referral bonuses  
- Promotional wallet credits  

Each cashback asset behaves like a financial credit and can only be claimed once by a single authenticated user.

The system is designed to maintain strict data integrity and prevent duplicate ownership even under concurrent claim attempts.

---

## 🧠 Assessment Context

This project was built as part of a technical evaluation.

### Objective

Build an Asset Management API that ensures:

- Secure user authentication  
- Concurrency-safe asset claiming  
- Relational claim history tracking  
- Perfect financial consistency  

---

## 🧩 Tasks Implemented

### 1️⃣ User Authentication

- JWT-based authentication
- User registration & login
- Protected claim APIs
- Role-based access control (Admin / User)

---

### 2️⃣ Concurrency & Data Integrity

To prevent duplicate claims:

- PostgreSQL transactions used
- Row-level locking (`SELECT ... FOR UPDATE`)
- Atomic claim execution
- Ledger-backed audit trail

---

### 3️⃣ Relational Queries

Efficient joins implemented for:

- User claim history
- Global voucher ownership
- Admin audit views

---

### 4️⃣ Admin Asset Lifecycle

Admin can:

- Create assets
- Update unclaimed assets
- Delete unclaimed assets
- Expire assets
- Recreate expired supply
- View voucher ownership

Claimed assets remain immutable to preserve audit integrity.

---

### 5️⃣ Ledger System

Every claim is recorded in an immutable ledger table containing:

- Asset ID
- User ID
- Amount
- Timestamp

This ensures financial traceability.

---

### 6️⃣ Background Expiry Scheduler

Automated expiry jobs mark assets as expired based on `expires_at` timestamps.

---

### 7️⃣ Rate Limiting & Locking (Optional Infra)

The system includes:

- Redis-based distributed locks
- Redis-backed rate limiting

However…

> Redis is **optional** and the system gracefully falls back to in-memory protection if Redis is not installed.

This ensures zero setup friction for reviewers.

---

# 🏗️ Tech Stack

| Layer | Technology |
|------|-------------|
Backend | Flask |
Database | PostgreSQL |
ORM | SQLAlchemy |
Auth | JWT |
Migrations | Alembic |
Scheduler | APScheduler |
Limiter | Flask-Limiter |
Locking | Redis (optional) |
Frontend | Jinja Templates |

---

# 📂 Project Structure

asset-mgmt-api/
│
├── app/
│ ├── models/
│ ├── routes/
│ ├── middleware/
│ ├── utils/
│ ├── jobs/
│ ├── scheduler.py
│ └── init.py
│
├── templates/
├── static/
├── migrations/
├── scripts/
├── run.py
├── requirements.txt
└── README.md


---

# ⚙️ Installation & Setup Guide

Follow these steps to run the project locally.

---

## 1️⃣ Clone Repository

```bash
git clone <repo-url>
cd asset-mgmt-api


---

# ⚙️ Installation & Setup Guide

Follow these steps to run the project locally.

---

## 1️⃣ Clone Repository

```bash
git clone <repo-url>
cd asset-mgmt-api

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup PostgreSQL Database

Create a database manually:

asset_mgmt_db

Update .env file accordingly.
