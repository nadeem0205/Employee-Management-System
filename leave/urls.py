from django.urls import path
from . import views

urlpatterns = [
    # Employee Leave application endpoint
    path("apply/", views.LeaveCreateView.as_view(), name="leave-apply"),
    # All leave listing endpoint
    path("list/", views.LeaveListView.as_view(), name="leave-list"),
    # Employee Leave approval endpoint
    path(
        "approval/<int:pk>/",
        views.LeaveApprovalView.as_view(),
        name="leave-approval",
    ),
]
