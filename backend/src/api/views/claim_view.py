from api.repositories.claim_repository import ClaimRepository
from api.selectors.claim_selector import ClaimSelector
from api.serializers import ClaimSerializer
from api.services.claim_service import ClaimService
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ClaimViewSet(viewsets.ModelViewSet):
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        selector = ClaimSelector()
        return selector.get_queryset_for_user(self.request.user)

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "insurance": {"type": "integer"},
                    "invoice": {"type": "string", "format": "binary"},
                    "invoice_date": {"type": "string", "format": "date"},
                    "amount": {"type": "number", "format": "decimal"},
                    "date_of_event": {"type": "string", "format": "date"},
                },
                "required": [
                    "insurance",
                    "invoice",
                    "invoice_date",
                    "amount",
                    "date_of_event",
                ],
            },
        },
        responses={201: ClaimSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        claim_repo = ClaimRepository()
        claim_service = ClaimService(claim_repo)

        try:
            insurance = serializer.validated_data["insurance"]
            invoice = serializer.validated_data["invoice"]
            invoice_date = serializer.validated_data["invoice_date"]
            amount = serializer.validated_data["amount"]
            date_of_event = serializer.validated_data["date_of_event"]

            claim = claim_service.submit_claim(
                user=request.user,
                insurance=insurance,
                invoice=invoice,
                invoice_date=invoice_date,
                amount=amount,
                date_of_event=date_of_event,
            )

            return Response(
                ClaimSerializer(claim).data, status=status.HTTP_201_CREATED,
            )

        except PermissionError as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST,
            )

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        if user.role not in ["SUPPORT", "ADMIN"]:
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        instance = self.get_object()

        # Only allow updating status and review_notes
        allowed_fields = ["status", "review_notes"]
        update_data = {
            k: v for k, v in request.data.items() if k in allowed_fields
        }

        if not update_data:
            return Response(
                {"detail": "No valid fields provided for update."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            instance, data=update_data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
