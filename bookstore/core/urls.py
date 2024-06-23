# from django.urls import path
# from .views import RegisterView, LogoutView
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

# urlpatterns = [
#     path('api/register/', RegisterView.as_view(), name='register'),
#     path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('api/logout/', LogoutView.as_view(), name='logout'),
# ]



# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import RegisterView, LogoutView, AuthorViewSet, BookViewSet, CategoryViewSet
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# router = DefaultRouter()
# router.register(r'authors', AuthorViewSet)
# router.register(r'books', BookViewSet)
# router.register(r'categories', CategoryViewSet)

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('', include(router.urls)),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LogoutView, AuthorViewSet, BookViewSet, CategoryViewSet, ShoppingCartViewSet, CartItemViewSet, PurchaseViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PurchaseViewSet, SendEmailView

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'shopping-cart', ShoppingCartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'purchases', PurchaseViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Online Bookstore API",
      default_version='v1',
      description="API documentation for the Online Bookstore",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('send-email/', SendEmailView.as_view(), name='send-email'),
]
