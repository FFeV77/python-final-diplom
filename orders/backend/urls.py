from backend.views import (ActivateUserView, BasketView, BuyerOrderView,
                           CategoryView, ContactView, ListProductView,
                           OrderConfirmView, OrderShopView, ProductView,
                           RegisterView, ShopLoadView, ShopView, UserView)
from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('orders', BuyerOrderView, basename='orders')
router.register('products', ListProductView, basename='products')
router.register('product', ProductView, basename='product')
router.register('shops', ShopView, basename='shops')
router.register('orders_shop', OrderShopView, basename='orders_shop')
router.register('contacts', ContactView, basename='contacts')
router.register('category', CategoryView, basename='category')
router.register('basket', BasketView, basename='basket')

urlpatterns = [
    path('user/', UserView.as_view(), name='user'),
    path('register/', RegisterView.as_view(), name='user'),
    path('activation/<int:id>/<str:token>', ActivateUserView.as_view(), name='activation'),
    path('order_new', OrderConfirmView.as_view(), name='order_new'),
    path('get-token/', views.obtain_auth_token),
    path('load', ShopLoadView.as_view()),
] + router.urls
