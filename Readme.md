
# Documentação do Sistema de Gestão de Contratos

## Visão Geral
Este sistema permite a gestão de contratos financeiros, incluindo a criação, atualização, listagem e filtragem de contratos. Além disso, é possível calcular resumos financeiros, como valor total a receber, valor total desembolsado, número total de contratos e taxa média.

---

## Endpoints da API
### 0. **Swagger**
**URL:** `http://localhost:8000/`

**Método:** `GET`

**Descrição:** Interface mais comoda para fazer testes da API.

### 1. **Criação de Contrato**
**URL:** `api/contracts/create/`  
**Método:** `POST`  
**Descrição:** Cria um novo contrato, aceitando um único contrato ou múltiplos contratos.

#### Exemplo de Request:
**Para um único contrato:**
```json
{
  "cpf": "74291696000",
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
```

**Para múltiplos contratos:**
```json
[
  {
    "cpf": "74291696000",
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
]
```

---
### 2. **Atualização de Contrato**
**URL:** `api/contracts/update/<id>/`  
**Método:** `PUT`  
**Descrição:** Atualiza os dados de um contrato existente.

#### Exemplo de Requests:
## Para Atualizar Apenas Campos do Contrato:
```json
{
  "address_city": "Sorocaba",
  "contract_rate": 2.0
}

```
## Para Atualizar Contrato e Parcelas:
```json
{
  "cpf": "98765432100",
  "birth_date": "1990-05-20",
  "issue_date": "2025-01-17",
  "loan_value": 20000,
  "address_country": "Brasil",
  "address_state": "SP",
  "address_city": "Campinas",
  "phone_number": "11987654321",
  "contract_rate": 1.8,
  "parcels": [
    {
      "parcel_number": 1,
      "parcel_value": 5000,
      "due_date": "2025-02-01"
    },
    {
      "parcel_number": 2,
      "parcel_value": 5000,
      "due_date": "2025-03-01"
    },
    {
      "parcel_number": 3,
      "parcel_value": 5000,
      "due_date": "2025-04-01"
    }
  ]
}

```

---

### 3. **Listagem de Contratos**
**URL:** `api/contracts/list/`  
**Método:** `GET`  
**Descrição:** Lista todos os contratos existentes. Suporta filtros.

#### Filtros Disponíveis:
- `cpf`: Filtra pelo CPF do cliente.
- `issue_date`: Filtra pelo ano, mês/ano ou data completa de emissão.
- `address_state`: Filtra pelo estado de residência.

#### Exemplo de Request:
**Filtro por CPF:**
```
api/contracts/list/?cpf=74291696000
```

**Filtro por ano de emissão:**
```
api/contracts/list/?issue_date=2025
```

**Filtro com multiplos filtros**
```
api/contracts/list/?cpf=12345678901&issue_date__year=2025&address_state=SP
```

---

### 4. **Resumo dos Contratos**
**URL:** `api/contracts/summary/`  
**Método:** `GET`  
**Descrição:** Retorna um resumo financeiro dos contratos.

#### Exemplo de Resumo:
```json
{
  "total_value_to_receive": 6000.0,
  "total_disbursed": 10000.0,
  "total_contracts": 1,
  "avg_rate": 1.5
}
```

### 4. **Lista todos os contratos e suas parcelas**
**URL:** `api/contracts/listall/`  
**Método:** `GET`  
**Descrição:** Retorna todos os contratos e suas parcelas, para facilitar vizualização dos contratos criados e editados. 

#### Exemplo de Resumo:
```json
[
  {
    "id": 1,
    "cpf": "98765432100",
    "birth_date": "2025-01-15",
    "issue_date": "2025-01-15",
    "loan_value": "99999.00",
    "address_country": "Brazil",
    "address_state": "SP",
    "address_city": "Itu",
    "phone_number": "11900362875",
    "contract_rate": "1.00",
    "parcels": [
      {
        "parcel_number": 123456789,
        "parcel_value": "1.00",
        "due_date": "2025-01-15"
      }
    ]
  },
  {
    "id": 2,
    "cpf": "12345678901",
    "birth_date": "1990-05-10",
    "issue_date": "2025-01-15",
    "loan_value": "10000.00",
    "address_country": "Brasil",
    "address_state": "SP",
    "address_city": "São Paulo",
    "phone_number": "11999999999",
    "contract_rate": "1.50",
    "parcels": [
      {
        "parcel_number": 1,
        "parcel_value": "2000.00",
        "due_date": "2025-02-15"
      },
      {
        "parcel_number": 2,
        "parcel_value": "2000.00",
        "due_date": "2025-03-15"
      }
    ]
  },
]
```
---

## Testes

### Testes Implementados
Os testes cobrem as seguintes funcionalidades:
1. **Criação de contratos válidos.**
2. **Filtragem de contratos por CPF, data de emissão e estado.**
3. **Resumo financeiro dos contratos.**
4. **Validação da existência de contratos após criação.**

### Exemplo de Saída de Testes
```bash
python manage.py test

Ran 7 tests in 0.053s

OK
```

---

## Configurações
### Dependências
- Django
- Django REST Framework
- django-filter

### Instalação
1. Clone o repositório.
2. Instale as dependências com `pip install -r requirements.txt`.
3. Configure o banco de dados no arquivo `settings.py` se quiser,
     mas já subi um arquivo chamado `credit_management_db.db` que é banco sqlite com alguns cadastros já feitos para facilitar review do codigo.
4. Execute as migrações: `python manage.py migrate`.
5. Inicie o servidor: `python manage.py runserver`.