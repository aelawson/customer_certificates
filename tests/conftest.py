import pytest

from faker import Faker
from falcon import testing

import app

@pytest.fixture(scope='session')
def client(request):
    return testing.TestClient(app.create())

@pytest.fixture(scope='session')
def fake(request):
    return Faker()
