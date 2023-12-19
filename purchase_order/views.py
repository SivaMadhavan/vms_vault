from rest_framework.views import APIView
from vendor.authentication import CustomAuthentication
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseOrder
from .serializers import PurchaseOrderCreateListSerializer, PurchaseOrderUpdateSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView


class PurchaseOrderCreateListView(GenericAPIView, ListModelMixin):
    authentication_classes = (CustomAuthentication,)
    serializer_class = PurchaseOrderCreateListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PurchaseOrderCreateListSerializer
        return PurchaseOrderCreateListSerializer

    def post(self, request):
        serializer_class = self.serializer_class(data=request.data)
        if not serializer_class.is_valid():
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        response = PurchaseOrder().create(request)
        status_code = status.HTTP_201_CREATED if response else status.HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)

    def get_queryset(self):
        user, _ = self.request.user
        return PurchaseOrder.objects.filter(vendor=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PurchaseOrderReadUpdateDeleteView(GenericAPIView):
    serializer_class = PurchaseOrderUpdateSerializer

    def get(self, *args, **kwargs):
        code = status.HTTP_200_OK
        try:
            pur_order = PurchaseOrder.objects.get(pk=kwargs.get('purchase_order_id'))
            data = PurchaseOrderCreateListSerializer(pur_order).data
        except PurchaseOrder.DoesNotExist as e:
            data = {"message" : str(e)}
            code = status.HTTP_404_NOT_FOUND
        return Response(data, status=code)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        obj = PurchaseOrder.objects.filter(pk=kwargs.get('purchase_order_id')).first()
        for k,v in data.items():
            setattr(obj,k,v)
        obj.save()

        return Response({"message": "Updated Successfully"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        message = "Deleted Successfully"
        code = status.HTTP_204_NO_CONTENT
        try:
            PurchaseOrder.objects.get(pk=kwargs.get('purchase_order_id')).delete()
        except PurchaseOrder.DoesNotExist as e:
            message = str(e)
            code = status.HTTP_404_NOT_FOUND
        return Response({"message": message}, status=code)
