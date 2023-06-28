from django.urls import path
from . import views

urlpatterns = [
    # All Employee listing endpoint
    path('list/', views.EmployeeListView.as_view(), name='employee_list' ),

    # Employee creation endpoint
    path('create/', views.EmployeeCreateView.as_view(), name='employee_create'),

    # Employee Updation endpoint
    path('update/<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee_update'),

    # Employee deletion endpoint
    path('delete/<int:pk>/', views.EmployeeDeleteView.as_view(), name='employee_delete'),

]