from django.db import models

# Create your models here.
class patient(models.Model):
	floor = models.IntegerField(default=0)
	room = models.IntegerField(default=0)
	bed_no = models.IntegerField(default=0)
	percentage = models.IntegerField(default=100)
	device_id =  models.CharField(max_length=50, null=True, blank=True)
	status = models.IntegerField(default = 1)
	buzzer_status = models.IntegerField(default = 5)
	patient_id =  models.CharField(max_length=50, null=True, blank=True)
	saline_info =  models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		return self.device_id
