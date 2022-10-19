from accounts.models import Account
from rest_framework import serializers

from .models import Product


class AccountCustomSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account

        fields = [
            "id",
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


class DetailedProductSerializer(serializers.ModelSerializer):
    seller = AccountCustomSerializer(read_only=True)

    class Meta:
        model = Product

        fields = [
            "id",
            "description",
            "price",
            "quantity",
            "is_active",
            "seller",
        ]

        read_only_fields = ["is_active"]


class GenericProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]

        read_only_fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]
