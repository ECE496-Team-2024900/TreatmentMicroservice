import uuid
import json
from django.core.serializers import serialize
from .models import TreatmentSessions, Wounds, Reports
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
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

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

@api_view(['POST'])
@csrf_exempt
def update_wound_status(request):
    """
    API to update the wound's 'treated' status.
    Expects a JSON body with 'wound_id' and 'treated' fields.
    """
    try:
        data = json.loads(request.body)
        wound_id = data.get("wound_id")
        treated = data.get("treated")

        if wound_id is None or treated is None:
            return JsonResponse({"error": "Missing wound_id or treated field"}, status=400)

        wound = Wounds.objects.filter(id=wound_id).first()
        if wound:
            wound.treated = treated
            wound.save()
            return JsonResponse({"message": "Wound status updated successfully"}, status=200)
        else:
            return JsonResponse({"error": "Wound not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

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

# Retrieves treatments meeting specified criteria ordered from most to least recent
# Expects a body that contains fields and their assignments to filter by
# If a body isn't provided, function will still work, but recommended to use the get_all_treatments method

# Response HTTP status values:
# - 200 = treatments returned
# - 204 = no error, but no treatments exist meeting this criteria
# - 500 = error encountered
@api_view(['POST'])
def get_treatments(request):
    try:
        filters = json.loads(request.body)

        # Adding filter if patient_id asked for, as this requires traversing the foreign key relationship
        if 'patient_id' in filters:
            patient_id = filters.pop('patient_id')
            filters['wound__patient_id'] = patient_id

        # Fetching treatments from DB
        sorted_patient_treatments = TreatmentSessions.objects.filter(**filters).order_by('-date_scheduled')

        if sorted_patient_treatments.exists():
            return JsonResponse(list(sorted_patient_treatments.values()), safe=False, status=200)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'No treatments found.'}, status=204)

@api_view(['GET'])
def get_treatment_parameters(request):
    treatment_id = request.GET.get('id', None)
    if treatment_id is None:
        return JsonResponse({'message':'Please provide a treatment ID'}, status=400)
    try:
        treatment = TreatmentSessions.objects.filter(pk=treatment_id).first()

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
        treatment_id = request.GET.get('id', None)
        obj = TreatmentSessions.objects.get(id=treatment_id)
        if (obj is not None and obj.video_call_id is not None):
            return JsonResponse({"message": str(obj.video_call_id)}, status=200)
        else:
            return JsonResponse({"message": "Video Call ID not found"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

@api_view(['PUT'])
def remove_video_call_id(request):
    try:
        treatment_id = request.GET.get('id', None)
        obj = TreatmentSessions.objects.get(id=treatment_id)
        if (obj is not None and obj.video_call_id is not None):
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

@api_view(['GET'])
def get_all_images_for_wound(request):
    try:
        obj = TreatmentSessions.objects.filter(wound=request.GET.get('wound')).values("id","image_urls")
        if (obj is not None):
            return JsonResponse({"message": list(obj)}, status=200)
        else:
            return JsonResponse({"message": "No images exist"}, status=404)
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


@api_view(['GET'])
def get_wound(request):
    wound_id = request.GET.get('id', None)
    if wound_id is None:
        return JsonResponse({'message':'Please provide a wound ID'}, status=400)
    try:
        wound = Wounds.objects.filter(pk=wound_id).first()
        if wound is None:
            return JsonResponse({'message': 'No wound found for the given ID.'}, status=404)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)
    return JsonResponse({'message': model_to_dict(wound)}, status=200)

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

# Retrieves wounds meeting specified criteria
# Expects a body that contains fields and their assignments to filter by
# If a body isn't provided, function will still work, but recommended to use the get_all_wounds method
@api_view(['POST'])
# Response HTTP status values:
# - 200 = wounds returned
# - 204 = no error, but no wounds exist meeting this criteria
# - 500 = error encountered
def get_wounds(request):
    try:
        filters = json.loads(request.body)

        # Fetching wounds from DB
        wounds = Wounds.objects.filter(**filters)
        if wounds.exists():
            return JsonResponse(list(wounds.values()), safe=False, status=200)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    return JsonResponse({'message': 'No wounds found.'}, status=204)

# Get wound information for a wound ID
# Expects a wound ID query parameter
# Returns all information for that wound
@api_view(['GET'])
def get_wound_info(request):
    try:
        # Retrieve wound ID from query parameters
        wound_id = request.GET.get("id")

        # Find wound based on ID
        obj = Wounds.objects.get(id=wound_id)

        # Return wound information, if it exists
        if (obj is not None):
            return JsonResponse({"message": model_to_dict(obj)}, status=200)
        else:
            return JsonResponse({"message": "No wound information found"}, status=404)
    except Exception as e:
        # Internal server error handling
        return JsonResponse({"message": str(e)}, status=500)
  
@api_view(['GET'])
def get_session_info(request):
    # Get the treatment id parameter passed in
    treatment_id = request.GET.get("id")
    try:
        # Filter by id to find the required treatment session record
        obj = TreatmentSessions.objects.get(id=treatment_id)

        # No record found with the specified id
        if obj is None:
            return JsonResponse({"message": "Treatment session id not found"}, status=400)
        
        # Return a json with the following fields and their values
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
# Returns a success or error message
@api_view(['PUT'])
def set_pain_score_and_session_complete(request):
    # Get the treatment id parameter passed in
    treatment_id = request.GET.get('id', None)

    # No treatment id provided - cannot update any record
    if treatment_id is None:
        return JsonResponse({'message':'Please provide a treatment ID'}, status=400)
    try:
        # Filter by the treatment id to find the required treatment session record 
        # and update it using the new field values that were passed in as the request body
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

        # Get the relevant timer values, defaulting to 5 minutes (15 seconds) if they are None
        drug_timer = treatment_session.estimated_duration_for_drug_administration or 15
        light_timer = treatment_session.estimated_duration_for_light_administration or 15
        wash_timer = treatment_session.estimated_duration_for_wash_administration or 15

        # Return the timers as a JSON response
        return JsonResponse({
            "drug_timer": drug_timer,
            "light_timer": light_timer,
            "wash_timer": wash_timer
        }, status=200)

    except TreatmentSessions.DoesNotExist:
        return JsonResponse({"message": "Treatment session not found"}, status=404)

@api_view(["PUT"])
def add_report(request):
    try:
        # Fetch query parameter
        treatment_id = request.GET.get('id')

        # Check to ensure this treatment exists
        treatment = get_object_or_404(TreatmentSessions, id=treatment_id)
        
        # Parse the request body to get the report data
        report_data = json.loads(request.body)["fileData"]

        # Create the new report in the DB
        report = Reports.objects.create(treatment_id=treatment_id, report_data=report_data)
        return JsonResponse({"message": "Report added successfully"}, status=201)

    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)

