from rest_framework import serializers
from meter_app import models
class serializers_meter(serializers.ModelSerializer):
    class Meta:
        fields={
            'id',
            'title',
            'description'
        }
        model=models.meter
        fields="__all__"