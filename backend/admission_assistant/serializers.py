# backend/admission_assistant/serializers.py

from rest_framework import serializers
from .models import (
    Admission,
    Document,
    Payment,
    Guardian,
    EntryTest
)

class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class EntryTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryTest
        fields = '__all__'

class AdmissionSerializer(serializers.ModelSerializer):
    guardians = GuardianSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    entry_test = EntryTestSerializer(read_only=True)

    class Meta:
        model = Admission
        fields = '__all__'
        read_only_fields = ('admission_code', 'status', 'entry_test_unlocked')