# Online Banking System

A robust Django-based web application designed to handle various aspects of online banking, including account management, loan tracking, and transactions. This system ensures seamless user experience and adheres to business rules, offering features for both customers and employees.

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/<your-username>/Online-Banking-System/actions) 

## Features

### Customer Features
- Secure login and authentication using custom credentials.
- Access to account details, including:
  - Personal information
  - Account balance and transaction history
- Loan tracking:
  - View active loans and installment schedules
  - Account status management (Active, Frozen, Low Balance).
- User-friendly dashboard for a seamless banking experience.

### Employee Features
- Dedicated employee login.
- Employee-specific dashboard showing managed loan accounts.
- Tools to manage account statuses and loan details.

### Admin Features
- Manage customer and employee accounts.
- Assign roles and permissions.
- Generate and monitor loan and transaction reports.

## Technologies Used

- **Backend**: Django (Python), PostgreSQL
- **Frontend**: HTML, CSS
- **Libraries/Tools**:
  - Django ORM for database interactions
  - Custom User Authentication (AbstractBaseUser and PermissionsMixin)
  - Secure password management

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL
- Django 

### Steps to Run the Project
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/Online-Banking-System.git
   cd Online-Banking-System
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # For macOS/Linux
   env\Scripts\activate     # For Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the database:
   Update `settings.py` with your PostgreSQL database credentials.
5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```
8. Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Screenshots

<img width="1280" alt="Screenshot 2024-11-20 at 2 33 35 PM" src="https://github.com/user-attachments/assets/71715fee-0043-4e36-8ccf-013831249c31">


## Future Enhancements
- Add security like capcha verification for password reset.
- Integrate advanced reporting tools for admin users.
- Implement notification systems for due installments.

## Contributors
- Thilak L - [GitHub Profile](https://github.com/thilak0105)
- Teammate 1 - [Subramanian G](https://github.com/Demoncyborg07)
- Teammate 2 - [Raghul A R](https://github.com/a-steel-heart)

