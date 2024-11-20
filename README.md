Online Banking System
A robust Django-based web application designed to handle various aspects of online banking, including account management, loan tracking, and transactions. This system ensures seamless user experience and adheres to business rules, offering features for both customers and employees.

Features
Customer Features
Secure login and authentication using custom credentials.
Access to account details, including:
Personal information
Account balance and transaction history
Loan tracking:
View active loans and installment schedules
Account status management (Active, Frozen, Low Balance).
User-friendly dashboard for a seamless banking experience.
Employee Features
Dedicated employee login.
Employee-specific dashboard showing managed loan accounts.
Tools to manage account statuses and loan details.
Admin Features
Manage customer and employee accounts.
Assign roles and permissions.
Generate and monitor loan and transaction reports.
Technologies Used
Backend: Django (Python), PostgreSQL
Frontend: HTML, CSS
Libraries/Tools:
Django ORM for database interactions
Custom User Authentication (AbstractBaseUser and PermissionsMixin)
Secure password management
Version Control: Git & GitHub
Setup Instructions
Prerequisites
Python 3.9+
PostgreSQL
Git
Steps to Run the Project
Clone the repository:

bash
Copy code
git clone https://github.com/<your-username>/Online-Banking-System.git
cd Online-Banking-System
Set up a virtual environment:

bash
Copy code
python -m venv env
source env/bin/activate  # For macOS/Linux
env\Scripts\activate     # For Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Configure the database:

Update settings.py with your PostgreSQL database credentials.
Run migrations:
bash
Copy code
python manage.py makemigrations
python manage.py migrate
Create a superuser for admin access:

bash
Copy code
python manage.py createsuperuser
Run the development server:

bash
Copy code
python manage.py runserver
Access the application at http://127.0.0.1:8000/.

Project Highlights
Database Models:
Customer model for customer details
Account model for account information
Loan and Installments models for loan tracking
Transactions model for transaction history
Custom Authentication: Separate login flows for customers and employees.
Dynamic Dashboards: Tailored interfaces for customers and employees.
Error Handling: Ensures smooth transactions and account updates.
Screenshots
(Add screenshots of your home page, customer profile, employee dashboard, etc.)

Future Enhancements
Add session handling for enhanced security.
Integrate advanced reporting tools for admin users.
Implement notification systems for due installments.
Contributors
Your Name - GitHub Profile
Teammate 1 - GitHub Profile
Teammate 2 - GitHub Profile
License
This project is licensed under the MIT License.

