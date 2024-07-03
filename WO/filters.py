import django_filters
from django_filters import FilterSet, CharFilter, BooleanFilter, DateFromToRangeFilter
from django.db.models import Q
from django.db.models.expressions import RawSQL

from .models import *


class PatientFilter(FilterSet):
    fuzzy_query = CharFilter(method='custom_search')

    class Meta:
        model = Patient
        fields = ['cat_id', 'patient_name', 'record_number']

    def custom_search(self, queryset, name, value):
        # 解密病人姓名
        decrypted_patient_name = RawSQL("public.decrypt_info(decode(substring(patient_name from 3), 'hex'))", ())
        return queryset.annotate(decrypted_patient_name=decrypted_patient_name).filter(
            Q(cat_id__exact=value) |
            Q(decrypted_patient_name__exact=value) |
            Q(record_number__exact=value)
        )


class WorkOrderFilter(FilterSet):
    date = CharFilter(method='filter_by_date')
    location = CharFilter(method='filter_by_location')

    class Meta:
        model = Qrcode
        fields = ['date', 'location']

    def filter_by_date(self, queryset, name, value):
        return queryset.filter(qrcode__date=value)

    def filter_by_location(self, queryset, name, value):
        return queryset.filter(qrcode__location=value)


class ReceiveTimeFilter(FilterSet):
    receive_time_null = BooleanFilter(method='filter_by_receive_time_null')

    class Meta:
        model = WorkOrder
        fields = ['receive_time']

    def filter_by_receive_time_null(self, queryset, name, value):
        if value:
            return queryset.filter(receive_time__isnull=True)
        else:
            return queryset
    

class QuerySampleBarcodeFilter(FilterSet):
    extract = DateFromToRangeFilter()

    class Meta:
        model = SampleBarcode
        fields = ['extract']