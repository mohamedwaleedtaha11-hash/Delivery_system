# Food Delivery API

A RESTful backend for a food delivery system built with Django REST Framework and Docker.

## Features
- JWT Authentication (Djoser + SimpleJWT)
- Restaurants, menu items, orders, and drivers management
- Live location tracking for drivers
- Object-level permissions for customers and drivers
- Dockerized setup

## Tech Stack
- Python 3.12
- Django & Django REST Framework
- Docker

## Quick Start with Docker
```bash
git clone [https://github.com/mohamedwaleedtaha11-hash/Delivery_system.git](https://github.com/mohamedwaleedtaha11-hash/Delivery_system.git)
cd Delivery_system
docker build -t delivery_system .
docker run -p 8000:8000 delivery_system

API Endpoints
/api/restaurants/ - Restaurants list

/api/menu_items/ - Menu items list

/api/menu_items/{id}/order/ - Place an order

/api/orders/ - Orders management

/api/drivers/ - Drivers list

Author
Mohamed Waleed
