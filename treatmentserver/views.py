from sys import exception
import json
from django.http import JsonResponse
from django.shortcuts import render
import json
from rest_framework.decorators import api_view
from .models import TreatmentSessions, Wounds
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
        TreatmentSessions.objects.filter(pk=treatment_id).update(**updated_parameters)
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
        return JsonResponse({'message':'Please provide a patient ID and date.'}, status=400)
    try:
        treatment_date = datetime.strptime(treatment_date, '%Y-%m-%d').date()
        sorted_prev_treatments = TreatmentSessions.objects.filter(
                                    wound__patient_id=patient_id,
                                    date_scheduled__lt=treatment_date
                                ).order_by('-date_scheduled')
        prev_treatment = sorted_prev_treatments.first()

        if prev_treatment is None:
            return JsonResponse({'message': 'No previous treatment found for the given patient and date.'}, status=204)

    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)
    return JsonResponse(model_to_dict(prev_treatment), status=200)

# Retrieves a patient's most recent treatment before a given day
# Expects a patient ID and treatment date to look before
@api_view(['GET'])
def get_treatment_parameters(request):
    treatment_id = request.GET.get('id', None)
    if treatment_id is None:
        return JsonResponse({'message':'Please provide a treatment ID'}, status=400)
    try:
        treatment_date = datetime.strptime(treatment_date, '%Y-%m-%d').date()
        treatment = TreatmentSessions.objects.filter(pk=treatment_id)

        if treatment is None:
            return JsonResponse({'message': 'No treatment found for the given ID.'}, status=204)

    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)
    return JsonResponse(model_to_dict(treatment), status=200)

@api_view(['PUT'])
def add_video_call_id(request):
    req = json.loads(request.body.decode('utf-8'))
    try:
        obj = TreatmentSessions.objects.get(id=req['id'])
        if (obj is not None):
            obj.video_call_id = req['video_call_id']
            obj.save()
            return JsonResponse({"message": "Video Call ID is updated"}, status=200)
        else:
            return JsonResponse({"message": "Video Call ID not found"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

@api_view(['GET'])
def get_video_call_id(request):
    try:
        obj = TreatmentSessions.objects.exclude(video_call_id__isnull=True).first()
        if (obj is not None):
            return JsonResponse({"message": str(obj.video_call_id)}, status=200)
        else:
            return JsonResponse({"message": "Video Call ID not found"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

@api_view(['PUT'])
def remove_video_call_id(request):
    req = json.loads(request.body.decode('utf-8'))
    try:
        obj = TreatmentSessions.objects.get(id=req['id'])
        if (obj is not None):
            obj.video_call_id = None
            obj.save()
            return JsonResponse({"message": "Video Call ID is updated"}, status=200)
        else:
            return JsonResponse({"message": "Video Call ID not found"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)
        return JsonResponse({"message": str(obj.video_call_id)})
    except TreatmentSessions.DoesNotExist:
        return JsonResponse({"message": "Video Call ID not found"})

@api_view(['GET'])
def get_session_info(request):
    treatment_id = request.GET.get("id")
    try:
        obj = TreatmentSessions.objects.get(id=treatment_id)
        if obj is None:
            return JsonResponse({"message": "Treatment session id not found"}, status=400)
        
        return JsonResponse({
            "session_number": str(obj.session_number),
            "date": str(obj.date_scheduled),
            "time": str(obj.start_time_scheduled),
            "completed": str(obj.completed)
        })
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)

# Store updated parameters
# Expects a JSON body with key-value pairs that denote fields to update and the updated value
# Expects a treatment ID
@api_view(['PUT'])
def set_pain_score_and_session_complete(request):
    treatment_id = request.GET.get('id', None)
    if treatment_id is None:
        return JsonResponse({'message':'Please provide a treatment ID'}, status=400)
    try:
        updated_fields = json.loads(request.body)
        TreatmentSessions.objects.filter(pk=treatment_id).update(**updated_fields)
        return JsonResponse({'message':'Updated fields successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)