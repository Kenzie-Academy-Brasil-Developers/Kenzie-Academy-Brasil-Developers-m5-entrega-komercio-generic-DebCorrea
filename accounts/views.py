from rest_framework import generics

from accounts.models import Account
from accounts.serializers import AccountSerializer


class AccountView(generics.ListCreateAPIView):
    queryset = Account.objects
    serializer_class = AccountSerializer
