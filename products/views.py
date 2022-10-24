from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from utils.mixins import SerializerByMethodMixin

from .models import Product
from .permissions import IsProductOwnerOrReadOnly, IsSellerOrReadOnly
from .serializers import DetailedProductSerializer, GenericProductSerializer


class ProductView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly]

    queryset = Product.objects.all()
    serializer_map = {
        "GET": GenericProductSerializer,
        "POST": DetailedProductSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProductOwnerOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = DetailedProductSerializer
