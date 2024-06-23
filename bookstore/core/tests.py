from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book, Author, Category, ShoppingCart, CartItem, Purchase, PurchaseItem

class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
        self.author = Author.objects.create(first_name='John', last_name='Doe')
        self.category = Category.objects.create(name='Fiction')
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            published_date='2023-01-01',
            isbn='1234567890123',
            category=self.category,
            summary='A test book.',
            price=9.99
        )
        self.cart = ShoppingCart.objects.create(user=self.user)

        # Obtain the token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

class UserTests(BaseTestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class BookTests(BaseTestCase):
    def test_create_book(self):
        url = reverse('book-list')
        data = {
            'title': 'Test Book',
            'author': self.author.id,
            'published_date': '2023-01-01',
            'isbn': '1234567890123',
            'category': self.category.id,
            'summary': 'A test book.',
            'price': 9.99
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_books(self):
        url = reverse('book-list')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_book(self):
        url = reverse('book-detail', args=[self.book.id])
        data = {
            'title': 'Updated Test Book',
            'author': self.author.id,
            'published_date': '2023-01-01',
            'isbn': '1234567890123',
            'category': self.category.id,
            'summary': 'An updated test book.',
            'price': 19.99
        }
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class AuthorTests(BaseTestCase):
    def test_create_author(self):
        url = reverse('author-list')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1970-01-01',
            'date_of_death': '2020-01-01'
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_authors(self):
        url = reverse('author-list')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_author(self):
        url = reverse('author-detail', args=[self.author.id])
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'date_of_death': '2020-01-01'
        }
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_author(self):
        url = reverse('author-detail', args=[self.author.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CategoryTests(BaseTestCase):
    def test_create_category(self):
        url = reverse('category-list')
        data = {
            'name': 'Fiction'
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_categories(self):
        url = reverse('category-list')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        category = Category.objects.create(name='Fiction')
        url = reverse('category-detail', args=[category.id])
        data = {
            'name': 'Science Fiction'
        }
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        category = Category.objects.create(name='Fiction')
        url = reverse('category-detail', args=[category.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ShoppingCartTests(BaseTestCase):
    def test_add_to_cart(self):
        url = reverse('cartitem-list')
        data = {
            'book': self.book.id,
            'quantity': 1
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_cart_items(self):
        CartItem.objects.create(cart=self.cart, book=self.book, quantity=1)
        url = reverse('cartitem-list')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_from_cart(self):
        cart_item = CartItem.objects.create(cart=self.cart, book=self.book, quantity=1)
        url = reverse('cartitem-detail', args=[cart_item.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class PurchaseTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        CartItem.objects.create(cart=self.cart, book=self.book, quantity=1)

    def test_create_purchase(self):
        url = reverse('purchase-list')
        response = self.client.post(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_purchases(self):
        Purchase.objects.create(user=self.user, total_amount=9.99)
        url = reverse('purchase-list')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
