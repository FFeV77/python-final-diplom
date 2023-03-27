from django.urls import path
from rest_framework.authtoken import views

from backend.views import BasketView, CreateUserView, GetUserView, ListProduct, ProductView, ShopLoadView, ShopView

urlpatterns = [
    path('get-token/', views.obtain_auth_token),
    path('user/', GetUserView.as_view()),
    path('register', CreateUserView.as_view()),
    path('shop/<int:pk>', ShopView.as_view()),
    path('load', ShopLoadView.as_view()),
    path('products', ListProduct.as_view()),
    path('products/<int:pk>', ProductView.as_view()),
    path('basket', BasketView.as_view()),
]
