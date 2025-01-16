from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Contract, Parcel
from  rich.console import Console

console = Console()

#Meu deus  esse framework de teste do django é bem completo,
#mas o pytest ainda é melhor.
class ContractAPITestCase(APITestCase):
    console.print("[bold red]Iniciando testes de contrato[/bold red]")
    def setUp(self):
        # Dados de contrato para teste
        self.contract_data = {
            "cpf": "40876005059",
            "birth_date": "1980-01-01",
            "issue_date": "2025-01-15",
            "loan_value": 10000.0,
            "address_country": "Brasil",
            "address_state": "SP",
            "address_city": "São Paulo",
            "phone_number": "11999999999",
            "contract_rate": 1.5,
            "parcels": [
                {"parcel_number": 1, "parcel_value": 2000.0, "due_date": "2025-02-15"},
                {"parcel_number": 2, "parcel_value": 2000.0, "due_date": "2025-03-15"},
                {"parcel_number": 3, "parcel_value": 2000.0, "due_date": "2025-04-15"}
            ]
        }

        # URL para criação de contrato
        self.create_url = reverse('contract-create')  
        
        # Criando o contrato de teste
        self.contract = Contract.objects.create(
            cpf="40876005059", 
            loan_value=10000.0, 
            contract_rate=1.5,
            birth_date="1980-01-01",
            issue_date="2025-01-15",
            address_country="Brasil",
            address_state="SP",
            address_city="São Paulo",
            phone_number="11999999999"
        )
        # Criando as parcelas
        Parcel.objects.bulk_create([
            Parcel(contract=self.contract, parcel_number=1, parcel_value=2000.0, due_date="2025-02-15"),
            Parcel(contract=self.contract, parcel_number=2, parcel_value=2000.0, due_date="2025-03-15"),
            Parcel(contract=self.contract, parcel_number=3, parcel_value=2000.0, due_date="2025-04-15"),
        ])

    def test_create_contract(self):
        # Testa a criação de um contrato com dados válidos
        response = self.client.post(self.create_url, self.contract_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        console.print("[bold green]Contrato criado com sucesso[/bold green]")
    def test_filter_by_contract_id(self):
        # Testa o filtro por ID de contrato
        url = reverse('contract-list') + "?id=" + str(self.contract.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        console.print("[bold green]Filtro por ID de contrato realizado com sucesso[/bold green]")

    def test_filter_by_cpf(self):
        # Testa o filtro por CPF
        url = reverse('contract-list') + "?cpf=" + self.contract.cpf
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        console.print("[bold green]Filtro por CPF realizado com sucesso[/bold green]")
    def test_filter_by_issue_date_year(self):
        # Testa o filtro por ano de emissão
        url = reverse('contract-list') + "?issue_date=2025"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        console.print("[bold green]Filtro por ano de emissão realizado com sucesso[/bold green]")
    def test_filter_by_issue_date_month_year(self):
        # Testa o filtro por mês/ano de emissão
        url = reverse('contract-list') + "?issue_date=2025-01"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        console.print("[bold green]Filtro por mês/ano de emissão realizado com sucesso[/bold green]")
    def test_filter_by_address_state(self):
        # Testa o filtro por estado de residência
        url = reverse('contract-list') + "?address_state=SP"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        console.print("[bold green]Filtro por estado de residência realizado com sucesso[/bold green]")
    def test_filter_multiple_filters(self):
        # Testa o uso de múltiplos filtros
        url = reverse('contract-list') + "?cpf=12345678901&issue_date=2025-01&address_state=SP"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        console.print("[bold green]Filtro múltiplo realizado com sucesso[/bold green]") 