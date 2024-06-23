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
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   Install dependencies:
   pip install -r requirements.txt
   Set up the database:
   python manage.py migrate
   Create a superuser:
   python manage.py createsuperuser
   Run the development server:
   python manage.py runserver

# API Endpoints

## User Registration and Authentication

### Register
- **POST** `/api/register/`
  - **Request:** `{"username": "newuser", "password": "newpassword", "email": "newuser@example.com"}`
  - **Response:** `{"id": 1, "username": "newuser", "email": "newuser@example.com"}`

### Login
- **POST** `/api/login/`
  - **Request:** `{"username": "testuser", "password": "testpassword"}`
  - **Response:** `{"refresh": "token", "access": "token"}`

### Logout
- **POST** `/api/logout/`
  - **Request:** `{"refresh": "token"}`
  - **Response:** `204 No Content`

## Books

### List Books
- **GET** `/api/books/`
  - **Response:** `[{"id": 1, "title": "Book Title", "author": "Author Name", ...}, ...]`

### Create Book
- **POST** `/api/books/`
  - **Request:** `{"title": "New Book", "author": 1, "published_date": "2023-01-01", "isbn": "1234567890123", "category": 1, "summary": "Summary of the book", "price": 9.99}`
  - **Response:** `{"id": 1, "title": "New Book", "author": 1, ...}`

### Retrieve Book
- **GET** `/api/books/{id}/`
  - **Response:** `{"id": 1, "title": "Book Title", "author": "Author Name", ...}`

### Update Book
- **PUT** `/api/books/{id}/`
  - **Request:** `{"title": "Updated Book", "author": 1, "published_date": "2023-01-01", "isbn": "1234567890123", "category": 1, "summary": "Updated summary", "price": 19.99}`
  - **Response:** `{"id": 1, "title": "Updated Book", "author": 1, ...}`

### Delete Book
- **DELETE** `/api/books/{id}/`
  - **Response:** `204 No Content`

## Authors

### List Authors
- **GET** `/api/authors/`
  - **Response:** `[{"id": 1, "first_name": "John", "last_name": "Doe", ...}, ...]`

### Create Author
- **POST** `/api/authors/`
  - **Request:** `{"first_name": "John", "last_name": "Doe", "date_of_birth": "1970-01-01", "date_of_death": "2020-01-01"}`
  - **Response:** `{"id": 1, "first_name": "John", "last_name": "Doe", ...}`

### Retrieve Author
- **GET** `/api/authors/{id}/`
  - **Response:** `{"id": 1, "first_name": "John", "last_name": "Doe", ...}`

### Update Author
- **PUT** `/api/authors/{id}/`
  - **Request:** `{"first_name": "Jane", "last_name": "Doe", "date_of_birth": "1980-01-01", "date_of_death": "2020-01-01"}`
  - **Response:** `{"id": 1, "first_name": "Jane", "last_name": "Doe", ...}`

### Delete Author
- **DELETE** `/api/authors/{id}/`
  - **Response:** `204 No Content`

## Categories

### List Categories
- **GET** `/api/categories/`
  - **Response:** `[{"id": 1, "name": "Fiction"}, ...]`

### Create Category
- **POST** `/api/categories/`
  - **Request:** `{"name": "Fiction"}`
  - **Response:** `{"id": 1, "name": "Fiction"}`

### Retrieve Category
- **GET** `/api/categories/{id}/`
  - **Response:** `{"id": 1, "name": "Fiction"}`

### Update Category
- **PUT** `/api/categories/{id}/`
  - **Request:** `{"name": "Science Fiction"}`
  - **Response:** `{"id": 1, "name": "Science Fiction"}`

### Delete Category
- **DELETE** `/api/categories/{id}/`
  - **Response:** `204 No Content`

## Shopping Cart

### Add to Cart
- **POST** `/api/cart-items/`
  - **Request:** `{"book": 1, "quantity": 1}`
  - **Response:** `{"id": 1, "cart": 1, "book": 1, "quantity": 1}`

### List Cart Items
- **GET** `/api/cart-items/`
  - **Response:** `[{"id": 1, "cart": 1, "book": 1, "quantity": 1}, ...]`

### Remove from Cart
- **DELETE** `/api/cart-items/{id}/`
  - **Response:** `204 No Content`

## Purchases

### Create Purchase
- **POST** `/api/purchases/`
  - **Response:** `{"id": 1, "user": 1, "created_at": "2023-01-01T00:00:00Z", "total_amount": 19.99}`

### List Purchases
- **GET** `/api/purchases/`
  - **Response:** `[{"id": 1, "user": 1, "created_at": "2023-01-01T00:00:00Z", "total_amount": 19.99}, ...]`
  - 


  # Docker Setup

This project uses Docker to simplify the setup and deployment process. Follow the steps below to get the application running with Docker.

## Docker Installation

- **Install Docker:** If you don't already have Docker installed, [download and install it here](https://www.docker.com/get-started).

## Building and Running the Application with Docker

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/online-bookstore-api.git
    cd online-bookstore-api
    ```

2. **Create a `.env` file:** In the root directory of the project, create a `.env` file with the following content:

    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    DATABASE_URL=postgres://user:password@db:5432/bookstore
    EMAIL_HOST=smtp.sendgrid.net
    EMAIL_HOST_USER=apikey
    EMAIL_HOST_PASSWORD=your_sendgrid_api_key
    EMAIL_PORT=587
    ```

3. **Build the Docker image:**

    ```sh
    docker-compose build
    ```

4. **Run the Docker containers:**

    ```sh
    docker-compose up
    ```

## Docker Compose Configuration

The `docker-compose.yml` file is configured to run two services: `web` and `db`.

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn --bind 0.0.0.0:8000 bookstore.wsgi:application
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: bookstore
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password

volumes:
  postgres_data:


## Dockerfile

The Dockerfile sets up the environment and dependencies for the Django application.

```dockerfile
# Dockerfile
FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bookstore.wsgi:application"]


Accessing the Application
The application will be available at http://localhost:8000.

Stopping the Application
To stop the running containers:

Press CTRL+C in the terminal where the containers are running.

Alternatively, run:

docker-compose down

