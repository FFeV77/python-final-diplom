from backend import serialyzers
from backend.models import (Category, Contact, Order, OrderItem, Product,
                            ProductInfo, Shop, User)
from backend.permissions import IsOrderUserOwner, IsShop
from backend.utils import file_shop_load, link_shop_load
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
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


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = serialyzers.UserSerialyzer


class UserView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serialyzers.UserSerialyzer

    def get_object(self):
        return self.request.user


class CategoryView(ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related('products')
    permission_classes = [IsAuthenticated]
    serializer_class = serialyzers.CategorySerialyzer


class ListProductView(ReadOnlyModelViewSet):
    queryset = Product.objects.prefetch_related('product_infos')
    permission_classes = [IsAuthenticated]
    serializer_class = serialyzers.ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    ...


class ProductView(ReadOnlyModelViewSet):
    queryset = ProductInfo.objects.prefetch_related('product_parameters__parameter')
    permission_classes = [IsAuthenticated]
    serializer_class = serialyzers.ProductInfoSerializer


class BuyerOrderView(ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated & IsOrderUserOwner]
    serializer_class = serialyzers.OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).exclude(state='basket')


class BasketView(ModelViewSet):
    queryset = OrderItem.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serialyzers.OrderItemSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        basket, _ = Order.objects.get_or_create(user=self.request.user, state='basket')
        return queryset.filter(order=basket)

    def perform_create(self, serializer):
        basket, _ = Order.objects.get_or_create(user=self.request.user, state='basket')
        return serializer.save(order=basket)


class OrderConfirmView(APIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated & IsOrderUserOwner]

    def change_quantity(self, items):
        save_list = [item.save() for item in items]
        OrderItem.objects.bulk_update(save_list, item.product_info.quantity)

    def verify_items(self, basket):
        errors = {}
        items = {}
        ordered_items = OrderItem.objects.filter(order=basket)
        for item in ordered_items:
            try:
                check_quantity = item.quantity <= item.product_info.quantity
                if check_quantity:
                    item.product_info.quantity -= item.quantity
                    items[item.product_info.pk] = item.product_info.quantity
                    continue
                else:
                    errors[item.product_info.pk] = 'incorrect quantity'
            except OrderItem.DoesNotExist:
                errors['0']('Item Not Found')
        return errors, items

    def check_basket(self):
        try:
            basket = Order.objects.get(user=self.request.user, state='basket')
            return basket
        except Order.DoesNotExist:
            return False

    def verify_contact(self, basket, request):
        if request.data.get('contact'):
            try:
                return Contact.objects.get(pk=request.data.get('contact'))
            except Contact.DoesNotExist:
                raise serialyzers.ValidationError('Wrong contact')
        if basket.contact:
            return basket.contact
        else:
            raise serialyzers.ValidationError('Contact must be set for order')

    def put(self, request):
        basket = self.check_basket()
        if basket:
            errors, items = self.verify_items(basket)
            contact = self.verify_contact(basket, request)
            if not errors and contact:
                for product, quantity in items.items():
                    instance = ProductInfo.objects.get(pk=product)
                    instance.quantity = quantity
                    instance.save()
                basket.state = 'new'
                basket.contact = contact
                basket.save(update_fields=['state', 'contact'])
                resp = {'Message: Order created'}
            else:
                resp = errors
        else:
            resp = {'message': 'basket is empty'}
        return Response(resp)


class ContactView(ModelViewSet):
    queryset = Contact.objects.all()
    permission_classes = [IsAuthenticated & IsOrderUserOwner]
    serializer_class = serialyzers.ContactSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ShopView(ModelViewSet):
    queryset = Shop.objects.prefetch_related('id__product_infos')
    permission_classes = [IsAuthenticated]
    serializer_class = serialyzers.ShopSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated & IsShop]
        return [permission() for permission in permission_classes]


class OrderShopView(ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsShop]
    serializer_class = serialyzers.OrderSerializer

    def get_queryset(self):
        shops = Shop.objects.filter(user=self.request.user)
        queryset = Order.objects.filter(ordered_items__product_info__shop__in=shops)
        return queryset


class ShopLoadView(APIView):
    queryset = Shop.objects.all()
    permission_classes = [IsAuthenticated & IsShop]

    def post(self, request):
        if request.data.get('file'):
            resp = file_shop_load(request.data['file'], request)
        elif request.data.get('link'):
            resp = link_shop_load(request.data['link'], request)
        else:
            resp = {'error': 'data not set'}
        return Response(resp)
