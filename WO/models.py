# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class CaUser(models.Model):
    username = models.CharField(primary_key=True, max_length=150)
    password = models.CharField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    getpasstime = models.CharField(blank=True, null=True, max_length=100)
    ca_group = models.CharField(default='ma', blank=True, null=True, max_length=100)
    userid = models.CharField(unique=True, max_length=6, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'ca_user'


class Patient(models.Model):
    cat_id = models.CharField(unique=True, max_length=8, blank=True, null=True)
    patient_name = models.CharField()
    birthday = models.DateField(blank=True, null=True)
    initial_diagnosis = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    comment = models.CharField(blank=True, null=True)
    record_number = models.CharField(max_length=100)
    hospital = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient'
        unique_together = (('id', 'patient_name', 'record_number'),)


class SampleBarcode(models.Model):
    sample_barcode_detail = models.CharField(primary_key=True, max_length=12)
    sample_barcode = models.CharField(max_length=9, blank=True, null=True)
    project = models.CharField(max_length=2, blank=True, null=True)
    source = models.CharField(max_length=5, blank=True, null=True)
    extract = models.DateTimeField(blank=True, null=True)
    cat = models.ForeignKey(Patient, models.DO_NOTHING, to_field='cat_id', blank=True, null=True)
    quota = models.IntegerField(blank=True, null=True)
    done = models.IntegerField(blank=True, null=True)
    expired = models.IntegerField(blank=True, null=True)
    lock = models.IntegerField(blank=True, null=True)
    physical_comment = models.CharField(blank=True, null=True)
    histological_comment = models.CharField(blank=True, null=True)
    tube_type = models.CharField(max_length=10, blank=True, null=True)
    sample_quality = models.CharField(max_length=30, blank=True, null=True)
    existing_sample_barcode = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sample_barcode'


class Qrcode(models.Model):
    qrcode = models.CharField(primary_key=True)
    sample_barcode_detail = models.ForeignKey('SampleBarcode', models.DO_NOTHING, db_column='sample_barcode_detail')
    experiment_barcode = models.CharField(blank=True, null=True)
    work_order = models.ForeignKey('WorkOrder', models.DO_NOTHING, db_column='work_order', blank=True, null=True)
    machine = models.CharField(blank=True, null=True)
    location = models.CharField(max_length=1, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    version = models.CharField(max_length=1, blank=True, null=True)
    comment = models.CharField(blank=True, null=True)
    antibody_type = models.CharField(blank=True, null=True)
    chip_type = models.CharField(blank=True, null=True)
    cover_type = models.CharField(blank=True, null=True)
    operating_type = models.CharField(blank=True, null=True)
    operator = models.CharField(blank=True, null=True)
    preprocess_type = models.CharField(blank=True, null=True)
    preprocess_start_time = models.DateTimeField(blank=True, null=True)
    preprocess_end_time = models.DateTimeField(blank=True, null=True)
    cell_reveal_start_time = models.DateTimeField(blank=True, null=True)
    cell_reveal_end_time = models.DateTimeField(blank=True, null=True)
    nis_start_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    nis_end_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    cat_start_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    cat_end_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    report_time = models.DateTimeField(blank=True, null=True)
    report_path = models.CharField(blank=True, null=True)
    preprocess_comment = models.CharField(blank=True, null=True)
    cell_reveal_comment = models.CharField(blank=True, null=True)
    preprocess_barcode = models.CharField(max_length=15, blank=True, null=True)
    preprocess_work_order = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qrcode'


class WorkOrder(models.Model):
    work_order = models.CharField(primary_key=True, max_length=8)
    add_time = models.DateTimeField(blank=True, null=True)
    receive_time = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    finish_time = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(CaUser, models.DO_NOTHING, db_column='owner', to_field='userid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'work_order'

    
class Cat(models.Model):
    qrcode = models.OneToOneField('Qrcode', models.DO_NOTHING, db_column='qrcode', primary_key=True)
    log = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'cat'


class CatReport(models.Model):
    qrcode = models.ForeignKey('Qrcode', models.DO_NOTHING, db_column='qrcode', blank=True, null=True)
    new_qrcode = models.CharField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cat_report'


class Nis(models.Model):
    qrcode = models.CharField(blank=True, null=True)
    parameter = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'nis'


class ReportData(models.Model):
    date = models.DateField(blank=True, null=True)
    work_order = models.ForeignKey('WorkOrder', models.DO_NOTHING, db_column='work_order', blank=True, null=True)
    qrcode = models.ForeignKey(Qrcode, models.DO_NOTHING, db_column='qrcode', blank=True, null=True)
    candidate = models.IntegerField(blank=True, null=True)
    cat = models.CharField(blank=True, null=True)
    modify = models.CharField(max_length=1, blank=True, null=True)
    final = models.CharField(blank=True, null=True)
    userid = models.ForeignKey(CaUser, models.DO_NOTHING, db_column='userid', to_field='userid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_data'


class Machine(models.Model):
    location_value = models.CharField(blank=True, null=True)
    checkbox_text = models.CharField(blank=True, null=True)
    checkbox_value = models.CharField(primary_key=True)
    visible = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'machine'


class AntibodyDropdown(models.Model):
    option_text = models.CharField(blank=True, null=True)
    option_value = models.CharField(primary_key=True)
    visible = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'antibody_dropdown'


class CellReveal(models.Model):
    qrcode = models.CharField(blank=True, null=True)
    parameter = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'cell_reveal'


class ChipDropdown(models.Model):
    option_text = models.CharField(blank=True, null=True)
    option_value = models.CharField(primary_key=True)
    visible = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chip_dropdown'


class CoverDropdown(models.Model):
    option_text = models.CharField(blank=True, null=True)
    option_value = models.CharField(primary_key=True)
    visible = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cover_dropdown'


class LocationDropdown(models.Model):
    option_text = models.CharField(blank=True, null=True)
    option_value = models.CharField(primary_key=True)
    visible = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_dropdown'


class OperatingDropdown(models.Model):
    option_text = models.CharField(blank=True, null=True)
    option_value = models.CharField(primary_key=True)
    visible = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operating_dropdown'


class PreprocessDropdown(models.Model):
    option_text = models.CharField(blank=True, null=True)
    option_value = models.CharField(primary_key=True)
    visible = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preprocess_dropdown'


class ProjectDropdown(models.Model):
    option_text = models.CharField(blank=True, null=True)
    option_value = models.CharField(primary_key=True)
    visible = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_dropdown'


class ProtocolDropdown(models.Model):
    option_text = models.CharField(blank=True, null=True)
    option_value = models.CharField(primary_key=True)
    visible = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'protocol_dropdown'


class SampleBarcodeResult(models.Model):
    sample_barcode = models.CharField(primary_key=True, max_length=9)
    result = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sample_barcode_result'


class SourceDropdown(models.Model):
    option_text = models.CharField(blank=True, null=True)
    option_value = models.CharField(primary_key=True)
    visible = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source_dropdown'


# Django內建模型
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


# Django內建模型
class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


# Django內建模型
class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


# Django內建模型
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

    REQUIRED_FIELDS = 'username'
    USERNAME_FIELD = 'username'

    class Meta:
        managed = False
        db_table = 'auth_user'


# Django內建模型
class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


# Django內建模型
class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


# Django內建模型
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


# Django內建模型
class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


# Django內建模型
class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


# Django內建模型
class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'