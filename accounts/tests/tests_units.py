import uuid

from accounts.models import Account
from django.test import TestCase


class AccountsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.account = Account.objects.create_user(
            {
                "username": "ale",
                "password": "abcd",
                "first_name": "alexandre",
                "last_name": "alves",
            }
        )

    def test_id_is_valid_uuid(self):
        """
        Verifica se o `id` gerado é um UUID válido
        """

        self.assertTrue(uuid.UUID(str(self.account.id)))

    def test_id_is_not_editable(self):
        """
        Verifica se `id` não é um campo editável
        """

        self.assertFalse(self.account._meta.get_field("id").editable)

    def test_username_max_length(self):
        """
        Verifica se `username` tem `max_length` esperado
        """

        max_length = self.account._meta.get_field("username").max_length

        self.assertEqual(max_length, 150)

    def test_username_is_unique(self):
        """
        Verifica se `username` tem constraint `unique`
        """

        self.assertTrue(self.account._meta.get_field("username").unique)

    def test_first_name_max_length(self):
        """
        Verifica se `max_length` de `first_name` é o esperado
        """

        max_length = self.account._meta.get_field("first_name").max_length

        self.assertEqual(max_length, 50)

    def test_last_name_max_length(self):
        """
        Verifica se `max_length` de `last_name` é o esperado
        """

        max_length = self.account._meta.get_field("last_name").max_length

        self.assertEqual(max_length, 50)

    def test_is_seller_default(self):
        """
        Verifica se o default de `is_seller` é False
        """

        self.assertFalse(self.account._meta.get_field("is_seller").default)
