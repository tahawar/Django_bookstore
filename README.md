# Online Bookstore API

## Description

The Online Bookstore API is a RESTful service built using Django and Django REST Framework. It allows users to perform CRUD operations on books, authors, and categories, manage a shopping cart, and handle purchases. The application supports user registration, authentication, and email notifications for successful purchases. This project demonstrates the use of Django, Django REST Framework, PostgreSQL, and Celery for background tasks.

## Technologies Used

- **Django**: Web framework for the backend.
- **Django REST Framework**: Toolkit for building Web APIs.
- **PostgreSQL**: Database for storing application data.
- **Celery**: Asynchronous task queue for handling background tasks.
- **Docker**: Containerization for development and deployment.
- **GitHub Actions**: CI/CD for automated testing and deployment.

## Features

1. **User Registration and Authentication**:
   - Users can register, log in, and log out.
   - Token-based authentication for secure access.

2. **CRUD Operations**:
   - **Books**: Create, read, update, and delete books. Each book has details like title, author, published date, ISBN, category, summary, and price.
   - **Authors**: Create, read, update, and delete authors.
   - **Categories**: Create, read, update, and delete categories.

3. **Shopping Cart**:
   - Users can add books to their shopping cart, view the cart, remove books from the cart, and purchase the books in the cart.

4. **Email Notifications**:
   - After a successful purchase, an email notification is sent to the user with the details of their purchase.

## Setup Instructions

1. **Clone the repository**:
   ```sh
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
