from django.db import models

# Create your models here.
class patient(models.Model):
	floor = models.IntegerField(default=0)
	room = models.IntegerField(default=0)
	bed_no = models.IntegerField(default=0)
	percentage = models.IntegerField(default=0)





def __str__(self):
	return self.name