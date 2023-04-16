from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.serializers.json import DjangoJSONEncoder
class TutoringUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_tutor = models.BooleanField(default=False)
    full_name = models.CharField(max_length=50)
    MAJOR_CHOICES = [
        ('ECE', 'Electrical/Computer Engineering'),
        ('BME', 'Biomedical Engineering'),
        ('CS', 'Computer Science'),
        ('HIS', 'History'),
        ('PSY', 'Psychology')
    ]
    def get_default():
        return list()
    major = models.CharField(max_length=3, choices=MAJOR_CHOICES)
    locations = ArrayField(models.CharField(max_length=20, default="NA"), default=get_default)
    is_virtual = models.BooleanField(default=False)
    classes = ArrayField(models.CharField(max_length=50, default="NA"), default=get_default)
    availability = ArrayField(models.CharField(max_length=255, default="NA"), default=get_default)
    pay_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    tutorSession = ArrayField(
        models.JSONField(encoder=DjangoJSONEncoder),
       default=get_default,
        blank=True,
        null=True
    )

    def set_availability(self, availabilities):
        self.tutorSession = availabilities

    def get_availability(self):
        return self.tutorSession

    def add_availability(self,date):
        self.tutorSession.append(date)

    def remove_availability(self, date):
        self.tutorSession.remove(date)

class TutorRequest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_requests')
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_requests')
    session_date = models.DateField()
    session_time = models.TimeField()
    duration= models.DecimalField(max_digits=5, decimal_places=2,default=0)
    description= models.CharField(max_length=255, null=True)
    pay_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    
