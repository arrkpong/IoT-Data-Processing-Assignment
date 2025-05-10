# backend\sensors\serializers.py
from rest_framework import serializers
from sensors.models import SensorReading

class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = '__all__'
