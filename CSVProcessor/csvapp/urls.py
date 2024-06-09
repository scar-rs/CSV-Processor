from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='upload_csv')),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('data-processing-options/', views.data_processing_options, name='data_processing_options'),
]
