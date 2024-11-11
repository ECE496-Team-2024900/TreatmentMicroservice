from django.http import JsonResponse

from treatmentserver.models import TreatmentSessions
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
