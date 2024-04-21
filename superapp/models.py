from django.db import models
from django.contrib.auth.models import AbstractUser

#Добавить поля
#Надо бы переименовать... только лень)

class Doctor(AbstractUser):
    klapan = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    fathers_name = models.CharField(max_length=40)
    sex_choices = [
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
    ]
    sex = models.CharField(max_length=7, choices=sex_choices, default='Мужской')
    date_of_birth = models.DateField(null=True)
    date_of_operation = models.DateField(null=True)
    date_of_death = models.DateField(null=True)
    height = models.CharField(max_length=5)
    comment_created_at = models.TextField()
    times_of_creating_comments = models.TextField()
    #Измерения поехали
    weight = models.TextField()
    diastolic_pressure = models.TextField()
    arteric_pressure = models.TextField()
    heart_pulse = models.TextField()
    temperature = models.TextField(null=True)
    oxygen_blood = models.TextField(null=True)
    pulse_metrics_date = models.TextField()
    pulse_metrics_time = models.TextField(null=True)
    weight_metrics_date = models.TextField()
    weight_metrics_time = models.TextField(null=True)
    pressure_metrics_date = models.TextField()
    pressure_metrics_time = models.TextField(null=True)
    temperature_metrics_date = models.TextField(null=True)
    temperature_metrics_time = models.TextField(null=True)
    oxygen_blood_date = models.TextField(null=True)
    oxygen_blood_time = models.TextField(null=True)
    #Измерения закончились
    allergies = models.TextField(null=True)
    side_effects = models.TextField(null=True)
    illnesses = models.TextField()
    intolerant_drugs = models.TextField(null=True)
    illnesses_patient = models.TextField(null=True)
    drugs = models.TextField()
    drugs_patient = models.TextField(null=True)
    time_drugs_patient = models.TextField(null=True)
    comments = models.TextField()
    medication_schedule = models.TextField(null=True)
    date_of_made_klapan = models.DateField(null=True)
    manufacturer = models.CharField(max_length=40)
    is_doctor = models.BooleanField(default=False)
    # doctor
    comments_patient = models.TextField(null=True)
    t_number = models.CharField(max_length=12)
    workplace = models.TextField()
    position = models.CharField(max_length=40)
    doctor_id = models.IntegerField(null=True)
    heart_pulse_list = models.TextField()
    is_called = models.BooleanField(default=False)
    date_of_visit = models.TextField(null=True)
    last_id = models.IntegerField(null=True)
    last_date = models.CharField(max_length=255, null=True)
    codes = models.TextField(null=True)
    def __str__(self):
        return self.username

    USERNAME_FIELD = 'username'


class Dairy(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    user_id = models.IntegerField()


class Room(models.Model):
    id_doctor = models.IntegerField()
    id_patient = models.IntegerField()

class Message(models.Model):
    sender = models.CharField(max_length=255)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    patient_id = models.IntegerField(null=True)
    doctor_id = models.IntegerField(null=True)



'''
@receiver(pre_save, sender=Doctor)
def update_custom_field_created_at(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Doctor.objects.get(pk=instance.pk)
        if old_instance.heart_pulse != instance.heart_pulse:
            instance.comment_created_at = timezone.now()
    else:
        instance.comment_field_created_at = timezone.now()
'''
'''    
@receiver(pre_save, sender=Doctor)
def add_in_times(self, sender, instance, *args, **kwargs):
    if instance.pk:
        old_instance = Doctor.objects.get(pk=instance.pk)
        if old_instance.heart_pulse != instance.heart_pulse:
            instance.comment_created_at = timezone.now()
            self.times_of_creating_comments += str(self.comment_created_at)
            self.times_of_creating_comments += ', '
            super().save(*args, **kwargs)

'''
