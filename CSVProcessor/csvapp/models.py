from django.db import models

class CSVFileData(models.Model):
    csv_file = models.FileField(upload_to='csv_files/')
    csv_data = models.JSONField(null=True,blank=True)
    class Meta:
        app_label = 'csvapp'
        verbose_name = 'CSV File Data'
        verbose_name_plural = 'CSV File Data'

    def __str__(self):
        return f"CSV File Data: {self.pk}"

class ProcessedResults(models.Model):
    column_name = models.CharField(max_length=255)  # Name of the CSV column
    mean_value = models.FloatField(null=True, blank=True)
    median_value = models.FloatField(null=True, blank=True)
    std_value = models.FloatField(null=True, blank=True) 
    class Meta:
        verbose_name = 'Processed Results'
        verbose_name_plural = 'Processed Results'

    def __str__(self):
        return f"Processed Results: Column - {self.column_name}"
       

