import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from backend.models import User
from django.urls import reverse


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


@pytest.mark.celery(result_backend='redis://python-final-diplom-redis-1:6379')
@pytest.mark.django_db
def test_load(client, django_user_model):
    data = {'file': 'data/shop1.yaml'}
    user_shop = django_user_model.objects.create_user(password='test', email='test@email.ru', type='shop')
    user = django_user_model.objects.create_user(password='test', email='test1@email.ru')

    req = client.post('/api/load', data=data)
    assert req.status_code == 401

    client.force_authenticate(user)
    req = client.post('/api/load', data=data)
    assert req.status_code == 403

    client.force_authenticate(user_shop)
    req = client.post('/api/load', data=data)
    assert req.status_code == 200


@pytest.mark.celery(result_backend='redis://python-final-diplom-redis-1:6379')
@pytest.mark.django_db
def test_basket(client, django_user_model):
    user = django_user_model.objects.create_user(password='test', email='test1@email.ru', is_active=True)
    data = {
            "product_info": 1,
            "quantity": 1,
            }
    client.force_authenticate(user)
    req = client.post('/api/basket/', data=data)

    assert req.status_code == 200
