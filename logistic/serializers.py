from rest_framework import serializers, generics
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions_data = validated_data.pop('positions')
        stock = Stock.objects.create(**validated_data)
        for position_data in positions_data:
            StockProduct.objects.create(stock=stock, **position_data)
        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions')
        positions = instance.positions.all() if hasattr(instance, 'positions') else []
        positions = list(positions)
        stock = super().update(instance, validated_data)

        for position_data in positions_data:
            position = positions.pop(0)
            position.product = position_data.get('product', position.product)
            position.quantity = position_data.get('quantity', position.quantity)
            position.price = position_data.get('price', position.price)
            position.save()

        for position in positions:
            position.delete()

        return stock
