from django.http import JsonResponse

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
            "time": str(obj.start_time_scheduled)
        })
    except TreatmentSessions.DoesNotExist:
        return JsonResponse({"message": "Treatment session info not found"})
