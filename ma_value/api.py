from django import get_version
from django.urls import path
from django.views.decorators.cache import cache_page

from apps.api.views import (
    models_by_brand, results_valuation, urls_generated,
    json_translate)


app_name = 'api'
urlpatterns = [
    path('results-valuation/', results_valuation),
    path('results-valuation/<str:job_id>/', results_valuation),
    path('urls-generated/<str:job_id>/', urls_generated),
    path('gfk/models/', models_by_brand),
    path('gfk/models/<str:job_id>/', models_by_brand),
    path('translate/<str:lang>/', json_translate)
]
