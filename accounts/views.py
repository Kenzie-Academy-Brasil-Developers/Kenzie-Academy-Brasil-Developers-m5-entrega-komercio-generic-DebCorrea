from rest_framework import generics

from accounts.models import Account
from accounts.serializers import AccountSerializer


class AccountView(generics.ListCreateAPIView):
    queryset = Account.objects
    serializer_class = AccountSerializer


class AccountNewestView(generics.ListAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        num = self.request.parser_context["kwargs"]["num"]

        queryset = Account.objects.all().order_by("date_joined").values()

        return queryset[:num]
