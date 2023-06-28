from django.urls import path
from . import views

urlpatterns = [
    # All Employee Salary listing endpoint

    path('list/', views.SalaryListView.as_view(), name='salary-list'),

    # Employee Salary creation endpoint
    path('create/', views.SalaryCreateView.as_view(), name='salary-create'),

    # Employee Salary updation endpoint
    path('update/<int:pk>/', views.SalaryUpdateView.as_view(), name='salary-update'),

    # Employee Salary deletion endpoint
    path('delete/<int:pk>/', views.SalaryDeleteView.as_view(), name='salary-delete'),

]
