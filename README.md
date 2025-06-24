# 🚖 Uber Clone – Ride Booking Web App

A full-stack **Uber Clone** built using **Django (backend)** and **React (frontend)**. The platform allows users to register as either a **rider (driver)** or a **passenger**, and perform respective actions like requesting or accepting rides. Integrated with **MapmyIndia API** to enable real-time routing and geolocation features.

---

## 📌 Project Overview

This project simulates the core functionality of a ride-hailing app like Uber. Users can:

- ✍️ Register as a **Rider (Driver)** or **Passenger**
- 🔐 Login and access dashboards based on role
- 📍 Passengers can request rides by entering pickup and drop locations
- 🚗 Riders can accept and manage ride requests
- 🗺️ View routes and directions using **MapmyIndia Routing API**
- 🛑 (Payment integration is pending and will be added soon)

---

## 🛠 Tech Stack

### 🔧 Backend

- Python Django
- Django REST Framework
- JWT Authentication
- SQLite / PostgreSQL (configurable)

### 💻 Frontend

- React.js (Vite)
- Axios (for API communication)
- Tailwind CSS (for styling)

### 🗺 Maps & Routing

- MapmyIndia Geocoding API
- MapmyIndia Directions & Routing API

---

## ✅ Key Features

- Role-based user registration: Rider or Passenger
- Secure JWT-based authentication
- Rider dashboard: View ride requests, accept ride
- Passenger dashboard: Request ride with pickup/drop
- Real-time routing via MapmyIndia APIs
- View estimated route on map with directions
- Profile management (username, email, profile picture)
- Modular API structure for easy extension

---

## 🧪 Project Setup

### 📥 Clone the Repository

```bash
git clone https://github.com/yourusername/uberclone.git
cd uberclone


🔧 Backend Setup (Django)
cd backend/
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


💻 Frontend Setup (React)
cd frontend/
npm install
npm run dev


🔜 Upcoming Features
💳 Payment integration (Razorpay/Stripe/UPI)

📈 Ride history and analytics

🔔 Real-time driver location tracking

💬 Notifications for ride status

