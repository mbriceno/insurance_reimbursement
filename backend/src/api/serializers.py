from rest_framework import serializers
from models.pet import Pet
from models.insurance import PetInsurance
from models.claim import Claim

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'owner', 'name', 'species', 'birth_date']
        read_only_fields = ['owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class PetInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetInsurance
        fields = ['id', 'owner', 'pet', 'coverage_start', 'coverage_end', 'status', 'created_at']
        read_only_fields = ['owner', 'coverage_end', 'status', 'created_at']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['id', 'insurance', 'invoice', 'invoice_date', 'amount', 'status', 'review_notes', 'date_of_event', 'created_at']
        read_only_fields = ['status', 'review_notes', 'created_at']

    def validate_insurance(self, value):
        user = self.context['request'].user
        if value.owner != user:
            raise serializers.ValidationError("You can only submit claims for your own insurance policies.")
        return value
