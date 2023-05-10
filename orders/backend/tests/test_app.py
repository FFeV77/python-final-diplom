import pytest
import yaml
from backend.logic.utils import yaml_shop_load
from backend.models import Category, Parameter, Product, ProductInfo, ProductParameter, Shop, User
from django.urls import reverse
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

data = '''shop: Связной
categories:
  - id: 224
    name: Смартфоны
  - id: 15
    name: Аксессуары
  - id: 1
    name: Flash-накопители

goods:
  - id: 4216292
    category: 224
    model: apple/iphone/xs-max
    name: Смартфон Apple iPhone XS Max 512GB (золотистый)
    price: 110000
    price_rrc: 116990
    quantity: 14
    parameters:
      "Диагональ (дюйм)": 6.5
      "Разрешение (пикс)": 2688x1242
      "Встроенная память (Гб)": 512
      "Цвет": золотистый
  - id: 4216313
    category: 224
    model: apple/iphone/xr
    name: Смартфон Apple iPhone XR 256GB (красный)
    price: 65000
    price_rrc: 69990
    quantity: 9
    parameters:
      "Диагональ (дюйм)": 6.1
      "Разрешение (пикс)": 1792x828
      "Встроенная память (Гб)": 256
      "Цвет": красный
  - id: 4216226
    category: 224
    model: apple/iphone/xr
    name: Смартфон Apple iPhone XR 256GB (черный)
    price: 65000
    price_rrc: 69990
    quantity: 5
    parameters:
      "Диагональ (дюйм)": 6.1
      "Разрешение (пикс)": 1792x828
      "Встроенная память (Гб)": 256
      "Цвет": черный
  - id: 4672670
    category: 224
    model: apple/iphone/xr
    name: Смартфон Apple iPhone XR 128GB (синий)
    price: 60000
    price_rrc: 64990
    quantity: 7
    parameters:
      "Диагональ (дюйм)": 6.1
      "Разрешение (пикс)": 1792x828
      "Встроенная память (Гб)": 256
      "Цвет": синий'''


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_factory():
    def factory(*args, **kwargs):
        return baker.make(User, *args, **kwargs)
    return factory


@pytest.mark.celery(result_backend='redis://python-final-diplom-redis-1:6379')
@pytest.mark.django_db
def test_register(client):
    data = {"email": "987654345678@name.ru", "type": "shop", "password": "test", "password2": "test"}
    link = reverse('register')

    req = client.post(link, data=data)

    assert req.status_code == 201
    resp = req.json()
    assert resp['email'] == data['email']
    check = User.objects.get(email=data['email'])
    assert check


@pytest.mark.celery(result_backend='redis://python-final-diplom-redis-1:6379')
@pytest.mark.django_db
def test_user(client, django_user_model):
    user = django_user_model.objects.create_user(password='test', email='test1@email.ru', is_active=True)
    link = reverse('user')

    client.force_authenticate(user)
    req = client.get(link)

    assert req.status_code == 200
    resp = req.json()
    assert resp['email'] == user.email


@pytest.mark.celery(result_backend='redis://python-final-diplom-redis-1:6379')
@pytest.mark.django_db
def test_activate(client, django_user_model):
    user = django_user_model.objects.create_user(password='test', email='test1@email.ru', is_active=False)
    token = Token.objects.get(user=user)
    link = reverse('activation', kwargs={'id': user.pk, 'token': token.key})

    req = client.patch(link)

    assert req.status_code == 200
    chek_activate = User.objects.get(pk=user.pk)
    assert chek_activate.is_active


@pytest.mark.celery(result_backend='redis://python-final-diplom-redis-1:6379')
@pytest.mark.django_db
def test_contact(client, django_user_model):
    user = django_user_model.objects.create_user(password='test', email='test1@email.ru', is_active=True)
    data = {'city': 'Moskow', 'street': 'Red Squeare', 'phone': '9265920311'}
    link = reverse('contacts-list')

    client.force_authenticate(user)
    req = client.post(link, data=data)

    assert req.status_code == 201
    check = client.get(link)
    resp = check.json()
    assert len(resp) == 1


@pytest.mark.celery(result_backend='redis://python-final-diplom-redis-1:6379')
@pytest.mark.django_db
def test_shop_create(client, django_user_model):
    user = django_user_model.objects.create_user(password='test', email='test1@email.ru', is_active=True, type='shop')
    data = {'name': 'Связной'}
    link = reverse('shops-list')

    client.force_authenticate(user)
    req = client.post(link, data=data)

    assert req.status_code == 201
    check = client.get(link)
    resp = check.json()
    assert len(resp) == 1
    check_shop = client.get(reverse('shops-detail', kwargs={'pk': 1}))
    resp = check_shop.json()
    assert resp['name'] == data['name']


@pytest.mark.django_db
class TestOrders:
    def test_load(self, client, django_user_model):
        user_shop = django_user_model.objects.create_user(password='test', email='test@email.ru', type='shop', is_active=True)
        shop_data = yaml.load(data, Loader=yaml.Loader)

        client.force_authenticate(user_shop)
        yaml_shop_load(shop_data, user_shop)

        categories = Category.objects.count()
        assert categories == 3
        products = Product.objects.count()
        assert products == 4
        product_info = ProductInfo.objects.count()
        assert product_info == 4
        parameter = Parameter.objects.count()
        assert parameter == 4
        product_parameter = ProductParameter.objects.count()
        assert product_parameter == 16


# @pytest.mark.celery(result_backend='redis://python-final-diplom-redis-1:6379')
# @pytest.mark.django_db
# def test_basket(client, django_user_model):
#     user = django_user_model.objects.create_user(password='test', email='test1@email.ru', is_active=True)
#     data = {
#             "product_info": 1,
#             "quantity": 1,
#             }
#     client.force_authenticate(user)
#     req = client.post('/api/basket/', data=data)

#     assert req.status_code == 200
