from backend.models import Contact, Order, Product, ProductInfo, Shop, User
from backend.permissions import IsOrderUserOwner, IsShop
from backend.serialyzers import (ContactSerializer, CreateUserSerialyzer, OrderSerializer, ProductInfoSerializer, ProductSerializer, ShopLoadSerializer,
                                 ShopSerializer, UpdateUserSerializer)
from backend.utils import file_shop_load, link_shop_load
from rest_framework.generics import (CreateAPIView, RetrieveAPIView, ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerialyzer


class GetUserView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user


class ListProduct(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    ...


class ProductView(RetrieveAPIView):
    queryset = ProductInfo.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductInfoSerializer


class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        request = super().get_queryset()
        return request.filter(user=self.request.user)
    

class OrderView(RetrieveAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsOrderUserOwner]
    serializer_class = OrderSerializer


class ContactView(ListCreateAPIView):
    queryset = Contact.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def get_queryset(self):
        request = super().get_queryset()
        return request.filter(user=self.request.user)


class ShopView(RetrieveAPIView):
    queryset = Shop.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer


class ShopLoadView(APIView):
    queryset = Shop.objects.all()
    permission_classes = [IsAuthenticated & IsShop]
    serializer_class = ShopLoadSerializer

    def post(self, request):
        if request.data.get('file'):
            resp = file_shop_load(request.data['file'], request)
        elif request.data.get('link'):
            resp = link_shop_load(request.data['link'], request)
        else:
            resp = {'error': 'data not set'}
        return Response(resp)
