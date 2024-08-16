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

**Running test**
```bash
python manage.py test authentication/tests order/tests product/tests
```
**Accessing the Application**

Open a web browser and view the API documentation on http://127.0.0.1:8000/swagger/

**API ENDPOINTS**
### Authentication

#### POST /api/v1/auth/login
- **Description:** Authenticate a user .
- **Request:**
  - **Body:** 
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```

- **Response:**
  - **200 OK:** 

#### GET /api/v1/auth/logout
- **Description:** logout a user .
- **200 OK:**

### Products

#### GET /ap1/v1/products
- **Description:** Retrieve a list of all products.
- **Request:**
- Access to only Logged in users 
- **Response:**
  - **200 OK:**
    ```json
    [
      {
        "id": 1,
        "name": "Adidas",
        "description": "shoe",
        "price": "$5.0",
        "quantity": 23
      }
    ]
    ```

#### POST /ap1/v1/products
- **Description:** Create a new product entry.
- **access control:** ADMIN only 
- **Request:**`
  - **Body:**
    ```json
    {
      "name": "Adidas",
      "description": "shoes",
      "price":50,
      "quantity": 23
    }
    ```
- **Response:**
  - **201 Created:** 
    ```json
    {
      "id": 1,
      "name": "Adidas",
      "description": "shoes",
      "price":"$50",
      "quantity": 23
    }
    ```
  - **400 Bad Request:** Invalid data.

#### PATCH  PUT  DELETE /api/v1/products/{id}/
- **Description:** Update and deletes details of a product by only admin users.
- PATCH and PUT
  ``` json
     {
        "name": "new name",
        "price": 54
     }
  ```

### Orders

#### POST /api/v1/orders/
- **Description**: Creates an order
- **body**
```json
    {
    "product":[{"id": 1, "quantity": 3}]
    } 
```
#### GET /api/v1/orders/{id}/status
-> Open to all users

#### PATCH /api/v1/orders/{id}/status
-> only admin users
**body**
``` json
{
"status": "completed"
}
```

### Reports
#### GET /api/v1/orders/salesreports
-> only admin users
#### GET /api/v1/products/stockreports
-> only admin users



This structure clearly communicates how to use each endpoint, what to expect in terms of input and output, and any special requirements like authentication.
