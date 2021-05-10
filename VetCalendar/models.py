from django.db import models
from loginApp.models import User
import re, datetime

class Shift(models.Model):
    shift = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u'{0}'.format(self.shift)

class ShiftType(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ScheduleShift(models.Model):
    date = models.DateField()
    shift = models.ForeignKey(Shift, related_name='assignments', on_delete=models.CASCADE)
    shift_type = models.ForeignKey(ShiftType, related_name='assigned_types', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_shifts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Request(models.Model):
    requestUser = models.ForeignKey(User, related_name='user_requests', on_delete=models.CASCADE)
    switchUser = models.ForeignKey(User, related_name='user_switches', on_delete=models.CASCADE)
    request_type = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
