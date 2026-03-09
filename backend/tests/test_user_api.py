import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_registration(self):
        url = reverse("register")
        data = {"email": "apiuser@example.com", "password": "apipassword123"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == data["email"]
        assert response.data["role"] == "CUSTOMER"

    def test_profile_unauthenticated(self):
        url = reverse("me")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_profile_authenticated(self):
        user = User.objects.create_user(email="authuser@example.com", password="password123")
        self.client.force_authenticate(user=user)
        url = reverse("me")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email
        assert response.data["role"] == user.role
