import django_filters

from django_filters import CharFilter
from .models import *

class business_search_filter(django_filters.FilterSet):
    store_name = CharFilter(field_name='store_name', lookup_expr='icontains')
    class Meta:
        model = Business
        fields = ['store_name']