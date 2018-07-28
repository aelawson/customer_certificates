import app
import pytest

from falcon import testing

@pytest.fixture()
def client():
    return testing.TestClient(app.create())

class TestHello():
    def test_get_hello_world(self, client):
        expected = 'Hello World!'
        result = client.simulate_get('/hello')

        assert expected == result.text