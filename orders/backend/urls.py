from django.urls import path
from rest_framework.authtoken import views

from backend.views import CreateUserView, GetUserView, ListProduct, ShopLoadView, ShopView

urlpatterns = [
    path('get-token/', views.obtain_auth_token),
    path('user/', GetUserView.as_view()),
    path('register', CreateUserView.as_view()),
    path('shop/<int:pk>', ShopView.as_view()),
    path('load', ShopLoadView.as_view()),
    path('products', ListProduct.as_view()),
]
