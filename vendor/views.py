from .models import Vendor, HistoricalPerformance
from rest_framework.status import (
    HTTP_404_NOT_FOUND, HTTP_200_OK,
    HTTP_204_NO_CONTENT, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST)
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from .serializers import VendorCreateListSerializer, VendorUpdateSerializer, VendorPerformanceSerializer
from .authentication import CustomAuthentication


class VendorCreateListView(GenericAPIView, ListModelMixin):
    # authentication_classes = (CustomAuthentication,)
    serializer_class = VendorCreateListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VendorCreateListSerializer
        return VendorCreateListSerializer

    def post(self, request):
        serializer_class = self.serializer_class(data=request.data)
        if not serializer_class.is_valid():
            return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)
        response = Vendor().create(request)
        status_code = HTTP_201_CREATED if response else HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)

    def get_queryset(self):
        return Vendor.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class VendorReadUpdateDeleteView(GenericAPIView):
    def get(self, *args, **kwargs):
        vendor = Vendor.objects.get(pk=kwargs.get('vendor_id'))
        data = VendorCreateListSerializer(vendor).data
        return Response(data, status=HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        serializer = VendorUpdateSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        Vendor.objects.filter(pk=kwargs.get('vendor_id')).update(**data)
        return Response({"message": "Updated Successfully"}, status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        message = "Deleted Successfully"
        status = HTTP_204_NO_CONTENT
        try:
            vendor = Vendor.objects.get(pk=kwargs.get('vendor_id'))
            vendor.delete()
        except Vendor.DoesNotExist as e:
            message = str(e)
            status = HTTP_404_NOT_FOUND
        return Response({"message": message}, status=status)


class VendorPerformance(GenericAPIView):
    authentication_classes = (CustomAuthentication,)

    def get(self, request, *args, **kwargs):
        data = HistoricalPerformance.get_metrics(request, *args, **kwargs)
        data = VendorPerformanceSerializer(data).data
        return Response(data, status=HTTP_200_OK)
