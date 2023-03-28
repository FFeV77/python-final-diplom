from backend.views import (ContactView, CreateUserView, GetUserView,
                           ListProduct, OrderListView, ProductView,
                           ShopLoadView, ShopView, OrderView)
from django.urls import path
from rest_framework.authtoken import views

urlpatterns = [
    path('register', CreateUserView.as_view()),
    path('get-token/', views.obtain_auth_token),
    path('user/', GetUserView.as_view()),
    path('load', ShopLoadView.as_view()),
    path('shop/<int:pk>', ShopView.as_view()),
    path('products', ListProduct.as_view()),
    path('products/<int:pk>', ProductView.as_view()),
    path('basket', OrderListView.as_view()),
    path('order/<int:pk>', OrderView.as_view()),
    path('contact', ContactView.as_view()),
]
