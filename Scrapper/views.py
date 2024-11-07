from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Brand
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['asin', 'sku', 'name']
    search_fields = ['name']
    ordering_fields = ['name', 'asin', 'sku']

    def get_queryset(self):
        brand_name = self.kwargs.get('brand_name')
        try:
            brand = Brand.objects.get(name=brand_name)
        except Brand.DoesNotExist:
            return Product.objects.none()
        return Product.objects.filter(brand=brand)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
