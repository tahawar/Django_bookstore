
from rest_framework import generics, permissions, status, viewsets, filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import RegisterSerializer, AuthorSerializer, BookSerializer, CategorySerializer, ShoppingCartSerializer, CartItemSerializer, PurchaseSerializer
from .models import Author, Book, Category, ShoppingCart, CartItem, Purchase, PurchaseItem
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .models import Purchase, PurchaseItem
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Purchase, ShoppingCart, PurchaseItem, CartItem, Book
from .serializers import PurchaseSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": str(e)})

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['date_of_birth']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author', 'category']
    search_fields = ['title', 'summary']
    ordering_fields = ['published_date', 'author']

class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user).order_by('id')  # Add .order_by('id') to ensure ordering

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            cart, created = ShoppingCart.objects.get_or_create(user=request.user)  # Ensure ShoppingCart exists
            book = Book.objects.get(id=data['book'])
            cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
            if not created:
                cart_item.quantity += int(data['quantity'])
                cart_item.save()
            else:
                cart_item.quantity = int(data['quantity'])
                cart_item.save()
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)






class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            cart = ShoppingCart.objects.get(user=request.user)
            cart_items = cart.items.all()
            if not cart_items.exists():
                return Response({"detail": "No items in the cart."}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate total amount
            total_amount = sum(item.book.price * item.quantity for item in cart_items)

            # Create purchase
            purchase = Purchase.objects.create(user=request.user, total_amount=total_amount)

            # Add cart items to purchase
            purchase_items = []
            for item in cart_items:
                purchase_item = PurchaseItem.objects.create(
                    purchase=purchase,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.book.price
                )
                purchase_items.append({
                    "book": item.book.title,
                    "quantity": item.quantity,
                    "price": item.book.price
                })
                item.delete()

            response_data = {
                "purchase_id": purchase.id,
                "user": request.user.username,
                "total_amount": total_amount,
                "items": purchase_items
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        except ShoppingCart.DoesNotExist:
            return Response({"detail": "Shopping cart not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SendEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        purchase_id = request.data.get('purchase_id')
        user_email = request.user.email
        try:
            purchase = Purchase.objects.get(id=purchase_id, user=request.user)
            items = PurchaseItem.objects.filter(purchase=purchase)
            item_list = "\n".join([f"{item.book.title} - {item.quantity} x {item.price}" for item in items])
            total_amount = purchase.total_amount

            message = Mail(
                from_email="Ujavid@lumina247.com",
                to_emails=user_email,
                subject='Purchase Confirmation',
                plain_text_content=f'Thank you for your purchase!\n\nItems:\n{item_list}\n\nTotal Amount: {total_amount}'
            )
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)

            return Response({"detail": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Purchase.DoesNotExist:
            return Response({"detail": "Purchase not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@shared_task
def send_purchase_confirmation_email(email, purchase_id):
    purchase = Purchase.objects.get(id=purchase_id)
    items = purchase.items.all()
    item_details = "\n".join([f"{item.book.title}: {item.quantity} @ {item.price}" for item in items])
    message = f"Thank you for your purchase!\n\nYour order details:\n{item_details}\n\nTotal Amount: {purchase.total_amount}"
    send_mail(
        'Purchase Confirmation',
        message,
        'tahawarihsan.codrivity@gmail.com',
        [email],
        fail_silently=False,
    )

