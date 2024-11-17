from django.http import JsonResponse
import json
from rest_framework.decorators import api_view

from treatmentserver.models import TreatmentSessions
def index(request):
    return JsonResponse({"message": "This is the treatment microservice"})

def add_video_call_id(request):
    req = request.get_json()
    try:
        obj = TreatmentSessions.objects.get(id=req['id'])
        obj.video_call_id = req['video_call_id']
        obj.save()
        return JsonResponse({"message": "Video Call ID is updated"})
    except TreatmentSessions.DoesNotExist:
        return JsonResponse({"message": "Video Call ID not found"})

def get_video_call_id(request):
    req = request.get_json()
    try:
        obj = TreatmentSessions.objects.get(id=req['id'])
        return JsonResponse({"message": str(obj.video_call_id)})
    except TreatmentSessions.DoesNotExist:
        return JsonResponse({"message": "Video Call ID not found"})

def get_session_info(request):
    treatment_id = request.GET.get("id")
    try:
        obj = TreatmentSessions.objects.get(id=treatment_id)
        return JsonResponse({
            "session_number": str(obj.session_number),
            "date": str(obj.date_scheduled),
            "time": str(obj.start_time_scheduled),
            "completed": str(obj.completed)
        })
    except TreatmentSessions.DoesNotExist:
        return JsonResponse({"message": "Treatment session info not found"})

# Store updated parameters
# Expects a JSON body with key-value pairs that denote fields to update and the updated value
# Expects a treatment ID
@api_view(['POST'])
def set_pain_score_and_session_complete(request):
    treatment_id = request.GET.get('id', None)
    if treatment_id is None:
        return JsonResponse({'message':'Please provide a treatment ID'}, status=400)
    try:
        updated_fields = json.loads(request.body)
        TreatmentSessions.objects.filter(pk=treatment_id).update(**updated_fields)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)
    return JsonResponse({'message':'Updated fields successfully'}, status=200)