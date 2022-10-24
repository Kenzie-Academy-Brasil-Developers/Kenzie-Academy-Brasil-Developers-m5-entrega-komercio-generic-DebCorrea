from products.models import Product
from rest_framework.test import APITestCase


class ProductViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/products/"

        cls.ACCOUNT_URL = "/api/accounts/"

        cls.LOGIN_URL = "/api/login/"

        cls.seller_account_data = {
            "username": "ale",
            "password": "abcd",
            "first_name": "alexandre",
            "last_name": "alves",
            "is_seller": True,
        }

        cls.common_account_data = {
            "username": "deb",
            "password": "1234abcd",
            "first_name": "deb",
            "last_name": "correa",
        }

        cls.product_data = {
            "description": "Mouse bonitinho",
            "price": 99.75,
            "quantity": 13,
        }

    def test_seller_can_create_product(self):
        """
        Verifica se um vendedor consegue criar um produto corretamente
        """
        self.client.post(self.ACCOUNT_URL, self.seller_account_data)

        seller_login = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.seller_account_data["username"],
                "password": self.seller_account_data["password"],
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {seller_login.data['token']}",
        )

        response = self.client.post(self.BASE_URL, self.product_data)

        self.assertEqual(response.status_code, 201)

        self.assertEqual(Product.objects.count(), 1)

    def test_returned_seller_product_creation(self):
        """
        Verifica se `seller` é retornado no formato esperado
        na criação do produto
        """
        seller = self.client.post(self.ACCOUNT_URL, self.seller_account_data)

        seller_login = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.seller_account_data["username"],
                "password": self.seller_account_data["password"],
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {seller_login.data['token']}",
        )

        product = self.client.post(self.BASE_URL, self.product_data)

        self.assertEqual(product.data["seller"], seller.data)

    def test_common_account_can_not_create_product(self):
        """
        Verifica se um usuário comum não consegue criar um produto
        """
        self.client.post(self.ACCOUNT_URL, self.common_account_data)

        common_user_login = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.common_account_data["username"],
                "password": self.common_account_data["password"],
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {common_user_login.data['token']}",
        )

        response = self.client.post(self.BASE_URL, self.product_data)

        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            response.data,
            {
                "detail": "You do not have permission to perform this action.",
            },
        )

        self.assertEqual(Product.objects.count(), 0)

    def test_create_product_missing_keys(self):
        """
        Verifica se requisição retorna erro com chaves faltando no body
        """
        self.client.post(self.ACCOUNT_URL, self.seller_account_data)

        seller_login = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.seller_account_data["username"],
                "password": self.seller_account_data["password"],
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {seller_login.data['token']}",
        )

        response = self.client.post(self.BASE_URL, {})

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.data,
            {
                "description": ["This field is required."],
                "price": ["This field is required."],
                "quantity": ["This field is required."],
            },
        )

    def test_product_quantity_must_be_positive(self):
        """
        Verifica se um produto não pode ter quantidade negativa
        """
        self.client.post(self.ACCOUNT_URL, self.seller_account_data)

        seller_login = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.seller_account_data["username"],
                "password": self.seller_account_data["password"],
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {seller_login.data['token']}",
        )

        response = self.client.post(
            self.BASE_URL,
            {
                "description": self.product_data["description"],
                "price": self.product_data["price"],
                "quantity": -13,
            },
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.data,
            {"quantity": ["Ensure this value is greater than or equal to 0."]},
        )

    def test_product_owner_can_update_it(self):
        """
        Verifica se o vendedor do produto pode editá-lo
        """
        self.client.post(self.ACCOUNT_URL, self.seller_account_data)

        seller_login = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.seller_account_data["username"],
                "password": self.seller_account_data["password"],
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {seller_login.data['token']}",
        )

        product = self.client.post(self.BASE_URL, self.product_data)

        response = self.client.patch(
            f"{self.BASE_URL}{product.data['id']}/",
            {
                "description": "Smartband XYZ 1000000",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["description"], "Smartband XYZ 1000000")

    def test_not_product_owner_can_not_update_it(self):
        """
        Verifica se o usuário não dono do produto não pode editá-lo
        """
        self.client.post(self.ACCOUNT_URL, self.seller_account_data)

        self.client.post(self.ACCOUNT_URL, self.common_account_data)

        seller_login = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.seller_account_data["username"],
                "password": self.seller_account_data["password"],
            },
        )

        common_login = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.common_account_data["username"],
                "password": self.common_account_data["password"],
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {seller_login.data['token']}",
        )

        product = self.client.post(self.BASE_URL, self.product_data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {common_login.data['token']}",
        )

        response = self.client.patch(
            f"{self.BASE_URL}{product.data['id']}/",
            {
                "description": "Smartband XYZ 1000000",
            },
        )

        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            response.data,
            {
                "detail": "You do not have permission to perform this action.",
            },
        )

    def test_products_listing(self):
        """
        Verifica se a listagem de produtos funciona como esperado
        e não requer autorização
        """
        response = self.client.get(self.BASE_URL)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["count"], 0)

    def test_product_filter(self):
        """
        Verifica se a filtragem de produtos funciona corretamente
        e não requer autorização
        """
        self.client.post(self.ACCOUNT_URL, self.seller_account_data)

        seller_login = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.seller_account_data["username"],
                "password": self.seller_account_data["password"],
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {seller_login.data['token']}",
        )

        product = self.client.post(self.BASE_URL, self.product_data)

        self.client.credentials(HTTP_AUTHORIZATION="")

        response = self.client.get(f"{self.BASE_URL}{product.data['id']}/")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data, product.data)

    def test_returned_seller_product_listing(self):
        """
        Verifica se `seller` é retornado no formato esperado
        na listagem do produto
        """
        seller = self.client.post(self.ACCOUNT_URL, self.seller_account_data)

        seller_login = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.seller_account_data["username"],
                "password": self.seller_account_data["password"],
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {seller_login.data['token']}",
        )

        self.client.post(self.BASE_URL, self.product_data)

        products = self.client.get(self.BASE_URL)

        self.assertEqual(
            str(products.data["results"][0]["seller_id"]),
            seller.data["id"],
        )
