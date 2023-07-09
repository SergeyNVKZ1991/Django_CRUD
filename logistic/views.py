from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'description']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['address', 'products']
    search_fields = ['address', 'positions__product__title', 'positions__product__description']
    ordering_fields = ['address', 'positions__quantity', 'positions__price']


class StockListView(generics.ListAPIView):
    serializer_class = StockSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('search', '')
        queryset = Stock.objects.filter(positions__product__title__icontains=search_query) | Stock.objects.filter(positions__product__description__icontains=search_query)
        return queryset.distinct()
