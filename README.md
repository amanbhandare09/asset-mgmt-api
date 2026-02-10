# Asset Management API — Cashback Credit Pool

## Overview

This project implements a production-grade backend system for managing limited cashback wallet assets.

It ensures strict financial integrity when multiple authenticated users attempt to claim the same cashback credit simultaneously.

---

## Core Features

### Authentication
- JWT-based login & registration
- Role-based access (Admin / User)

### Asset Lifecycle Management
- Create cashback assets
- Update unclaimed assets
- Delete unclaimed assets
- Expire assets
- Recreate expired supply

### Claim Protection
- PostgreSQL row-level locking
- Redis distributed locks
- Transactional claim execution

### Ledger System
- Immutable claim audit trail
- User claim history
- Global voucher ownership view

### Concurrency Protection
- Prevents duplicate claims
- Handles high contention scenarios

### Rate Limiting
- Redis-backed API throttling
- Abuse protection on claim endpoints

### Background Jobs
- Automated asset expiry scheduler

---

## Tech Stack

| Layer | Tech |
|------|------|
Backend | Flask |
Database | PostgreSQL |
ORM | SQLAlchemy |
Auth | JWT |
Locking | Redis |
Limiter | Flask-Limiter |
Scheduler | APScheduler |
Frontend | Jinja Templates |

---

## Running the Project

### 1. Install Dependencies

```bash
pip install -r requirements.txt


## Redis (Optional)

Redis is used for:

- Distributed locking
- Rate limiting storage

The system automatically falls back to in-memory mode if Redis is not installed, ensuring zero setup friction for reviewers.
