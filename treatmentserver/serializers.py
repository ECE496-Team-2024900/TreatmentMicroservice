from rest_framework import serializers
from base.models import TreatmentSession

class TreatmentSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentSession
        fields = '__all__'
