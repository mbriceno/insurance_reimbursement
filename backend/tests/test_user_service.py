import pytest
from django.contrib.auth import get_user_model
from api.services.user_service import UserService

User = get_user_model()

@pytest.mark.django_db
class TestUserService:
    def test_create_user_success(self):
        email = "test@example.com"
        password = "password123"
        user = UserService.create_user(email=email, password=password)
        
        assert user.email == email
        assert user.check_password(password)
        assert user.role == User.Role.CUSTOMER
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_user_duplicate_email(self):
        email = "test@example.com"
        password = "password123"
        UserService.create_user(email=email, password=password)
        
        with pytest.raises(Exception): # Django will raise IntegrityError
            UserService.create_user(email=email, password="anotherpassword")
