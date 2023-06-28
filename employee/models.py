from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    """
    Model for Employee
    Atribs:
        emp_id(int): Employee ID
        frist_name(str): First Name of employee
        last_name(str): Last Name of employee
        email(str): Email the employee
        phone_number(str): Phone Number of the employee
        Designation(str): Designation of the employee
    """
    emp_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True)
    designation = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def full_name(self):
        """
        Method to give the full name of the Employee
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name

