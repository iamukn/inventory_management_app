## README

### Inventory Management System

**Overview**

This Django application is a basic inventory management system that includes user authentication, product management, order processing, and basic reporting functionalities.

**Features**

* User authentication and role-based access control (admin, regular user)
* Product management (create, read, update, delete for admin; read-only for regular users)
* Order management (create orders, track status, admin can update order status)
* Basic reporting (low stock products, sales report)

**Prerequisites**

* Python 3.8 or later
* Virtual environment (recommended)

**Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/iamukn/inventory-management.git
   ```
2. Create a virtual environment (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate.bat on Windows
   ```
3. Install dependencies and add environmental variable:
   ```bash
   pip install -r requirements.txt
   export SECRET_KEY="your personal secret key"
   ```
4. Create the database:
   ```bash
   python3 manage.py makemigrations
   python manage.py migrate
   ```
5. Create a superuser (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

**Running the Application**

```bash
python manage.py runserver
```

**Accessing the Application**

Open a web browser and go to http://127.0.0.1:8000/swagger/

**Additional Notes**

* The application uses SQLite for the database for simplicity. For production environments, consider using a more robust database like PostgreSQL or MySQL.
* Implement unit tests for key functionalities to ensure code quality and maintainability.
* Consider adding error handling and validation for API requests.
* Explore additional features like search functionality, product categories, and more detailed reporting.
