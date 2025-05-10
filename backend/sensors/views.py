# backend\sensors\views.py
from rest_framework import status, generics
from rest_framework.response import Response
from .models import SensorReading
from .serializers import SensorReadingSerializer
from .services import clean_and_flag, aggregate_stats
import pandas as pd

class IngestDataView(generics.CreateAPIView):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer

class ProcessedDataView(generics.GenericAPIView):
    def get_queryset(self):
        return SensorReading.objects.all()

    def get(self, request):
        qs = self.get_queryset().values()
        df = pd.DataFrame.from_records(qs)
        df_clean = clean_and_flag(df)
        return Response(df_clean.to_dict(orient='records'))


class AggregatedDataView(generics.GenericAPIView):
    def get(self, request):
        window = request.query_params.get('window', '1H')
        qs = SensorReading.objects.all().values()
        df = pd.DataFrame.from_records(qs)
        stats = aggregate_stats(df, window)
        return Response(stats)
