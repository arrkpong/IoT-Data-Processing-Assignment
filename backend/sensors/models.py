from django.db import models

class SensorReading(models.Model):
    timestamp = models.DateTimeField(verbose_name="เวลาที่วัด")
    temperature = models.FloatField(verbose_name="อุณหภูมิ (°C)")
    humidity = models.FloatField(verbose_name="ความชื้น (%)")
    air_quality = models.FloatField(verbose_name="คุณภาพอากาศ")

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
        ]
        verbose_name = "ข้อมูลเซนเซอร์"
        verbose_name_plural = "ข้อมูลเซนเซอร์ทั้งหมด"
