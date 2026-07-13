import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import CustomUser

@pytest.mark.django_db
class TestAuthentication:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.register_url = reverse('auth_register')
        self.login_url = reverse('auth_login')
        self.change_password_url = reverse('auth_change_password')
        self.reset_request_url = reverse('auth_password_reset')
        self.reset_confirm_url = reverse('auth_password_reset_confirm')

    def test_register_customer_success(self):
        payload = {
            "email": "test_cust@example.com",
            "password": "password123",
            "role": "CUSTOMER",
            "first_name": "Charlie",
            "last_name": "Brown",
            "phone": "555-1234",
            "gender": "MALE",
            "preferred_notification": "EMAIL"
        }
        response = self.client.post(self.register_url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['user']['email'] == "test_cust@example.com"
        assert response.data['user']['role'] == "CUSTOMER"
        assert "tokens" in response.data

    def test_login_success(self):
        CustomUser.objects.create_user(
            email="login_test@example.com",
            password="password123",
            role="CUSTOMER"
        )
        payload = {
            "email": "login_test@example.com",
            "password": "password123"
        }
        response = self.client.post(self.login_url, payload, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert response.data['user']['email'] == "login_test@example.com"

    def test_change_password_authenticated(self):
        user = CustomUser.objects.create_user(
            email="change_pwd@example.com",
            password="password123",
            role="CUSTOMER"
        )
        self.client.force_authenticate(user=user)
        payload = {
            "old_password": "password123",
            "new_password": "newsecurepassword123"
        }
        response = self.client.post(self.change_password_url, payload, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        self.client.logout()
        login_response = self.client.post(self.login_url, {
            "email": "change_pwd@example.com",
            "password": "newsecurepassword123"
        }, format='json')
        assert login_response.status_code == status.HTTP_200_OK

    def test_password_reset_flow(self):
        CustomUser.objects.create_user(
            email="reset_me@example.com",
            password="password123",
            role="CUSTOMER"
        )
        response = self.client.post(self.reset_request_url, {
            "email": "reset_me@example.com"
        }, format='json')
        assert response.status_code == status.HTTP_200_OK
        uidb64 = response.data['uidb64']
        token = response.data['token']
        
        confirm_payload = {
            "uidb64": uidb64,
            "token": token,
            "new_password": "newpassword12345"
        }
        confirm_response = self.client.post(self.reset_confirm_url, confirm_payload, format='json')
        assert confirm_response.status_code == status.HTTP_200_OK
        
        login_response = self.client.post(self.login_url, {
            "email": "reset_me@example.com",
            "password": "newpassword12345"
        }, format='json')
        assert login_response.status_code == status.HTTP_200_OK
