from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import TreatmentSessions
def index(request):
    return JsonResponse({"message": "This is the treatment microservice"})

@api_view(['PUT'])
def add_video_call_id(request):
    req = request.get_json()
    try:
        obj = TreatmentSessions.objects.get(id=req['id'])
        obj.video_call_id = req['video_call_id']
        obj.save()
        return JsonResponse({"message": "Video Call ID is updated"}, status=200)
    except TreatmentSessions.DoesNotExist:
        return JsonResponse({"message": "Video Call ID not found"}, status=404)

@api_view(['GET'])
def get_video_call_id():
    try:
        obj = TreatmentSessions.objects.filter(video_call_id__isnull=False).first()
        return JsonResponse({"message": str(obj.video_call_id)}, status=200)
    except TreatmentSessions.DoesNotExist:
        return JsonResponse({"message": "Video Call ID not found"}, status=404)

@api_view(['GET'])
def get_treatment_timer(request, treatment_id):
    try:
        # Fetch the treatment session using the provided treatment ID
        treatment_session = TreatmentSessions.objects.get(id=treatment_id)

        # Get the relevant timer values, defaulting to 5 minutes (300 seconds) if they are None
        drug_timer = treatment_session.estimated_duration_for_drug_administration or 5 * 60  # 5 minutes (in seconds)
        light_timer = treatment_session.estimated_duration_for_light_administration or 5 * 60  # 5 minutes (in seconds)
        wash_timer = treatment_session.estimated_duration_for_wash_administration or 5 * 60  # 5 minutes (in seconds)

        # Return the timers as a JSON response
        return JsonResponse({
            "drug_timer": drug_timer,
            "light_timer": light_timer,
            "wash_timer": wash_timer
        }, status=200)

    except TreatmentSessions.DoesNotExist:
        return JsonResponse({"message": "Treatment session not found"}, status=404)