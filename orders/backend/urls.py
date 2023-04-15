from backend.views import (CategoryView, ContactView, UserView,
                           ListProductView, OrderShopView, ProductView,
                           ShopLoadView, ShopView, BuyerOrderView, ActivateUserView)
from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UserView, basename='user')
router.register('orders', BuyerOrderView, basename='orders')
router.register('products', ListProductView, basename='products')
router.register('product', ProductView, basename='product')
router.register('shops', ShopView, basename='shops')
router.register('orders_shop', OrderShopView, basename='orders_shop')
router.register('contacts', ContactView, basename='contacts')
router.register('category', CategoryView, basename='category')

urlpatterns = [
    path('activation/<int:id>/<str:token>', ActivateUserView.as_view(), name='activation'),
    path('get-token/', views.obtain_auth_token),
    path('load', ShopLoadView.as_view()),
] + router.urls
