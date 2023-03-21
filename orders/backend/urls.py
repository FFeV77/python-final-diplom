from django.urls import path
from rest_framework.authtoken import views

from backend.views import CreateUserView, GetUserView

urlpatterns = [
    path('get-token/', views.obtain_auth_token),
    path('user/', GetUserView.as_view()),
    path('user/register', CreateUserView.as_view()),
]
