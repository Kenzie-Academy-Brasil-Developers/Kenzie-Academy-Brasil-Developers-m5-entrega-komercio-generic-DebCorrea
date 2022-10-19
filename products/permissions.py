from rest_framework.permissions import BasePermission
from rest_framework.views import Request, View

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsSellerOrReadOnly(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_seller
        )
