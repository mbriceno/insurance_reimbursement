from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Claim, Pet, PetInsurance
from .services.user_service import UserService

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "role")
        read_only_fields = ("role",)

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long.",
            )
        return value

    def create(self, validated_data):
        return UserService.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "role")
        read_only_fields = ("role",)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["email"] = user.email
        return token


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ("id", "owner", "name", "species", "birth_date")
        read_only_fields = ("owner",)

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class PetInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetInsurance
        fields = (
            "id",
            "owner",
            "pet",
            "coverage_start",
            "coverage_end",
            "status",
            "created_at",
        )
        read_only_fields = ("owner", "coverage_end", "status", "created_at")

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class ClaimSerializer(serializers.ModelSerializer):
    invoice = serializers.FileField()

    class Meta:
        model = Claim
        fields = (
            "id",
            "insurance",
            "invoice",
            "invoice_date",
            "amount",
            "status",
            "review_notes",
            "date_of_event",
            "created_at",
        )
        read_only_fields = ("status", "review_notes", "created_at")

    def validate_insurance(self, value):
        user = self.context["request"].user
        if value.owner != user:
            raise serializers.ValidationError(
                "You can only submit claims for your own insurance policies.",
            )
        return value
