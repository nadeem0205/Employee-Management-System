from django.db import models
from employee.models import Employee

class Salary(models.Model):
    """
    Model for salary
    Atribs:
        employee(obj): Employee
        basic(float): Basic Pay of the employee
        hra(float): House Rent Allowance of the employee
        pf(float): Proviedent Fund of the employee
        esi(float): State Insurance of the employee
        allowance(float): Special Allowance of the employee
        net_salary(float): Net Salary of the employee
    """
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    basic = models.FloatField()
    hra = models.FloatField()
    pf = models.FloatField()
    esi = models.FloatField()
    allowance = models.FloatField() 
    net_salary = models.FloatField()

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} {self.net_salary}"
    