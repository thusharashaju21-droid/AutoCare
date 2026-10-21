from django.contrib.auth.models import User
from rest_framework import serializers
from service.models import ServiceRequest


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]

        read_only_fields = ["id"]


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ServiceRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceRequest
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_date",
        ]

    def validate_vehicle_number(self, value):
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                "Vehicle number cannot be empty."
            )

        if len(value) > 20:
            raise serializers.ValidationError(
                "Vehicle number cannot exceed 20 characters."
            )

        return value

    def validate_vehicle_model(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Vehicle model cannot be empty."
            )

        return value.strip()

    def validate_problem_description(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Problem description cannot be empty."
            )

        return value.strip()