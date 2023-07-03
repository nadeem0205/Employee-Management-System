from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from .models import Employee
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


class EmployeeListView(ListView):
    """
    API to list all employees returned as JSON
    """

    model = Employee

    def get(self, request, *args, **kwargs):
        """
        Overriding the get method.
        """
        print(request.user)
        employees = self.get_queryset()
        print(employees)
        data = [
            {
                "id": employee.id,
                "user": employee.user.username,
                "Employee id": employee.emp_id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "email": employee.email,
                "phone_number": employee.phone_number,
                "date_of_birth": employee.date_of_birth,
                "designation": employee.designation,
            }
            for employee in employees
        ]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeCreateView(LoginRequiredMixin, CreateView):
    """
    API to create an Employee accepts JSON post requests,
    returns message as JSON
    """

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

    model = Employee
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        """
        Overriding the post method.
        """
        data = json.loads(request.body)
        print(request.user)
        print(data)

        employee = Employee(
            user=request.user,
            emp_id=data.get("emp_id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            date_of_birth=data.get("date_of_birth"),
            designation=data.get("designation"),
        )
        try:
            employee.save()
            return JsonResponse({"message": "Employee created successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)})


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    API to update an Employee accepts JSON post requests,
    returns message as JSON
    """

    model = Employee

    def test_func(self):
        employee = self.get_object()
        if self.request.user == employee.user:
            return True
        return False

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
        """
        Overriding the post method.
        """
        employee = self.get_object()
        data = json.loads(request.body)

        if "first_name" in data:
            employee.first_name = data["first_name"]
        if "last_name" in data:
            employee.last_name = data["last_name"]
        if "email" in data:
            employee.email = data["email"]
        if "phone_number" in data:
            employee.phone_number = data["phone_number"]
        if "date_of_birth" in data:
            employee.date_of_birth = data["date_of_birth"]
        if "designation" in data:
            employee.designation = data["designation"]

        try:
            employee.save()
            return JsonResponse({"message": "Employee updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)})


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    API to detele an Employee accepts delete request with specific employee endpoint,
    returns message as JSON
    """

    model = Employee

    def test_func(self):
        employee = self.get_object()
        if self.request.user == employee.user:
            return True
        return False

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

    def delete(self, request, *args, **kwargs):
        """
        Overriding the delete method.
        """
        self.pk = self.kwargs.get(self.pk_url_kwarg)
        print(self.pk)
        try:
            employee = self.model.objects.get(pk=self.pk)
            employee.delete()
            return JsonResponse({"message": "Employee deleted successfully"})
        except self.model.DoesNotExist:
            return JsonResponse({"error": "Employee not found"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
