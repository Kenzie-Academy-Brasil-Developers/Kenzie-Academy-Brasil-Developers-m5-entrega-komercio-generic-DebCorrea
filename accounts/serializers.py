from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account

        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        ]

        read_only_fields = [
            "date_joined",
            "is_active",
            "is_superuser",
        ]
