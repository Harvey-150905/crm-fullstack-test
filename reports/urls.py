from django.urls import path
from .views import sales_report

urlpatterns = [
    path('reports/sales/', sales_report),
]