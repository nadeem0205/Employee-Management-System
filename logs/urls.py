from django.urls import path
from . import views

urlpatterns = [
    # Endpoint to see all the log entries
    path("list/", views.APILogEntryListView.as_view(), name="log-entry"),
]
