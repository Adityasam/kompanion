from django.db import models
from django.urls import reverse
import datetime

class Database(models.Model):
    imei=models.CharField(max_length=100, default=None, null=True, blank=True)
    brand=models.CharField(max_length=100, default=None, null=True, blank=True)
    tab_id=models.CharField(max_length=10 , default=None, null=True)
    current_center=models.PositiveIntegerField(default=None, null=True)
    allotted_date=models.DateField(default=datetime.date.today, null=True, blank=True)
    allotted_time=models.CharField(max_length=10, default=None, null=True, blank=True)
    received_date=models.DateField(default=None, null=True, blank=True)
    received_time=models.CharField(max_length=10, default=None, null=True, blank=True)
    previous_centers=models.TextField(default=None, null=True, blank=True)
    received=models.BooleanField(default=False)
    allotted_to=models.CharField(max_length=100, default=None, null=True, blank=True)
    project=models.CharField(max_length=100, default=None, null=True, blank=True)
    start_date=models.DateField(default=None, null=True, blank=True)
    start_time=models.CharField(max_length=10, default=None, null=True, blank=True)
    end_date=models.DateField(default=None, null=True, blank=True)
    end_time=models.CharField(max_length=10, default=None, null=True, blank=True)
    damaged=models.BooleanField(default=False)
    under_maintenance=models.BooleanField(default=False)
    allotted=models.BooleanField(default=False)
    previous_allotment=models.TextField(default=None, null=True, blank=True)
    damage_record=models.TextField(default=None, null=True, blank=True)

    class Meta:
        ordering=('imei',)

class Center(models.Model):
    center_id=models.PositiveIntegerField()
    name=models.CharField(max_length=100)
    allotted=models.PositiveIntegerField(default=0)

    class Meta:
        ordering=('center_id',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:detail', args=[self.center_id])

class Maintenance(models.Model):
    under_maintenance=models.BooleanField(default=False)