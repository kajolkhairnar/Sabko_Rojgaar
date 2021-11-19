"""Sabko_Rojgaar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job_portal.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index ,name="index"),
path('admin_login',admin_login,name='admin_login'),
path('Employeer_login',Employeer_login,name='Employeer_login'),
path('Employee_login',Employee_login,name='Employee_login'),
path('employee_sign_up',employee_sign_up,name='employee_sign_up'),
path('Employee_Profile',Employee_Profile,name='Employee_Profile'),
path('Logout',Logout,name='Logout'),
path('Employeer_Signup',Employeer_Signup,name='Employeer_Signup'),
path('Employeer_Profile',Employeer_Profile,name='Employeer_Profile'),
path('admin_Profile',admin_Profile,name='admin_Profile'),
path('view_Employee',view_Employee,name='view_Employee'),
path('view_Employeers',view_Employeers,name='view_Employeers'),
path('delete_Employee/<int:pid>',delete_Employee,name='delete_Employee'),
path('pending_request',pending_request,name='pending_request'),
path('change_Status/<int:pid>',change_Status,name='change_Status'),
path('accepted_request',accepted_request,name='accepted_request'),
path('rejected_request',rejected_request,name='rejected_request'),
path('All_Employeers',All_Employeers,name='All_Employeers'),
path('delete_Employeer/<int:pid>',delete_Employeer,name='delete_Employeer'),
path('change_password',change_password,name='change_password'),
path('change_password_Rect',change_password_Rect,name='change_password_Rect'),
path('change_password_Emp',change_password_Emp,name='change_password_Emp'),
path('Add_Job',Add_Job,name='Add_Job'),
path('Job_List',Job_List,name='Job_List'),
path('Edit_Job/<int:pid>',Edit_Job,name='Edit_Job'),
path('change_company_images/<int:pid>',change_company_images,name='change_company_images'),
path('latest_jobs',latest_jobs,name='latest_jobs'),
path('employee_job_list',employee_job_list,name='employee_job_list'),
path('Job_Detail/<int:pid>',Job_Detail,name='Job_Detail'),
path('Apply_for_job/<int:pid>',Apply_for_job,name='Apply_for_job'),
path('Applied_Employee_List',Applied_Employee_List,name='Applied_Employee_List'),
path('contact',contact,name='contact'),
path('delete_job/<int:pid>',delete_job,name='delete_job'),
path('Accept_Application/<int:pid>',Accept_Application,name='Accept_Application'),
path('Reject_Application/<int:pid>',Reject_Application,name='Reject_Application'),
path('submit',submit,name='submit'),



]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



