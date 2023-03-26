import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from backend.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_factory():
    def factory(*args, **kwargs):
        return baker.make(User, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_register(client):
    data = {"email": "7@name.ru", "type": "shop", "password": "test"}
    req = client.post('/api/register', data=data)

    assert req.status_code == 201
    resp = req.json()
    assert resp['email'] == data['email']


@pytest.mark.django_db
def test_load(client, django_user_model):
    data = {'file': 'data/shop1.yaml'}
    user_shop = django_user_model.objects.create_user(password='test', email='test@email.ru', type='shop')
    user = django_user_model.objects.create_user(password='test', email='test1@email.ru')
    req = client.post('/api/load', data=data)
    assert req.status_code == 401

    client.force_login(user)
    req = client.post('/api/load', data=data)
    assert req.status_code == 401

    client.force_login(user_shop)
    req = client.post('/api/load', data=data)
    assert req.status_code == 200
