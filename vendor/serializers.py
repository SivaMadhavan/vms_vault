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
        fields = ('first_name','last_name','username','password')

    def validate(self, attrs):
        return attrs


class VendorPerformanceSerializer(serializers.ModelSerializer):
    average_response_time = serializers.SerializerMethodField()

    class Meta:
        model = HistoricalPerformance
        fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')

    def get_average_response_time(self, instance):
        seconds = instance.average_response_time
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        duration_string = "{:02} Hrs {:02} Mins {:02} Secs".format(int(hours), int(minutes), int(seconds))
        if days > 0:
            duration_string = "{} days, {}".format(int(days), duration_string)

        return duration_string

