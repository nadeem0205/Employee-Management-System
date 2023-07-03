from django.db import models
from employee.models import Employee


class Leave(models.Model):
    LEAVE_TYPES = (
        ("casual", "Casual Leave"),
        ("sick", "Sick Leave"),
        ("restricted", "Restricted Leave"),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(max_length=500)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leave_approvals",
    )

    def __str__(self):
        return f"{self.employee} - {self.leave_type} Leave"

    def get_approved_by(self):
        if self.approved_by:
            return self.approved_by.full_name()
        return None

    def leave_details(self):
        return (
            f"Employee Name : {self.employee.full_name()} \n"
            f"Leave Type : {self.leave_type} \n"
            f"Start Date : {self.start_date} \n"
            f"End Date : {self.end_date} \n"
            f"Reason : {self.reason}"
        )
