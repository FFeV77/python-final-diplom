from backend.models import (Category, Contact, Order, OrderItem, Parameter, Product, ProductInfo,
                            ProductParameter, Shop, User)
from rest_framework.serializers import ModelSerializer, CharField, IntegerField, ValidationError


class CreateUserSerialyzer(ModelSerializer):
    password = CharField(required=True, write_only=True, label='Пароль')
    password2 = CharField(required=True, write_only=True, label='Проверка пароля')
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password2', 'type', 'first_name', 'last_name', 'father_name', 'company', 'position', 'auth_token']
        read_only_fields = ['auth_token', 'id']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({'status': 'error', 'message': 'пароль не совпадает'})
        attrs.pop('password2')
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'type', 'first_name', 'last_name', 'father_name', 'company', 'position', 'token']
        read_only_fields = ['id', 'token']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ParameterSerializer(ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['name']


class ProductParameterSerialyzer(ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = ['parameter', 'value']

    def to_internal_value(self, data):
        ret = []
        for key, val in data.items():
            ret.append({'parameter': key, 'value': val})
        return ret


class CategorySerialyzer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'category']


class ProductInfoSerializer(ModelSerializer):
    product_parameters = ProductParameterSerialyzer(many=True)
    # product = SlugRelatedField('name')

    class Meta:
        model = ProductInfo
        fields = ['external_id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters']


class ShopSerializer(ModelSerializer):
    product_infos = ProductInfoSerializer(many=True)
    categories = CategorySerialyzer(many=True)

    class Meta:
        model = Shop
        fields = ['id', 'name', 'user', 'state', 'categories', 'product_infos']


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_info', 'quantity']


class OrderSerializer(ModelSerializer):
    contact = ContactSerializer()
    ordered_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['dt', 'state', 'contact', 'ordered_items']


class ProductInfoLoadSerializer(ModelSerializer):
    id = IntegerField(source='external_id')
    parameters = ProductParameterSerialyzer(source='product_parameters')

    class Meta:
        model = ProductInfo
        fields = ['id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'parameters']


class ShopLoadSerializer(ModelSerializer):
    shop = CharField(source='name')
    goods = ProductInfoLoadSerializer(many=True, source='product_infos')
    categories = CategorySerialyzer(many=True)

    class Meta:
        model = Shop
        fields = ['shop', 'user', 'state', 'categories', 'goods']

    def create(self, validated_data):
        categories = validated_data.pop('categories')
        for category in categories:
            Category.objects.update_or_create(id=category['id'], defaults={'name': category['name']})
        # product_infos = validated_data.pop('product_infos')
        # shop = Shop.objects.create(**validated_data)
        # shop.categories.set(categories)
        # shop.user_id.set()
        # for product in product_infos:
        #     parameters = product.pop('product_parameters')
        #     ProductInfo.objects.create(**product)
        #     for parameter in parameters:
        #         ProductParameter.objects.create(**parameter)
        return shop
