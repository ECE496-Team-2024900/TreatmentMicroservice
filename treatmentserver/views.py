from sys import exception
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import TreatmentSessions

def index(request):
    return JsonResponse({"message": "This is the treatment microservice"})

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
            "time": str(obj.start_time_scheduled)
        })
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)
