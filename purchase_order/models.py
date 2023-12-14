from django.db import models
from uuid import uuid4
from django.db.models import fields
import importlib
from vendor.models import HistoricalPerformance
from django.db.models import Q, F, Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import timedelta

STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("COMPLETED", "COMPLETED"),
    ("CANCELED", "CANCELED"),
)

Vendor = importlib.import_module('vendor.models').Vendor


class PurchaseOrder(models.Model):
    po_number = models.CharField(primary_key=True, max_length=255, default=uuid4)
    vendor = models.ForeignKey(Vendor, related_name="vendor_orders", on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True, null=True)
    delivery_date = models.DateTimeField(null=True)
    items = models.JSONField(null=True)
    quantity = models.IntegerField(null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(null=True)
    acknowledgment_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def time_difference(self):
        return models.ExpressionWrapper(
            models.F('acknowledgment_date') - models.F('issue_date'),
            output_field=fields.DurationField()
        )

    def create(self, request):
        data = dict(request.data)
        data['vendor'], _ = request.user
        purchase = PurchaseOrder.objects.create(**data)
        return {"message": "Created Successfully", "pk": purchase.pk}


@receiver(post_save, sender=PurchaseOrder)
def update_metrics(sender, instance, **kwargs):
    common_post_save_delete(instance)


@receiver(post_delete, sender=PurchaseOrder)
def update_metrics(sender, instance, **kwargs):
    common_post_save_delete(instance)


def common_post_save_delete(instance):
    if instance.vendor:
        v_perf, created = HistoricalPerformance.objects.get_or_create(vendor=instance.vendor)
        po_qs = PurchaseOrder.objects.filter(vendor=instance.vendor)
        if instance.status == 'COMPLETED':
            try:
                total = po_qs.count()

                # Find fulfilment rate
                completed = po_qs.filter(status='COMPLETED').count()
                v_perf.fulfillment_rate = round((completed / total) * 100, 2)

                # Find on time delivery rate
                before_del_date = po_qs.filter(issue_date__lte=F('delivery_date')).count()
                v_perf.on_time_delivery_rate = round((before_del_date / completed) * 100, 2)

                # Find average response time
                average = po_qs.annotate(diff=F('issue_date') - F('acknowledgment_date')).aggregate(avg=Avg('diff'))
                if average and isinstance(average.get('avg'), timedelta):
                    average = average.get('avg')
                    v_perf.average_response_time = average.total_seconds()
            except ZeroDivisionError as e:
                pass

        if instance.quality_rating:
            rating = po_qs.aggregate(average=Avg('quality_rating'))
            if rating.get('average'):
                v_perf.quality_rating_avg = rating.get('average')

        v_perf.save()
