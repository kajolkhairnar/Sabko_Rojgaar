from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Jobseekeruser(models.Model):
                user=models.ForeignKey(User,on_delete=models.CASCADE)
                mobile=models.IntegerField()
                image=models.FileField(null=False)
                gender=models.CharField(max_length=10,null=True)
                type=models.CharField(max_length=15)
                edu=models.CharField(max_length=100,null=True)
                jobd=models.CharField(max_length=100,null=True)
                sal=models.CharField(max_length=100,null=True)
                def _str_(self):
                   return self.user.username


class EmploymentProvideruser(models.Model):
                user = models.ForeignKey(User, on_delete=models.CASCADE)
                mobile = models.IntegerField()
                image = models.FileField(null=False)
                gender = models.CharField(max_length=10, null=True)
                workplace =models.CharField(max_length=100,null=True)
                workarea = models.CharField(max_length=100,null=True)
                type = models.CharField(max_length=15,null=True)
                Status = models.CharField(max_length=20,null=True)
                def _str_(self):
                    return self.user.username


class Job(models.Model):
    Employeer = models.ForeignKey(EmploymentProvideruser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    Title = models.CharField(max_length=100)
    salary = models.FloatField(max_length=20)
    Job_description = models.CharField(max_length=300)
    workplace_images = models.FileField(null=True)
    experience = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    Skills = models.CharField(max_length=100)
    date_of_creation = models.DateField()

    def _str_(self):
        return self.Title


class Employee_Jobs(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    employee = models.ForeignKey(Jobseekeruser, on_delete=models.CASCADE)
    document = models.FileField(null=True)
    applied_date = models.DateField()
    Status=models.CharField(max_length=20,default='Selected/Rejected')
    def _str_(self):
        return self.id

class sendresponse(models.Model):
    emp = models.ForeignKey(Employee_Jobs,on_delete=models.CASCADE)
    employee = models.ForeignKey(Jobseekeruser, on_delete=models.CASCADE)
    Employeer = models.ForeignKey(EmploymentProvideruser, on_delete=models.CASCADE)



    def _str_(self):
        return self.id
    





