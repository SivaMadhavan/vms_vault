from django.urls import path, include
from .views import PurchaseOrderCreateList, PurchaseOrderReadUpdateDelete

urlpatterns = [
    path('', PurchaseOrderCreateList.as_view(), name='purchase-order-create-list'),
    path('<purchase_order_id>', PurchaseOrderReadUpdateDelete.as_view(), name='purchase-order-create-list')
]
