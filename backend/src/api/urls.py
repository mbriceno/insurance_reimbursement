from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views.claim_view import ClaimViewSet
from .views.custom_token_view import CustomTokenObtainPairView
from .views.insurance_view import InsuranceViewSet
from .views.pet_view import PetViewSet
from .views.user_view import UserProfileView, UserRegistrationView

router = DefaultRouter()
router.register(r"pets", PetViewSet, basename="pet")
router.register(r"insurances", InsuranceViewSet, basename="insurance")
router.register(r"claims", ClaimViewSet, basename="claim")

urlpatterns = [
    path("auth/register/", UserRegistrationView.as_view(), name="register"),
    path("auth/me/", UserProfileView.as_view(), name="me"),
    path(
        "auth/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh",
    ),
    path("", include(router.urls)),
]
