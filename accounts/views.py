from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from accounts.models import Account
from accounts.permissions import IsAccountOwner
from accounts.serializers import (AccountDeactivateActivateSerializer,
                                  AccountSerializer)


class AccountView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountNewestView(generics.ListAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        num = self.request.parser_context["kwargs"]["num"]

        queryset = Account.objects.all().order_by("-date_joined").values()

        return queryset[:num]


class AccountUpdateView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        request.data["is_active"] = request.user.is_active
        return self.update(request, *args, **kwargs)


class AccountDeactivateActivateView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Account.objects.all()
    serializer_class = AccountDeactivateActivateSerializer
