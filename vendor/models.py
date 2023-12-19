from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from uuid import uuid4
from django.db.models import Q


# method for updating




class UserManager(BaseUserManager):

    def create_user(self, **kwargs):
        password = kwargs.pop('password')
        user = self.model(**kwargs)
        user.set_password(password)
        user.save()
        return user


class Vendor(AbstractUser):
    contact_details = models.TextField(null=True)
    address = models.TextField(null=True)
    vendor_code = models.CharField(primary_key=True, unique=True, max_length=255, default=uuid4)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "vendors"

    def __str__(self):
        return self.username

    def create(self, request):
        try:
            data = request.data
            vendor = Vendor.objects.create_user(**data)
            return {"username": vendor.username, "vendor_id": vendor.vendor_code}
        except Exception as e:
            return {'error': str(e)}


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    on_time_delivery_rate = models.FloatField(default=0, max_length=100)
    quality_rating_avg = models.FloatField(default=0, max_length=100)
    average_response_time = models.FloatField(default=0, max_length=100)
    fulfillment_rate = models.FloatField(default=0, max_length=100)

