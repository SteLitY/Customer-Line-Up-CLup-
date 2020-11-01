import django_filters

from .models import *

class business_search_filter(django_filters.FilterSet):
    class Meta:
        model = Business
        fields = '__all__'