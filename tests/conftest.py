import pytest

from falcon import testing

import app

@pytest.fixture(scope='session')
def client(request):
    return testing.TestClient(app.create())
