from django.urls import path
from .views import VendorCreateListView, VendorReadUpdateDeleteView, VendorPerformance
from rest_framework.authtoken import views

urlpatterns = [
    path('', VendorCreateListView.as_view(), name='vendor-create-list'),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('<vendor_id>/', VendorReadUpdateDeleteView.as_view(), name='vendor-read-update-delete'),
    path('<vendor_id>/performance', VendorPerformance.as_view(), name='vendor-read-update-delete'),
]