# 🚗 Vehicle Parking App V2

**Modern Application Development II (MAD-II)**  
**Semester:** May 2025  
**Student:** Harsh Dubey  
**Roll Number:** 22f3003278@ds.study.iitm.ac.in

---

## Project Overview

Vehicle Parking App V2 is a multi-user application that manages multiple parking lots, their corresponding parking spots, and parking activity for 4-wheeler vehicles. It features two user roles: **Admin** (superuser) and **User**. The app offers real-time spot management, automatic allocation, reservation history, daily reminders, monthly reports, and CSV exports.

---

## Frameworks & Tools Used

- **Backend:** Flask, SQLAlchemy, Flask-JWT-Extended, Celery, Redis, Flask-Caching
- **Frontend:** VueJS Bootstrap
- **Database:** SQLite
- **Other Tools:** Redis (for caching & Celery), Chart.js (for data visualization), Google Chat Webhook (daily reminders), Email (SMTP)

---

## User Roles

### Admin (Superuser)

- No registration required (created automatically at DB setup)
- Create, edit, delete parking lots (delete only when empty)
- View parking status and parked vehicle info
- View all registered users and dashboard stats

### User

- Register/Login
- View lots and reserve first-available spot
- Occupy and release spot
- View reservation history and monthly stats

---

## Database Schema (ER Diagram)

Includes:

- **User**
- **Admin**
- **ParkingLot**
- **ParkingSpot**
- **Reservation**

Each entity is related using foreign keys. Admin is a system-defined singleton.

---

## API Endpoints

### Auth

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

### Admin

- `GET /dashboard`
- `POST /lots`
- `PUT /lots/:id`
- `DELETE /lots/:id`
- `GET /lots`
- `GET /lots/:lotId/spots`
- `GET /lots/:lotId/spots/current`
- `GET /users`
- `GET /spots/:spotId/history`

### User

- `POST /reserve`
- `POST /occupy/:reservation_id`
- `POST /release/:reservation_id`
- `GET /history`
- `GET /dashboard/user`
- `GET /export/csv`

---

## Background Tasks (Celery + Redis)

### Daily Reminders

- Sent to users via Google Chat Webhook or email if they haven't made a reservation that day

### Monthly Activity Report

- Sent via HTML email on the 1st of each month
- Includes: total hours parked, money spent, favorite lot

### User-Triggered CSV Export

- Triggered from user dashboard
- Exports all reservation data (slot_id, timestamps, cost, etc.)

---

## Caching (Redis + Flask-Caching)

- Cached endpoints:
  - `/lots`
  - `/lots/:lotId/spots/current`
- Auto-invalidation on create/update/delete actions

---

## Features

- Role-based authentication using JWT (Admin/User)
- Full REST API
- Responsive UI (Bootstrap)
- Charts for usage/revenue stats (Chart.js)
- Async jobs using Celery + Redis
- Daily reminders + Monthly reports + CSV Export
- Frontend/backend validation
- Modular frontend with reusable Vue components

---

## Folder Structure (Example)

```
/server
  ├── beat.sh
  ├── worker.sh
  ├── requirements.txt
  ├─ run.py
  ├── backend
    ├── models/
    ├── routes/
    ├── tasks/
    ├── utils/
    ├── controllers/
    ├── middleware/
    ├── templates
    ├── __init__.py
    ├── config.py
    ├── extensions.py

/frontend
  ├── src/
    ├── components/
    ├── views/
    ├── store/
    ├── hooks/
    ├── pages/
    ├── router/
    ├── services/
    ├── utils/
    ├── App.vue
    ├── main.js

```

---
