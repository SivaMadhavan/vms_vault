from .models import Vendor
from django.forms.models import model_to_dict
from rest_framework import serializers
from .models import HistoricalPerformance


class VendorCreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class VendorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"

    def validate(self, attrs):
        return attrs


class VendorPerformanceSerializer(serializers.ModelSerializer):
    average_response_time = serializers.SerializerMethodField()

    class Meta:
        model = HistoricalPerformance
        fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')

    def get_average_response_time(self, instance):
        if instance is not None and hasattr(instance, 'average_response_time'):
            seconds = instance.average_response_time

            # Calculate days, hours, minutes, and seconds
            days, seconds = divmod(seconds, 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)

            # Format the duration string
            duration_parts = []
            if days > 0:
                duration_parts.append(f"{int(days)} days")
            duration_parts.append("{:02} Hrs".format(int(hours)))
            duration_parts.append("{:02} Mins".format(int(minutes)))
            duration_parts.append("{:02} Secs".format(int(seconds)))

            return ', '.join(duration_parts)
        return None
