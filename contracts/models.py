from django.db import models

class Contract(models.Model):
    cpf = models.CharField(max_length=11)
    birth_date = models.DateField()
    issue_date = models.DateField()
    loan_value = models.DecimalField(max_digits=10, decimal_places=2)
    address_country = models.CharField(max_length=100)
    address_state = models.CharField(max_length=100)
    address_city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    contract_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Contract {self.id} - {self.cpf}"

class Parcel(models.Model):
    contract = models.ForeignKey(Contract, related_name='parcels', on_delete=models.CASCADE)
    parcel_number = models.IntegerField()
    parcel_value = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

    def __str__(self):
        return f"Parcel {self.parcel_number} - Contract {self.contract.id}"
