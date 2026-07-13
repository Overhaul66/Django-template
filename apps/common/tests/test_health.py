import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestHealthEndpoint:
    def test_health_endpoint_returns_ok(self, client):
        response = client.get(reverse("health-check"))

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
