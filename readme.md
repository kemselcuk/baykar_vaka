# Aircraft Builder Application

## Overview

The Aircraft Builder Application is a Python-based project designed to manage the production of aircraft and their components efficiently. It integrates various functionalities for employees, teams, and inventory management. The application adheres to strict rules for part production, assembly, and inventory control, ensuring that the aircraft-building process is streamlined and error-free.

## Features

### Functionalities
1. **Employee Management:**
   - Login, logout, and registration for personnel.
   - Assignment of personnel to specific teams. A team can have multiple members.

2. **Team Operations:**
   - CRUD (Create, Read, Delete) operations for parts specific to each team.
   - Each team can only produce parts relevant to their responsibility (e.g., Avionics Team cannot produce wings).

3. **Aircraft Assembly:**
   - The Assembly Team combines all compatible parts to produce an aircraft.
   - Each part is unique to the aircraft model (e.g., TB2 wings cannot be used for TB3).
   - Assembled aircrafts are listed for review.

4. **Inventory Management:**
   - Alerts when parts are missing for specific aircraft models.
   - Ensures parts used in one aircraft cannot be reused in another.
   - Tracks the number of parts used and their assignment to specific aircraft models.

### Supported Components
- **Parts:** Kanat, Kuyruk, Gövde, Aviyonik
- **Aircraft Models:** TB2, TB3, AKINCI, KIZILELMA
- **Teams:** Kanat Takımı, Kuyruk Takımı, Gövde Takımı, Aviyonik Takımı, Montaj Takımı

## Technology Stack
- **Backend:** Python, Django, Django Rest Framework
- **Database:** PostgreSQL
- **API Documentation:** Swagger
- **Containerization:** Docker
- **Frontend:** Bootstrap

## Installation and Setup

### Prerequisites
- Docker
- Docker Compose

### Steps to Run the Application
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```
3. Access the application:
   - Backend API: `http://localhost:8000`
   - Swagger Documentation: `http://localhost:8000/swagger/`

## API Endpoints

### Global Endpoints
- **Admin Panel:** `/admin/`
- **Swagger UI:** `/swagger/`
- **ReDoc:** `/swagger/.redoc`

### Employee Management
- **Home:** `/employees/`
- **Login:** `/employees/login/`
- **Logout:** `/employees/logout/`
- **Register:** `/employees/register/`

### Team Operations
- **Create Part:** `/teams/create/`
- **List Parts:** `/teams/list/`
- **Delete Part:** `/teams/delete/<part_id>/`

### Aircraft Operations
- **Assemble Aircraft:** `/aircrafts/assemble/`
- **List Aircrafts:** `/aircrafts/list/`
- **Aircraft Details:** `/aircrafts/aircraft/<aircraft_id>/details/`

## Docker Configuration

The application uses Docker for containerization. Below is the `docker-compose.yml` configuration:

```yaml
version: '3.10'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: aircraft_builder
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres

  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             python manage.py create_teams &&
             python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    environment:
      - DOCKER_ENV=1
      - POSTGRES_DB=aircraft_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_HOST=db
      - POSTGRES_PORT=5432
    depends_on:
      - db

volumes:
  postgres_data:
```

## Additional Features
- **Documentation:** Comprehensive API documentation provided via Swagger.
- **Unit Tests:** Implemented for critical functionalities.
- **Relational Tables:** Separate tables for employees, teams, parts, and aircraft models.
- **Django Libraries:** Utilized advanced Django libraries for optimized performance.

## Screenshots from project

Login:
![alt text](<screenshots/Screenshot 2024-12-23 110838.png>)

---
Sign In:
![alt text](<screenshots/Screenshot 2024-12-23 110927.png>)

---

Home Page for Part Teams:
![alt text](<screenshots/Screenshot 2024-12-23 110938.png>)

---
Part List:
![alt text](<screenshots/Screenshot 2024-12-23 111003.png>)

---
Filtering Parts by Aircraft Types at Part List:
![alt text](<screenshots/Screenshot 2024-12-23 111016.png>)

---
Logging out:
![alt text](<screenshots/Screenshot 2024-12-23 111027.png>)

---
Home Page for 'Montaj Takımı':
![alt text](<screenshots/Screenshot 2024-12-23 111037.png>)

---
Part list for 'Montaj Takımı':
![alt text](<screenshots/Screenshot 2024-12-23 111046.png>)

---
Aircraft list for 'Montaj Takımı':
![alt text](<screenshots/Screenshot 2024-12-23 111056.png>)

---
The details of the Parts Used in Aircraft for 'Montaj Takımı':
![alt text](<screenshots/Screenshot 2024-12-23 111104.png>)

---
Create Aircraft page for 'Montaj Takımı':
![alt text](<screenshots/Screenshot 2024-12-23 111139.png>)