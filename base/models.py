from django.db import models

# Create your models here.

class TreatmentSession(models.Model):
    notes = models.CharField(max_length=65535)
    wound = models.ForeignKey('Wounds', models.DO_NOTHING)
    status_of_device = models.CharField(max_length=32)
    drug_volume_required = models.IntegerField()
    laser_power_required = models.IntegerField()
    wash_volume_required = models.IntegerField() 
    first_wait = models.IntegerField()
    second_wait = models.IntegerField()
    drug_volume_administered = models.IntegerField()
    wash_volume_administered = models.IntegerField()
    power_delivered_by_laser_1 = models.IntegerField()
    power_delivered_by_laser_2 = models.IntegerField()
    power_delivered_by_laser_3 = models.IntegerField()
    power_delivered_by_laser_4 = models.IntegerField()
    estimated_duration_for_drug_administration = models.IntegerField()
    estimated_duration_for_light_administration = models.IntegerField()
    estimated_duration_for_wash_administration = models.IntegerField()
    issues = models.CharField(max_length=65535)
    started = models.BooleanField()
    paused = models.BooleanField()
    completed = models.BooleanField()
    date_scheduled = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    handshake_random_string = models.CharField(max_length=10)
    handshake_counter = models.IntegerField()
    session_number = models.IntegerField()

    class Meta:
        db_table = 'treatment_sessions'

class Wounds(models.Model):
    patient_id = models.IntegerField()
    clinician_id = models.IntegerField()
    device_id = models.CharField()
    treated = models.BooleanField()

    class Meta:
        db_table = 'wounds'
