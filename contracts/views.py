from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contract
from .serializers import ContractSerializer
from .filters import ContractFilter
from rest_framework.exceptions import ValidationError

# View para criação de contrato
class ContractCreateView(generics.CreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Verifica se os dados são enviados como uma lista ou como um único contrato 
            # No Swagger isso buga, mas no postman/insominia funciona normalmente
            # Pra contornar no Swagger precisa adicionar o json do contrato unico dentro de uma lista.
            if isinstance(request.data, list):
                serializer = self.get_serializer(data=request.data, many=True)
            else:
                serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()


# View para Atualização de contrato
class ContractUpdateView(generics.UpdateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def perform_update(self, serializer):
        serializer.save()

# View para listar contratos com filtros
class ContractListView(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ContractFilter

# View para o resumo de todos os contratos 
class ContractListAllView(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

# View para o resumo dos contratos
class ContractSummaryView(APIView): 
    def get(self, request):
        filters = {}
        
        cpf = request.query_params.get('cpf', None)
        issue_date = request.query_params.get('issue_date', None)
        address_state = request.query_params.get('address_state', None)

        if cpf:
            filters['cpf'] = cpf
        if issue_date:
            # Verificando se issue_date é ano, mês/ano ou data completa
            try:
                filters['issue_date__year'] = int(issue_date)
            except ValueError:
                try:
                    # Se for mês/ano (mm/yyyy)
                    filters['issue_date__month'] = int(issue_date.split('/')[0])
                    filters['issue_date__year'] = int(issue_date.split('/')[1])
                except ValueError:
                    try:
                        # Se for data completa (dd/mm/yyyy)
                        filters['issue_date'] = issue_date
                    except ValueError:
                        pass
        if address_state:
            filters['address_state'] = address_state

        contracts = Contract.objects.filter(**filters)
        if not contracts.exists():
            return Response({"detail": "No contracts found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)
        
        total_value_to_receive = contracts.annotate(total_value=Sum('parcels__parcel_value')).aggregate(Sum('total_value'))['total_value__sum']
        total_disbursed = contracts.aggregate(Sum('loan_value'))['loan_value__sum']
        total_contracts = contracts.count()
        avg_rate = contracts.aggregate(Avg('contract_rate'))['contract_rate__avg']

        summary = {
            "total_value_to_receive": total_value_to_receive,
            "total_disbursed": total_disbursed,
            "total_contracts": total_contracts,
            "avg_rate": avg_rate
        }

        return Response(summary, status=status.HTTP_200_OK)  # Retorna status 200 OK
