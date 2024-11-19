import uuid
import json
from django.http import JsonResponse
import base64

from rest_framework.decorators import api_view

from . import settings
from .models import TreatmentSessions
from django.core.files.base import ContentFile

import boto3

s3 = boto3.client(
   "s3",
   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

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
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)
