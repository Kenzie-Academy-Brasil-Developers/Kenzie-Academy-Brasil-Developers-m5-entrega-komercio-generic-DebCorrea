import uuid

from accounts.models import Account
from django.test import TestCase
from products.models import Product


class ProductsModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        account = Account.objects.create_user(
            {
                "username": "ale",
                "password": "abcd",
                "first_name": "alexandre",
                "last_name": "alves",
                "seller": True,
            }
        )

        product_data = {
            "description": "Mouse bonitinho",
            "price": 299.75,
            "quantity": 13,
            "seller": account,
        }

        cls.product = Product.objects.create(**product_data)

    def test_id_is_valid_uuid(self):
        """
        Verifica se o `id` gerado é um UUID válido
        """

        self.assertTrue(uuid.UUID(str(self.product.id)))

    def test_id_is_not_editable(self):
        """
        Verifica se `id` não é um campo editável
        """

        self.assertFalse(self.product._meta.get_field("id").editable)

    def test_price_decimal_fields(self):
        """
        Verifica se `price` tem limites de campo esperados
        """

        self.assertEqual(self.product._meta.get_field("price").max_digits, 10)
        self.assertEqual(
            self.product._meta.get_field("price").decimal_places, 2
        )

    def test_is_active_default(self):
        """
        Verifica se o default de `is_active` é True
        """

        self.assertTrue(self.product._meta.get_field("is_active").default)
