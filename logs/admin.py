from django.contrib import admin
from logs.models import APILogEntry

admin.site.register(APILogEntry)
