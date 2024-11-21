from django.http import JsonResponse

from django.shortcuts import render
from rest_framework.decorators import api_view
from base.models import TreatmentSession, Wounds
import json
from datetime import datetime
from django.forms.models import model_to_dict

def index(request):
    return JsonResponse({"message": "This is the treatment microservice"})

# Store updated parameters
# Expects a JSON body with key-value pairs that denote fields to update and the updated value
# Expects a treatment ID
@api_view(['PUT'])
def set_treatment_parameters(request):
    treatment_id = request.GET.get('id', None)
    if treatment_id is None:
        return JsonResponse({'message':'Please provide a treatment ID'}, status=400)
    try:
        updated_parameters = json.loads(request.body)
        TreatmentSession.objects.filter(pk=treatment_id).update(**updated_parameters)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)
    return JsonResponse({'message':'Requested changes were successfully made'}, status=200)

# Retrieves a patient's most recent treatment before a given day
# Expects a patient ID and treatment date to look before
@api_view(['GET'])
def get_prev_treatment(request):
    patient_id = request.GET.get('id', None)
    treatment_date = request.GET.get('date', None)
    if (patient_id is None) or (treatment_date is None):
        return JsonResponse({'message':'Please provide a patient ID and current session number'}, status=400)
    try:
        treatment_date = datetime.strptime(treatment_date, '%Y-%m-%d').date()
        sorted_prev_treatments = TreatmentSession.objects.filter(
                                    wound__patient_id=patient_id,
                                    date_scheduled__lt=treatment_date
                                ).order_by('-date_scheduled')
        prev_treatment = sorted_prev_treatments.first()

        if prev_treatment is None:
            return JsonResponse({'message': 'No previous treatment found for the given patient and date.'}, status=204)

    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)
    return JsonResponse(model_to_dict(prev_treatment), status=200)