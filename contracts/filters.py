# contracts/filters.py
import django_filters
from .models import Contract

class ContractFilter(django_filters.FilterSet):
    cpf = django_filters.CharFilter(field_name="cpf", lookup_expr='exact')
    issue_date = django_filters.DateFromToRangeFilter(field_name="issue_date")
    address_state = django_filters.CharFilter(field_name="address_state", lookup_expr='exact')

    class Meta:
        model = Contract
        fields = ['id','cpf', 'issue_date', 'address_state']
