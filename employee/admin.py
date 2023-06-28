from django.contrib import admin
from . models import Employee

# We have to register new models here to view,
#  in django admin panel
admin.site.register(Employee)
