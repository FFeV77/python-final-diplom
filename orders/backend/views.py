from backend.models import Contact, Order, Product, ProductInfo, Shop, User
from backend.permissions import IsOrderUserOwner, IsShop
from backend.serialyzers import (ContactSerializer, OrderSerializer,
                                 ProductInfoSerializer, ProductSerializer,
                                 ShopLoadSerializer, ShopSerializer,
                                 UserSerialyzer)
from backend.utils import file_shop_load, link_shop_load
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


# Create your views here.
class ActivateUserView(APIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def patch(self, request, id, token):
        user = User.objects.get(pk=id)
        if user:
            created_token = Token.objects.get(user_id=user)
            if created_token.key == token:
                user.is_active = True
                user.save()
                resp = {'status': 'ok'}
            else:
                resp = {'status': 'error', 'message': 'activation link is invalid'}
        else:
            resp = {'status': 'error', 'message': 'invalid user'}
        return Response(resp)


class UserView(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerialyzer

    def get_object(self):
        return self.request.user

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         serializer = CreateUserSerialyzer
    #     else:
    #         serializer = super().get_serializer_class()
    #     return serializer

    def get_permissions(self):
        if self.action == 'create':
            permission = [AllowAny()]
        else:
            permission = super().get_permissions()
        return permission

    def list(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ListProductView(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    ...


class ProductView(ReadOnlyModelViewSet):
    queryset = ProductInfo.objects.prefetch_related('product_parameters')
    permission_classes = [IsAuthenticated]
    serializer_class = ProductInfoSerializer


class BuyerOrderView(ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated & IsOrderUserOwner]
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ContactView(ModelViewSet):
    queryset = Contact.objects.all()
    permission_classes = [IsAuthenticated & IsOrderUserOwner]
    serializer_class = ContactSerializer

    def get_queryset(self):
        request = super().get_queryset()
        return request.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        return super().perform_create(serializer)


class ShopView(ModelViewSet):
    queryset = Shop.objects.prefetch_related('id__product_infos')
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsShop]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        return super().perform_create(serializer)


class OrderShopView(ModelViewSet):
    queryset = Order.objects.filter(ordered_items__product_info__shop=9)
    permission_classes = [IsShop]
    serializer_class = OrderSerializer

    def get_queryset(self):
        shops = Shop.objects.filter(user=self.request.user)
        queryset = Order.objects.filter(ordered_items__product_info__shop__in=shops)
        return queryset


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
