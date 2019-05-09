import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.schedules.factories import UserFactory


@pytest.fixture(scope="session")
def api_client():
    return APIClient()


@pytest.fixture()
def auth_api_client(db):
    client = APIClient()
    user = UserFactory()
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    client.user = user
    return client
