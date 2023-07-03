from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, ListView
from .models import Leave
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .utility import send_leave_notification_mail, send_leave_status_email


@method_decorator(csrf_exempt, name="dispatch")
class LeaveCreateView(LoginRequiredMixin, CreateView):
    """
    API For an Employee to create a leave request,
    accepts key-value and returns message as JSON
    """

    model = Leave
    fields = ["employee", "leave_type", "start_date", "end_date", "reason"]

    def dispatch(self, request, *args, **kwargs):
        """
        Overriding dispatch method to send a response message,
        when user is not logged in
        """
        if not self.request.user.is_authenticated:
            return JsonResponse(
                {"message": "User is not logged in"}, status=401
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        leave_type = request.POST.get("leave_type")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason")

        employee = request.user.employee

        leave = Leave(
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
        )
        leave.save()

        # Send notification email to HR designated Employee
        send_leave_notification_mail(leave)

        return JsonResponse({"message": "Leave applied successfully"})


@method_decorator(csrf_exempt, name="dispatch")
class LeaveListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Leave

    def dispatch(self, request, *args, **kwargs):
        """
        Overriding dispatch method to send a response message,
        when user is not logged in
        """
        if not self.request.user.is_authenticated:
            return JsonResponse(
                {"message": "User is not logged in"}, status=401
            )
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        user = self.request.user
        if user.employee.designation == "HR":
            return True
        return False

    def get(self, request, *args, **kwargs):
        # leave = self.get_object()
        leaves = self.get_queryset()
        print(leaves)
        data = [
            {
                "id": leave.id,
                "employee": leave.employee.full_name(),
                "leave_type": leave.leave_type,
                "start_date": leave.start_date,
                "end_date": leave.end_date,
                "is_approved": leave.is_approved,
                "reason": leave.reason,
                "approved_by": leave.get_approved_by(),
            }
            for leave in leaves
        ]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class LeaveApprovalView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Leave

    def dispatch(self, request, *args, **kwargs):
        """
        Overriding dispatch method to send a response message,
        when user is not logged in
        """
        if not self.request.user.is_authenticated:
            return JsonResponse(
                {"message": "User is not logged in"}, status=401
            )
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        """
        Method for allowing only HR designated employee,
        to update the leave approval.
        """
        user = self.request.user
        if user.employee.designation == "HR":
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Method to see the individual leave request,
        for the user with permission.
        """
        leave = self.get_object()
        data = [
            {
                "id": leave.id,
                "employee": leave.employee.full_name(),
                "leave_type": leave.leave_type,
                "start_date": leave.start_date,
                "end_date": leave.end_date,
                "is_approved": leave.is_approved,
                "reason": leave.reason,
                "approved_by": leave.get_approved_by(),
            }
        ]
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **kwargs):
        """
        Overriding the post method for leave approval.
        """
        leave_id = kwargs.get("pk")
        leave = get_object_or_404(Leave, id=leave_id)

        is_approved = request.POST.get("is_approved")
        leave.is_approved = is_approved
        leave.approved_by = request.user.employee
        leave.save()

        # Send notification email to the requested employee
        send_leave_status_email(leave)

        if is_approved.lower() == "true":
            return JsonResponse(
                {"message": "Leave Request Approved successfully"}
            )
        else:
            return JsonResponse({"message": "Leave Request REJECTED !"})
