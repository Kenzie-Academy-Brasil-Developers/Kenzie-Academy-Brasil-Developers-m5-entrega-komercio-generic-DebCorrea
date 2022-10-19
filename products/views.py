from _project.utils.mixins import SerializerByMethodMixin
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .models import Product
from .permissions import IsSellerOrReadOnly
from .serializers import DetailedProductSerializer, GenericProductSerializer


class ProductView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly]

    queryset = Product.objects
    serializer_map = {
        "GET": GenericProductSerializer,
        "POST": DetailedProductSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
