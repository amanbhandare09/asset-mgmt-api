# Asset Management API — Cashback Credit Pool

## 📌 Domain Overview

This project is built in the domain of **Digital Wallet Cashback Credits**.

Many platforms issue cashback rewards such as:

- Signup bonuses  
- Referral incentives  
- Promotional wallet credits  

These credits behave like financial assets rather than generic coupons because they hold monetary value and can only be claimed once by a single user.

The core challenge is managing a limited pool of such assets while ensuring ownership remains perfectly consistent — even when multiple users attempt to claim the same credit simultaneously.

---

## 🧠 Assessment Objective

Build a backend system where authenticated users manage cashback vouchers while ensuring:

- Secure authentication  
- Concurrency-safe asset claiming  
- Data integrity under high contention  
- Relational visibility of ownership  

---

## 🚧 Problems Being Solved

This system addresses several real-world backend challenges:

- Preventing duplicate claims of the same asset  
- Handling race conditions during simultaneous requests  
- Maintaining financial ownership consistency  
- Recording immutable audit trails  
- Providing relational reporting of claims  

---

## 🛠️ Methodology & Design Approach

My problem-solving approach followed a layered system design:

### 1️⃣ Domain Modeling
Although described as coupons, I treated assets as financial wallet credits to ensure strict ownership handling.

### 2️⃣ Concurrency Risk Identification
Primary risks identified:

- Race conditions  
- Duplicate claims  
- Ownership conflicts  

### 3️⃣ Data Integrity First
Implemented transactional claim execution with PostgreSQL row-level locking (`SELECT FOR UPDATE`) to guarantee atomic ownership assignment.

### 4️⃣ Auditability
Introduced an immutable claims ledger to maintain financial traceability.

### 5️⃣ Access Control
Added JWT authentication and role-based RBAC for Admin vs User operations.

### 6️⃣ Scalability Considerations
Explored distributed locking, rate limiting, and expiry automation to simulate production readiness.

---

## 🏗️ Tech Stack

| Layer | Technology |
|------|-------------|
Backend | Flask |
Database | PostgreSQL |
ORM | SQLAlchemy |
Authentication | JWT |
Migrations | Alembic |
Scheduler | APScheduler |
Rate Limiter | Flask-Limiter |
Locking | Redis (Optional) |
Frontend | Jinja Templates |

---

## 🗄️ Database Design

### Users
Stores registered platform users.

Fields:
- id
- email
- password_hash
- role

---

### Cashback Assets
Represents each cashback credit issued.

Fields:
- id
- title
- total_value
- status (AVAILABLE / CLAIMED / EXPIRED)
- claimed_by
- claimed_at
- expires_at

---

### Claims Ledger
Immutable audit trail of claims.

Fields:
- id
- asset_id
- user_id
- amount
- claimed_at

---

## 🔐 Authentication & Authorization

- JWT-based login & registration
- Session-backed UI navigation
- Role-based access:

### Admin
- Create assets
- Update unclaimed assets
- Delete unclaimed assets
- Expire assets
- Recreate expired supply
- View voucher ownership

### User
- View assets
- Claim cashback
- View claim history
- Wallet balance view

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

---

### 1️⃣ Clone Repository
git clone <repo-url>
cd asset-mgmt-api

### 2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Setup PostgreSQL Database
Create a database:

asset_mgmt_db

### 5️⃣ Create .env File
Create a file in root:

.env
Example content:

DATABASE_URL=postgresql://postgres:password@localhost/asset_mgmt_db
JWT_SECRET_KEY=supersecretkey
.env is not pushed to GitHub for security reasons.

### 6️⃣ Run Migrations
flask db upgrade

### 7️⃣ Seed Admin User
Run SQL manually:

INSERT INTO users (email,password_hash,role)
VALUES (
'admin@gmail.com',
'$2b$12$examplehash...',
'ADMIN'
);
Admin credentials:

Email: admin@gmail.com
Password: admin123

### 8️⃣ Run Application
python run.py
App runs at:

http://127.0.0.1:5000