@api_view(['POST'])
def add_treatment(request):
    try:
        req = json.loads(request.body.decode('utf-8'))
        TreatmentSessions.objects.create(**req)
        return JsonResponse({"message": "Treatment added successfully"}, status=201)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)

@api_view(['PUT'])
def request_reschedule(request):
    try:
        treatment_id = request.GET.get('id')
        req = json.loads(request.body.decode('utf-8'))
        obj = TreatmentSessions.objects.get(id=treatment_id)
        if (obj is not None):
            obj.reschedule_requested = req['reschedule_requested']
            obj.save()
            return JsonResponse({"message": "Treatment session modified successfully"}, status=200)
        else:
            return JsonResponse({"message": "Treatment session not found"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

@api_view(['DELETE'])
def cancel_treatment(request):
    try:
        treatment_id = request.GET.get('id', None)
        TreatmentSessions.objects.get(id=treatment_id).delete()
        return JsonResponse({"message": "Treatment session deleted"}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)


# Retrieve the report for a specific treatment session
@api_view(["GET"])
def get_report(request):
    try:
        # Fetch query parameter
        treatment_id = request.GET.get('id')

        # Fetch the report object
        report = Reports.objects.get(treatment_id=treatment_id)

        return JsonResponse(model_to_dict(report), status=200)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)

# Retrieves wounds meeting specified criteria
# Expects a body that contains fields and their assignments to filter by
# If a body isn't provided, function will still work, but recommended to use the get_all_wounds method
@api_view(['POST'])
# Response HTTP status values:
# - 200 = wounds returned
# - 204 = no error, but no wounds exist meeting this criteria
# - 500 = error encountered
def get_wounds(request):
    try:
        filters = json.loads(request.body)

        # Fetching wounds from DB
        wounds = Wounds.objects.filter(**filters)
        if wounds.exists():
            return JsonResponse(list(wounds.values()), safe=False, status=200)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    return JsonResponse({'message': 'No wounds found.'}, status=204)
    
# Creates a new wound record in database
# Expects a JSON body with key-value pairs that denote the fields and their values
# Fields/keys required in JSON: infection_type, infection_location, device_id, patient_id, clinician_id, treated, date_added
# Returns a success or error message
@api_view(['PUT'])
def create_wound(request):
    try:
        body = json.loads(request.body)
        
        # Extract fields
        required_fields = ["infection_type", "infection_location", "device_id", "patient_id", "clinician_id", "treated", "date_added"]
        missing_fields = [field for field in required_fields if field not in body]
        
        if missing_fields:
            return JsonResponse({"message": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

        # Create and save the wound record
        new_wound = Wounds(
            infection_type=body['infection_type'],
            infection_location=body['infection_location'],
            device_id=body['device_id'],
            patient_id=body['patient_id'],
            clinician_id=body['clinician_id'],
            treated=body['treated'],
            date_added=body['date_added']
        )
        new_wound.save()

        return JsonResponse({"message": "Wound record created successfully"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON body"}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)
