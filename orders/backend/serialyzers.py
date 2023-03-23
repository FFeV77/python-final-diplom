from backend.models import (Category, Parameter, Product, ProductInfo,
                            ProductParameter, Shop, User)
from rest_framework.serializers import ModelSerializer


class CreateUserSerialyzer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'type', 'first_name', 'last_name', 'father_name', 'company', 'position', 'auth_token']
        read_only_fields = ['auth_token', 'id']

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
        fields = []


class ProductParameterSerialyzer(ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = []


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

    class Meta:
        model = ProductInfo
        fields = ['external_id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters']


class ShopSerializer(ModelSerializer):
    product_infos = ProductInfoSerializer(many=True)
    categories = CategorySerialyzer(many=True)

    class Meta:
        model = Shop
        fields = ['id', 'name', 'user', 'state', 'categories', 'product_infos']
