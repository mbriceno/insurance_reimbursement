from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from models.insurance import PetInsurance
from api.serializers import PetInsuranceSerializer

class InsuranceViewSet(viewsets.ModelViewSet):
    serializer_class = PetInsuranceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'SUPPORT']:
            return PetInsurance.objects.all()
        return PetInsurance.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
