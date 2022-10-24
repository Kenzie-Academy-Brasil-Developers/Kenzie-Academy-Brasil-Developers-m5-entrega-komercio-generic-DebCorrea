from rest_framework.permissions import BasePermission
from rest_framework.views import Request, View

from .models import Product

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsSellerOrReadOnly(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_seller
        )


class IsProductOwnerOrReadOnly(BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: View,
        obj: Product,
    ) -> bool:
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user == obj.seller
        )
