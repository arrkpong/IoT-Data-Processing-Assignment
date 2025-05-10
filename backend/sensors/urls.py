# backend\sensors\urls.py
from django.urls import path
from sensors.views import IngestDataView, ProcessedDataView , AggregatedDataView

urlpatterns = [
    path('api/sensors/data/', IngestDataView.as_view(), name='ingest'),
    path('api/sensors/processed/', ProcessedDataView.as_view(), name='processed'),
    path('api/sensors/aggregated/', AggregatedDataView.as_view(), name='aggregated'),
]