import uuid
import json
from django.core.serializers import serialize
from .models import TreatmentSessions, Wounds
from sys import exception
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
import base64
from . import settings
from django.core.files.base import ContentFile
from datetime import datetime
from django.forms.models import model_to_dict
import boto3

s3 = boto3.client(
   "s3",
   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

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
    try:
        req = json.loads(request.body.decode('utf-8'))
        obj = TreatmentSessions.objects.get(id=req['id'])
        if (obj is not None):
            obj.video_call_id = None
            obj.save()
            return JsonResponse({"message": "Video Call ID is updated"}, status=200)
        else:
            return JsonResponse({"message": "Video Call ID not found"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

@api_view(['GET'])
def get_all_treatments(request):
    try:
        obj = TreatmentSessions.objects.all()
        if (obj is not None):
            return JsonResponse({"message": list(obj.values())}, status=200)
        else:
            return JsonResponse({"message": "No treatment sessions exist"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

@api_view(['PUT'])
def add_images(request):
    try:
        req = json.loads(request.body.decode('utf-8'))
        image_64_decode = base64.urlsafe_b64decode(req["image"])
        image_id = uuid.uuid4()
        image_name = 'image-{id}.jpg'.format(id=image_id)
        image_result = ContentFile(image_64_decode, image_name)
        s3.upload_fileobj(image_result, settings.AWS_STORAGE_BUCKET_NAME, image_name)
        obj = TreatmentSessions.objects.get(id=req["id"])
        if (obj is not None):
            if (obj.image_urls is None):
                obj.image_urls = []
            obj.image_urls.append(f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{image_name}")
            obj.save()
            return JsonResponse({"message": "Image saved successfully"}, status=200)
        else:
            return JsonResponse({"message": "Image could not be saved"}, status=404)


@api_view(['GET'])
def get_all_wounds(request):
    try:
        obj = Wounds.objects.all()
        if (obj is not None):
            return JsonResponse({"message": list(obj.values())}, status=200)
        else:
            return JsonResponse({"message": "No treatment sessions exist"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

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