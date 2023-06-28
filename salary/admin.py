from django.contrib import admin
from .models import Salary

# We have to register new models here to view,
#  in django admin panel
admin.site.register(Salary)
