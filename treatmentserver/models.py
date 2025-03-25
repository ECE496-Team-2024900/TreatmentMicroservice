# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class Wounds(models.Model):
    patient_id = models.IntegerField()
    clinician_id = models.CharField()
    device_id = models.CharField()
    treated = models.BooleanField()
    date_added = models.DateField(blank=True, null=True)
    infection_type = models.CharField(blank=True, null=True)
    infection_location = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wounds'

class TreatmentSessions(models.Model):
    notes = models.CharField(blank=True, null=True)
    wound = models.ForeignKey(Wounds, models.DO_NOTHING)
    status_of_device = models.CharField(blank=True, null=True)
    drug_volume_required = models.FloatField(blank=True, null=True)
    laser_power_required = models.FloatField(blank=True, null=True)
    wash_volume_required = models.FloatField(blank=True, null=True)
    first_wait = models.FloatField(blank=True, null=True)
    second_wait = models.FloatField(blank=True, null=True)
    drug_volume_administered = models.FloatField(blank=True, null=True)
    wash_volume_administered = models.FloatField(blank=True, null=True)
    power_delivered_by_laser_1 = models.FloatField(blank=True, null=True)
    power_delivered_by_laser_2 = models.FloatField(blank=True, null=True)
    power_delivered_by_laser_3 = models.FloatField(blank=True, null=True)
    power_delivered_by_laser_4 = models.FloatField(blank=True, null=True)
    estimated_duration_for_drug_administration = models.FloatField(blank=True, null=True)
    estimated_duration_for_light_administration = models.FloatField(blank=True, null=True)
    estimated_duration_for_wash_administration = models.FloatField(blank=True, null=True)
    issues = models.TextField(blank=True, null=True)  # This field type is a guess.
    started = models.BooleanField()
    paused = models.BooleanField()
    completed = models.BooleanField()
    date_scheduled = models.DateField(blank=True, null=True)
    start_time_scheduled = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    handshake_random_string = models.CharField(blank=True, null=True)
    handshake_counter = models.IntegerField(blank=True, null=True)
    video_call_id = models.CharField(blank=True, null=True)
    session_number = models.IntegerField()
    pain_score = models.IntegerField(blank=True, null=True)
    image_urls = ArrayField(models.CharField(), default=list)
    reschedule_requested = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'treatment_sessions'

class Reports(models.Model):
    treatment = models.ForeignKey('TreatmentSessions', on_delete=models.DO_NOTHING)
    report_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'reports'
