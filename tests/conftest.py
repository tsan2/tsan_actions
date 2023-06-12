import pytest
from myproject.apps.genius.models import User

@pytest.fixture(autouse=False)
def create_user(client):
    data = {'id': 1, 'name': 'test', 'email': 'test@gmail.com', 'password': 'test'}
    response = client.post('/users/', data, format='json')
    return User.objects.get()