from backend.views import (ContactView, UserView,
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

urlpatterns = [
    path('activation/<int:id>/<str:token>', ActivateUserView.as_view(), name='activation'),
    path('get-token/', views.obtain_auth_token),
    # path('user/', UserView.as_view({'get': 'retrieve', 'post': 'create', 'patch': 'update', 'put': 'partial_update'})),
    path('load', ShopLoadView.as_view()),
    # path('shop/<int:pk>', ShopView.as_view()),
    # path('products', ListProduct.as_view()),
    # path('products/<int:pk>', ProductView.as_view()),
    # path('basket', OrderListView.as_view()),
    # path('order/<int:pk>', OrderView.as_view()),
    # path('order_shop/<int:pk>', OrderShopView.as_view()),
    path('contact', ContactView.as_view()),
] + router.urls
