from django.urls import path
from .views import VendorCreateListView, VendorReadUpdateDeleteView

urlpatterns = [
    path('', VendorCreateListView.as_view(), name='vendor-create-list'),
    path('<vendor_id>', VendorCreateListView.as_view(), name='vendor-read-update-delete')
]