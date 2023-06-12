import pytest

from rest_framework import status

from myproject.apps.genius.models import User, Action

data_users = {'id':1, 'name':'test', 'email':'test@gmail.com', 'password':'test'}
data_actions = {'id': 1, 'type_action':'work', 'name': 'test', 'description':'test', 'time': '04:53:20', 'date': '2023-06-12'}

@pytest.mark.django_db
def test_users_get(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert len(response.data) == User.objects.count()

@pytest.mark.django_db
def test_users_create(client):
    response = client.post('/users/', data_users, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.get().name == 'test'

@pytest.mark.django_db
def test_action_get(client):
    response = client.get('/actions/')
    assert response.status_code == 200
    assert len(response.data) == Action.objects.count()

@pytest.mark.django_db
def test_action_create(client, create_user):
    user = create_user
    data_actions['user'] = user
    response = client.post('/actions/', data_actions, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Action.objects.get().name == 'test'
