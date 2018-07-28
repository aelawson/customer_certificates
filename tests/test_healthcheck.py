import app
import pytest

from falcon import testing

@pytest.fixture()
def client():
    return testing.TestClient(app.create())

class TestHealthcheck():
    def test_healthcheck(self, client):
        expected = { 'api': 1, 'database': 1 }
        result = client.simulate_get('/healthcheck')

        assert expected == result.json