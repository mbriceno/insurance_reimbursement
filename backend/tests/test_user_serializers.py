import pytest
from django.contrib.auth import get_user_model
from api.serializers import UserRegistrationSerializer, UserProfileSerializer

User = get_user_model()

@pytest.mark.django_db
class TestUserSerializers:
    def test_registration_serializer_valid_data(self):
        data = {
            "email": "newuser@example.com",
            "password": "strongpassword123"
        }
        serializer = UserRegistrationSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["email"] == data["email"]
        assert serializer.validated_data["password"] == data["password"]

    def test_registration_serializer_weak_password(self):
        data = {
            "email": "newuser@example.com",
            "password": "abc"
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_profile_serializer_read_only_role(self):
        user = User.objects.create_user(email="test@example.com", password="password123", role=User.Role.CUSTOMER)
        data = {
            "email": "updated@example.com",
            "role": User.Role.ADMIN
        }
        serializer = UserProfileSerializer(instance=user, data=data, partial=True)
        assert serializer.is_valid()
        serializer.save()
        user.refresh_from_db()
        # Email should update if allowed, but role should NOT
        assert user.role == User.Role.CUSTOMER
