from rest_framework import serializers
from .models import PurchaseOrder


class PurchaseOrderCreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        # fields = '__all__'
        exclude = ('vendor',)


class PurchaseOrderReadUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
