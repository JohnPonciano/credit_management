from django.urls import path
from .views import ContractCreateView, ContractListView, ContractSummaryView, ContractListAllView, ContractUpdateView

urlpatterns = [
    path('contracts/', ContractCreateView.as_view(), name='contract-create'),
    path('contracts/update/<int:pk>/', ContractUpdateView.as_view(), name='contract-update'),
    path('contracts/list/', ContractListView.as_view(), name='contract-list'),
    path('contracts/summary/', ContractSummaryView.as_view(), name='contract-summary'),
    path('contracts/listall/', ContractListAllView.as_view(), name='contract-list-all'),
]
