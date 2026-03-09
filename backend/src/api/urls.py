from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.claim_view import ClaimViewSet
from .views.insurance_view import InsuranceViewSet
from .views.pet_view import PetViewSet

router = DefaultRouter()
router.register(r"pets", PetViewSet, basename="pet")
router.register(r"insurances", InsuranceViewSet, basename="insurance")
router.register(r"claims", ClaimViewSet, basename="claim")

urlpatterns = [
    path("", include(router.urls)),
]
