from django.urls import path
from rest_framework.authtoken import views

from backend.views import CreateUserView, GetUserView, ShopView

urlpatterns = [
    path('get-token/', views.obtain_auth_token),
    path('user/', GetUserView.as_view()),
    path('register', CreateUserView.as_view()),
    path('shop/<int:pk>', ShopView.as_view()),
]
