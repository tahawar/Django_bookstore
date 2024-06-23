Online Bookstore API
Project Overview
The Online Bookstore API is a RESTful service designed to manage an online bookstore. It allows users to perform CRUD operations on books, authors, and categories. Users can also register, authenticate, and manage their shopping cart. Once users purchase books, they receive an email notification with the details of their purchase.

Technologies Used
Backend: Django, Django REST Framework
Authentication: Django REST Framework Simple JWT
Database: PostgreSQL
Asynchronous Tasks: Celery (optional, if using for email notifications)
Containerization: Docker, Docker Compose
CI/CD: GitHub Actions
Documentation: drf-yasg for Swagger and ReDoc
Features
User Registration and Authentication: Users can register, log in, and log out.
CRUD Operations:
Books: Manage books with details like title, author, published date, ISBN, category, summary, and price.
Authors: Manage author information.
Categories: Manage book categories.
Shopping Cart: Users can add books to their cart, view cart contents, remove books, and purchase the books.
Email Notifications: (Optional) Send an email notification after a successful purchase.
Setup Instructions
Prerequisites
Python 3.10+
PostgreSQL
Docker (for containerization)
Git
Local Development
Clone the repository:

sh
Copy code
git clone https://github.com/yourusername/online-bookstore-api.git
cd online-bookstore-api
Create and activate a virtual environment:

sh
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:

sh
Copy code
pip install -r requirements.txt
Set up the database:
Update the DATABASES setting in bookstore/settings.py to match your PostgreSQL configuration.

python
Copy code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bookstore',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Run migrations:

sh
Copy code
python manage.py migrate
Create a superuser:

sh
Copy code
python manage.py createsuperuser
Run the development server:

sh
Copy code
python manage.py runserver
Docker Setup
Build and run the application using Docker:
sh
Copy code
docker-compose up --build
API Documentation
API documentation is available via Swagger and ReDoc.

Swagger UI: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/
API Endpoints
User Registration and Authentication
Register: POST /api/register/
Registers a new user.
Request body:
json
Copy code
{
  "username": "newuser",
  "password": "newpassword",
  "email": "newuser@example.com"
}
Login: POST /api/login/
Authenticates a user and returns JWT tokens.
Request body:
json
Copy code
{
  "username": "testuser",
  "password": "testpassword"
}
Token Refresh: POST /api/token/refresh/
Refreshes the access token.
Request body:
json
Copy code
{
  "refresh": "your_refresh_token"
}
Logout: POST /api/logout/
Logs out the user (blacklists the refresh token).
Books
List Books: GET /api/books/
Create Book: POST /api/books/
Request body:
json
Copy code
{
  "title": "Book Title",
  "author": 1,
  "published_date": "2023-01-01",
  "isbn": "1234567890123",
  "category": 1,
  "summary": "A brief summary",
  "price": 9.99
}
Retrieve Book: GET /api/books/{id}/
Update Book: PUT /api/books/{id}/
Request body:
json
Copy code
{
  "title": "Updated Book Title",
  "author": 1,
  "published_date": "2023-01-01",
  "isbn": "1234567890123",
  "category": 1,
  "summary": "An updated summary",
  "price": 12.99
}
Delete Book: DELETE /api/books/{id}/
Authors
List Authors: GET /api/authors/
Create Author: POST /api/authors/
Request body:
json
Copy code
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1970-01-01",
  "date_of_death": "2020-01-01"
}
Retrieve Author: GET /api/authors/{id}/
Update Author: PUT /api/authors/{id}/
Request body:
json
Copy code
{
  "first_name": "Jane",
  "last_name": "Doe",
  "date_of_birth": "1980-01-01",
  "date_of_death": "2020-01-01"
}
Delete Author: DELETE /api/authors/{id}/
Categories
List Categories: GET /api/categories/
Create Category: POST /api/categories/
Request body:
json
Copy code
{
  "name": "New Category"
}
Retrieve Category: GET /api/categories/{id}/
Update Category: PUT /api/categories/{id}/
Request body:
json
Copy code
{
  "name": "Updated Category"
}
Delete Category: DELETE /api/categories/{id}/
Shopping Cart
Add to Cart: POST /api/cart-items/
Request body:
json
Copy code
{
  "book": 1,
  "quantity": 2
}
List Cart Items: GET /api/cart-items/
Remove from Cart: DELETE /api/cart-items/{id}/
Purchases
Create Purchase: POST /api/purchases/
List Purchases: GET /api/purchases/
Email Notifications (Optional)
Send Email: POST /api/send-email/
Request body:
json
Copy code
{
  "recipient_email": "user@example.com",
  "subject": "Your Purchase",
  "message": "Thank you for your purchase."
}
Testing
To run tests, execute the following command:

sh
Copy code
python manage.py test
CI/CD
CI/CD is set up using GitHub Actions. Each push or pull request triggers the workflow defined in .github/workflows/ci.yml.

Deployment
To deploy the application using Docker:

Build and run the Docker containers:
sh
Copy code
docker-compose up --build
Contributions
Contributions are welcome! Please create an issue or submit a pull request for any changes or additions.

License
This project is licensed under the MIT License. See the LICENSE file for details.
