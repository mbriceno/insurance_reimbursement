from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from models.pet import Pet
from api.serializers import PetSerializer

class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'SUPPORT']:
            return Pet.objects.all()
        return Pet.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
