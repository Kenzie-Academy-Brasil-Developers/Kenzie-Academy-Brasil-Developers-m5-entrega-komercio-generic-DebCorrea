from accounts.models import Account
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase


class AccountViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/accounts/"

        cls.LOGIN_URL = "/api/login/"

        cls.admin_account = Account.objects.create_superuser(
            username="gohan", first_name="go", last_name="han", password="1234"
        )

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

    def test_can_create_seller_account(self):
        """
        Verifica a criação de conta de vendedor com dados corretos
        """
        response = self.client.post(self.BASE_URL, self.seller_account_data)

        self.assertEqual(response.status_code, 201)

        self.assertEqual(Account.objects.count(), 2)

    def test_can_create_common_account(self):
        """
        Verifica a criação de conta comum com dados corretos
        """
        response = self.client.post(self.BASE_URL, self.common_account_data)

        self.assertEqual(response.status_code, 201)

        self.assertEqual(Account.objects.count(), 2)

    def test_if_password_is_hashed(self):
        """
        Verifica se a senha está sendo hasheada corretamente para
        permanência no banco
        """
        response = self.client.post(self.BASE_URL, self.seller_account_data)

        seller = Account.objects.get(id=response.data["id"])

        self.assertTrue(
            seller.check_password(self.seller_account_data["password"]),
        )

    def test_returning_keys(self):
        """
        Verifica se o retorno da requisição tem as chaves esperadas
        """
        response = self.client.post(self.BASE_URL, self.seller_account_data)

        expected_keys = {
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        }

        self.assertSetEqual(set(response.data.keys()), expected_keys)

    def test_duplicated_username_error(self):
        """
        Verifica se propriedade `username` tem constraint unique
        """
        self.client.post(self.BASE_URL, self.seller_account_data)

        response = self.client.post(self.BASE_URL, self.seller_account_data)

        self.assertEqual(response.status_code, 400)

        self.assertRaisesMessage(
            ValidationError,
            {
                "username": ["user with this username already exists."],
            },
        )

    def test_missing_keys_error(self):
        """
        Verifica se requisição retorna erro com chaves faltando no body
        """
        response = self.client.post(self.BASE_URL, {})

        self.assertEqual(response.status_code, 400)

        self.assertRaisesMessage(
            KeyError,
            {
                "username": ["This field is required."],
                "password": ["This field is required."],
                "first_name": ["This field is required."],
                "last_name": ["This field is required."],
            },
        )

    def test_seller_account_login(self):
        """
        Verifica se vendedor com credenciais válidas faz o login e
        recebe o token corretamente
        """
        seller = self.client.post(self.BASE_URL, self.seller_account_data)

        response = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.seller_account_data["username"],
                "password": self.seller_account_data["password"],
            },
        )

        token = Token.objects.get(user_id=seller.data["id"])

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data, {"token": token.key})

    def test_common_account_login(self):
        """
        Verifica se usuário comum com credenciais válidas faz o login e
        recebe o token corretamente
        """
        common_user = self.client.post(self.BASE_URL, self.common_account_data)

        response = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.common_account_data["username"],
                "password": self.common_account_data["password"],
            },
        )

        token = Token.objects.get(user_id=common_user.data["id"])

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data, {"token": token.key})

    def test_missing_keys_error(self):
        """
        Verifica se a requisição com chaves faltando retorna o erro esperado
        """
        response = self.client.post(self.LOGIN_URL, {})

        self.assertEqual(response.status_code, 400)

        self.assertRaisesMessage(
            KeyError,
            {
                "username": ["This field is required."],
                "password": ["This field is required."],
            },
        )

    def test_can_not_log_invalid_user(self):
        """
        Verifica se usuário com credenciais inválidas retorna erro
        """
        self.client.post(self.BASE_URL, self.common_account_data)

        response = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.common_account_data["username"],
                "password": "senhaerrada",
            },
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.data,
            {
                "non_field_errors":
                ["Unable to log in with provided credentials."],
            },
        )

    def account_owner_updates_account_data(self):
        """
        Verifica se o usuário dono da conta pode atualizar seus dados
        """
        seller = self.client.post(self.BASE_URL, self.seller_account_data)

        login = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.seller_account_data["username"],
                "password": self.seller_account_data["password"],
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {login.data['token']}",
        )

        response = self.client.patch(
            f"{self.BASE_URL}{seller.data['id']}/",
            {
                "username": "xandre",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["username"], "xandre")

    def account_owner_updates_account_data(self):
        """
        Verifica se o usuário não dono da conta não pode atualizar
        dados da conta
        """
        seller = self.client.post(self.BASE_URL, self.seller_account_data)

        self.client.post(self.BASE_URL, self.common_account_data)

        login = self.client.post(
            self.LOGIN_URL,
            {
                "username": self.common_account_data["username"],
                "password": self.common_account_data["password"],
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {login.data['token']}",
        )

        response = self.client.patch(
            f"{self.BASE_URL}{seller.data['id']}/",
            {
                "username": "xandre",
            },
        )

        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            response.data,
            {"detail": "You do not have permission to perform this action."},
        )

    def test_admin_can_deactivate_account(self):
        """
        Verifica se um admin pode desativar uma conta
        """
        seller = self.client.post(self.BASE_URL, self.seller_account_data)

        admin_login = self.client.post(
            self.LOGIN_URL,
            {
                "username": "gohan",
                "password": "1234",
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {admin_login.data['token']}",
        )

        response = self.client.patch(
            f"{self.BASE_URL}{seller.data['id']}/management/",
            {
                "is_active": False,
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.data["is_active"])

    def test_admin_can_reactivate_account(self):
        """
        Verifica se um admin pode reativar uma conta
        """
        seller = self.client.post(self.BASE_URL, self.seller_account_data)

        admin_login = self.client.post(
            self.LOGIN_URL,
            {
                "username": "gohan",
                "password": "1234",
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {admin_login.data['token']}",
        )

        self.client.patch(
            f"{self.BASE_URL}{seller.data['id']}/management/",
            {
                "is_active": False,
            },
        )

        response = self.client.patch(
            f"{self.BASE_URL}{seller.data['id']}/management/",
            {
                "is_active": True,
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.data["is_active"])

    def test_not_admin_can_not_deactivate_account(self):
        """
        Verifica se um não admin não pode desativar uma conta
        """
        seller = self.client.post(self.BASE_URL, self.seller_account_data)

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

        response = self.client.patch(
            f"{self.BASE_URL}{seller.data['id']}/management/",
            {
                "is_active": False,
            },
        )

        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            response.data,
            {"detail": "You do not have permission to perform this action."},
        )

    def test_not_admin_can_not_reactivate_account(self):
        """
        Verifica se um não admin não pode reativar uma conta
        """
        seller = self.client.post(self.BASE_URL, self.seller_account_data)

        self.client.post(self.BASE_URL, self.common_account_data)

        admin_login = self.client.post(
            self.LOGIN_URL,
            {
                "username": "gohan",
                "password": "1234",
            },
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {admin_login.data['token']}",
        )

        self.client.patch(
            f"{self.BASE_URL}{seller.data['id']}/management/",
            {
                "is_active": False,
            },
        )

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

        response = self.client.patch(
            f"{self.BASE_URL}{seller.data['id']}/management/",
            {
                "is_active": True,
            },
        )

        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            response.data,
            {"detail": "You do not have permission to perform this action."},
        )

    def test_accounts_listing(self):
        """
        Verifica se a listagem de usuários funciona como esperado
        e não requer autenticação
        """
        response = self.client.get(self.BASE_URL)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["count"], 1)
