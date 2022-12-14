from accounts.serializers import AccountSerializer
from rest_framework import serializers

from .models import Product


class DetailedProductSerializer(serializers.ModelSerializer):
    seller = AccountSerializer(read_only=True)

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
