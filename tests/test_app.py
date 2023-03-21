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
def test_register(client, user_factory):
    data = {"email": "7@name.ru", "type": "shop", "password": "test"}

    req = client.post('/api/user/register', data=data)
    # print(req)
    assert req.status_code == 201
    resp = req.json()
    assert resp['email'] == data['email']
