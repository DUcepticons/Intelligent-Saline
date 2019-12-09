from django.contrib import admin
from .models import patient

from django.contrib.auth.models import Group  #for deleting Groups

# Register your models here.
admin.site.register(patient)
admin.site.unregister(Group)

admin.site.site_header = 'DUcepticons Administration'
admin.site.site_title = 'DUcepticons'


