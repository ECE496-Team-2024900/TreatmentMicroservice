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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TreatmentSessions(models.Model):
    notes = models.CharField(blank=True, null=True)
    wound = models.ForeignKey('Wounds', models.DO_NOTHING)
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
    image_urls = ArrayField(models.CharField(), default=list)

    class Meta:
        managed = False
        db_table = 'treatment_sessions'


class Wounds(models.Model):
    patient_id = models.IntegerField()
    clinician_id = models.IntegerField()
    device_id = models.CharField()
    treated = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'wounds'