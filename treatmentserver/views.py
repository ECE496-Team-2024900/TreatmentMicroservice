from django.http import JsonResponse

from django.shortcuts import render
from rest_framework.response import JsonResponse
from rest_framework.decorators import api_view
from base.models import TreatmentSession
from .serializers import TreatmentSessionSerializer
import json

def index(request):
    return JsonResponse({"message": "This is the treatment microservice"})

# Store updated parameters
# Expects a JSON body with key-value pairs that denote fields to update and the updated value
# Expects a treatment ID
@api_view(['POST'])
def set_treatment_parameters(request):
    treatment_id = request.POST['id']
    if treatment_id is None:
        return JsonResponse({'message':'Please provide a treatment ID'}, status=400)
    try:
        updated_parameters = json.loads(requests.body)
        TreatmentSession.objects.filter(pk=treatment_id).update(**updated_parameters)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)
    return JsonResponse({'message':'Requested changes were successfully made'}, status=200)