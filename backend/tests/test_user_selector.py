import pytest
from django.contrib.auth import get_user_model
from api.selectors.user_selector import UserSelector

User = get_user_model()

@pytest.mark.django_db
class TestUserSelector:
    def test_get_profile(self):
        user = User.objects.create_user(email="test@example.com", password="password123")
        profile = UserSelector.get_profile(user)
        assert profile == user
