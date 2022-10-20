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


class ProductAccountRelationshipTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.account_1 = Account.objects.create_user(
            {
                "username": "ale",
                "password": "abcd",
                "first_name": "alexandre",
                "last_name": "alves",
                "seller": True,
            }
        )

        cls.account_2 = Account.objects.create_user(
            {
                "username": "deb",
                "password": "1234",
                "first_name": "debora",
                "last_name": "correa",
                "seller": True,
            }
        )

        cls.product_1_data = {
            "description": "Celular boladão",
            "price": "1000.99",
            "quantity": 67,
        }

        cls.product_2_data = {
            "description": "Mouse bonitinho",
            "price": "299.75",
            "quantity": 13,
        }

    def test_account_may_contain_multiple_products(self):
        """
        Verifica se uma `account` pode conter mais de um `product`
        """

        self.product_1 = Product.objects.create(
            description=self.product_1_data["description"],
            price=self.product_1_data["price"],
            quantity=self.product_1_data["quantity"],
            seller=self.account_1,
        )

        self.product_2 = Product.objects.create(
            description=self.product_2_data["description"],
            price=self.product_2_data["price"],
            quantity=self.product_2_data["quantity"],
            seller=self.account_1,
        )

        self.assertEquals(self.account_1.products.count(), 2)

        self.assertIs(self.product_1.seller, self.account_1)
        self.assertIs(self.product_2.seller, self.account_1)

    def test_product_may_contain_one_account_only(self):
        """
        Verifica se um `product` pode conter apenas um `seller`
        """

        self.product_1 = Product.objects.create(
            description=self.product_1_data["description"],
            price=self.product_1_data["price"],
            quantity=self.product_1_data["quantity"],
            seller=self.account_1,
        )

        self.product_1.seller = self.account_2
        self.product_1.save()

        self.assertNotIn(self.product_1, self.account_1.products.all())

        self.assertIn(self.product_1, self.account_2.products.all())
