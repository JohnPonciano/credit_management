from rest_framework import serializers
from .models import Contract, Parcel

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ['parcel_number', 'parcel_value', 'due_date']

class ContractSerializer(serializers.ModelSerializer):
    parcels = ParcelSerializer(many=True)

    class Meta:
        model = Contract
        #Pra que serve o contract_rate? 
        fields = ['id', 'cpf', 'birth_date', 'issue_date', 'loan_value', 'address_country', 
                  'address_state', 'address_city', 'phone_number', 'contract_rate', 'parcels']
    

    #Cria os Contratos
    def create(self, validated_data):
        parcels_data = validated_data.pop('parcels')
        contract = Contract.objects.create(**validated_data)
        
        Parcel.objects.bulk_create([Parcel(contract=contract, **parcel_data) for parcel_data in parcels_data])
        
        return contract

    def update(self, instance, validated_data):        
        # Atualiza os contrato
        parcels_data = validated_data.pop('parcels',None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Atualiza as parcelas, se fornecidas
        if parcels_data is not None:
            instance.parcels.all().delete()
            Parcel.objects.bulk_create([
                Parcel(contract=instance, **parcel_data) for parcel_data in parcels_data
                ])
        return instance