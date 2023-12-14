from django.urls import path, include
from .views import PurchaseOrderCreateListView, PurchaseOrderReadUpdateDeleteView

urlpatterns = [
    path('', PurchaseOrderCreateListView.as_view(), name='purchase-order-create-list'),
    path('<purchase_order_id>', PurchaseOrderReadUpdateDeleteView.as_view(), name='purchase-order-read-update-delete')
]
