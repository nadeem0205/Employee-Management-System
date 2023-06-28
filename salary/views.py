from django.views.generic import(
    ListView,
    CreateView,
    UpdateView,
    DeleteView)
from .models import Salary
from employee.models import Employee
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin

class SalaryListView(ListView):
    model = Salary

    def get(self, request, *args, **kwargs):
        """
        Overriding the get method.
        """
        print(request.user)
        salary = self.get_queryset()
        data = [
            {'id' : salary.id,
             'employee': salary.employee.full_name(),
             'basic': salary.basic,
             'hra': salary.hra,
             'pf': salary.pf,
             'esi': salary.esi,
             'allowance': salary.allowance,
             'net_salary': salary.net_salary} for salary in salary
             ]
        print(data)
        return JsonResponse(data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class SalaryCreateView(LoginRequiredMixin, CreateView):
    model = Salary
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        """
        Overriding dispatch method to send a response message,
        when user is not logged in
        """
        if not self.request.user.is_authenticated:
            return JsonResponse({'message': 'User is not logged in'}, status=401)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Overriding the post method.
        """
        data = request.POST
        print(data['employee'])
        salary = Salary(
            employee = Employee.objects.get(emp_id=data['employee']),
            basic = data['basic'],
            hra = data['hra'],
            pf = data['pf'],
            esi = data['esi'],
            allowance = data['allowance'],
            net_salary = data['net_salary'],
        )
        print(salary.employee)
        try:
            salary.save()
            return JsonResponse({'message': 'Employee Salary created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class SalaryUpdateView(LoginRequiredMixin, UpdateView):
    model = Salary

    def dispatch(self, request, *args, **kwargs):
        """
        Overriding dispatch method to send a response message,
        when user is not logged in
        """
        if not self.request.user.is_authenticated:
            return JsonResponse({'message': 'User is not logged in'}, status=401)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Overriding the post method.
        """
        salary = self.get_object()
        data = request.POST

        if 'employee' in data:
            salary.employee = Employee.objects.get(emp_id=data['employee'])
        if 'basic' in data:
            salary.basic = data['basic']
        if 'hra' in data:
            salary.hra = data['hra']
        if 'pf' in data:
            salary.pf = data['pf']
        if 'esi' in data:
            salary.esi = data['esi']
        if 'allowance' in data:
            salary.allowance = data['allowance']
        if 'net_salary' in data:
            salary.net_salary = data['net_salary']

        try:
            salary.save()
            return JsonResponse({'message': 'Employee Salary updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class SalaryDeleteView(LoginRequiredMixin, DeleteView):
    model = Salary

    def dispatch(self, request, *args, **kwargs):
        """
        Overriding dispatch method to send a response message,
        when user is not logged in
        """
        if not self.request.user.is_authenticated:
            return JsonResponse({'message': 'User is not logged in'}, status=401)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Overriding the delete method.
        """
        self.pk = self.kwargs.get(self.pk_url_kwarg)
        print(self.pk)
        try:
            salary = self.model.objects.get(pk=self.pk)
            salary.delete()
            return JsonResponse({'message': 'Employee Salary deleted successfully'})
        except self.model.DoesNotExist:
            return JsonResponse({'error': 'Salary not found'})
        except Exception as e:
            return JsonResponse({'error': str(e)})