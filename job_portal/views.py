from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
from django.http import HttpResponse
import twilio
import zerosms
from django.core.mail import send_mail as sm
# Create your views here.

def index(request):
    return render(request,'index.html')

def admin_login(request):
    error =""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user=authenticate(username=u,password=p)
        try:
            if user.is_staff:
                 login(request,user)
                 error="no"
            else:
                 error = "yes"
        except:
             error="yes"
    d={'error':error}
    return render(request,'admin_login.html',d)

def Employeer_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = EmploymentProvideruser.objects.get(user=user)
                if user1.type == "Employeer" and user1.Status!="pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}
    return render(request,'Employeer_login.html',d)

def Employee_login(request):
    error=""
    if request.method=='POST':
        u = request.POST['email']
        p = request.POST['pwd']
        user=authenticate(username=u,password=p)
        if user:
            try:
                user1=Jobseekeruser.objects.get(user=user)
                if user1.type=="Employee":
                     login(request,user)
                     error="no"
                else:
                     error="yes"
            except:
                error="yes"
        else:
            error="yes"
    d={'error':error}
    return render(request,'Employee_login.html',d)

def employee_sign_up(request):
    error=""
    if request.method=='POST':
                            f=request.POST['fname']
                            l=request.POST['lname']
                            e=request.POST['email']
                            con=request.POST['contact']
                            fm=request.POST['gender']
                            p=request.POST['pwd']
                            i=request.FILES['photo']
                            try:
                                 user=User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
                                 Jobseekeruser.objects.create(user=user,mobile=con,image=i,gender=fm,type="Employee")
                                 error='no'
                            except:
                                 error='yes'
    d={'error':error}
    return render(request,'employee_sign_up.html',d)


def Employee_Profile(request):
    if not request.user.is_authenticated:
       return redirect('Employee_login')
    user = request.user
    employee = Jobseekeruser.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        fm = request.POST['gender']


        employee.user.first_name = f
        employee.user.last_name = l
        employee.mobile = con
        employee.gender = fm


        try:
            employee.save()
            employee.user.save()
            error = 'no'

        except:
            error = 'yes'

        try:
            i = request.FILES['photo']
            employee.image = i
            employee.save()
            error = 'no'

        except:
            pass

    d = {'employee': employee, 'error': error}
    return render(request, 'Employee_Profile.html',d)

def Logout(request):
    logout(request)
    return redirect('index')
def Employeer_Signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        fm = request.POST['gender']
        p = request.POST['pwd']
        i = request.FILES['photo']
        w = request.POST['workplace']
        a = request.POST['workplace_area']


        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            EmploymentProvideruser.objects.create(user=user, mobile=con, image=i, gender=fm,workplace=w,workarea=a,type="Employeer",Status= "Pending")
            error = 'no'
        except:
            error = 'yes'
    d = {'error': error}
    return render(request, 'Employeer_Signup.html',d)

def Employeer_Profile(request):
    if not request.user.is_authenticated:
       return redirect('Employeer_login')
    user=request.user
    employeer=EmploymentProvideruser.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']

        con = request.POST['contact']
        fm = request.POST['gender']


        w = request.POST['workplace']
        a = request.POST['workplace_area']
        employeer.user.first_name=f
        employeer.user.last_name = l
        employeer.mobile = con
        employeer.gender = fm
        employeer.workplace = w
        employeer.workplace_area = a

        try:
            employeer.save()
            employeer.user.save()
            error='no'

        except:
            error='yes'

        try:
            i = request.FILES['photo']
            employeer.image=i
            employeer.save()
            error='no'

        except:
            pass




    d={'employeer':employeer,'error':error}
    return render(request, 'Employeer_Profile.html',d)


def admin_Profile(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    rcount = EmploymentProvideruser.objects.all().count()
    scount = Jobseekeruser.objects.all().count()
    d={'rcount':rcount,'scount':scount}
    return render(request, 'admin_Profile.html',d)


def view_Employee(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    data=Jobseekeruser.objects.all()
    d={'data':data}
    return render(request, 'view_Employee.html',d)

def view_Employeers(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    return render(request, 'view_Employeers.html')

def delete_Employee(request,pid):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    Emp=User.objects.get(id=pid)
    Emp.delete()
    return redirect('view_Employee')
def pending_request(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    data=EmploymentProvideruser.objects.filter(Status="Pending")
    d={'data':data}
    return render(request,'pending_request.html',d)

def change_Status(request,pid):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    error=""
    Emp=EmploymentProvideruser.objects.get(id=pid)
    if request.method=="POST":
        s=request.POST['status']
        Emp.Status=s
        try:
            Emp.save()
            error="no"
        except:
            error="yes"
    d={'Emp':Emp,'error':error}
    return render(request,'change_Status.html',d)

def accepted_request(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    data=EmploymentProvideruser.objects.filter(Status="Accept")
    d={'data':data}
    return render(request,'accepted_request.html',d)

def rejected_request(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    data=EmploymentProvideruser.objects.filter(Status="Reject")
    d={'data':data}
    return render(request,'rejected_request.html',d)

def All_Employeers(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    data=EmploymentProvideruser.objects.all
    d={'data':data}
    return render(request,'All_Employeers.html',d)

def delete_Employeer(request,pid):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    Emp=EmploymentProvideruser.objects.get(id=pid)
    Emp.delete()
    return redirect('view_Employeers')

def change_password(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    error=""
    if request.method=="POST":
        c=request.POST['pwd']
        n=request.POST['npwd']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
               u.set_password(n)
               u.save()
               error="no"
            else:
               error="not"

        except:
           error="yes"

    d={'error':error}
    return render(request,'change_password.html',d)

def change_password_Emp(request):
    if not request.user.is_authenticated:
       return redirect('Employee_login')
    error=""
    if request.method=="POST":
        c=request.POST['pwd']
        n=request.POST['npwd']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
               u.set_password(n)
               u.save()
               error="no"
            else:
               error="not"

        except:
           error="yes"

    d={'error':error}
    return render(request,'change_password_Emp.html',d)

def change_password_Rect(request):
    if not request.user.is_authenticated:
       return redirect('Employeer_login')
    error=""
    if request.method=="POST":
        c=request.POST['pwd']
        n=request.POST['npwd']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
               u.set_password(n)
               u.save()
               error="no"
            else:
               error="not"

        except:
           error="yes"

    d={'error':error}
    return render(request,'change_password_Rect.html',d)





def Edit_Job(request,pid):
    if not request.user.is_authenticated:
       return redirect('Employeer_login')
    error = ""
    job = Job.objects.get(id=pid)
    if request.method == 'POST':

       t = request.POST['title']
       sd = request.POST['sdate']
       ed = request.POST['edate']
       sal = request.POST['salary']
       exp = request.POST['experience']
       loc = request.POST['location']
       skills = request.POST['skills']
       des = request.POST['description']
       job.Title=t
       job.Job_description=des
       job.location=loc
       job.salary=sal
       job.experience=exp
       job.Skills=skills


       try:
         job.save()
         error = 'no'

       except:

        error = 'yes'
        if sd:
            try:
              job.start_date=sd
              job.save()
            except:
                pass

        else :
            pass
        
        if ed:
            try:
              job.e_date=ed
              job.save()
            except:
                pass

        else :
            pass

    d = {'error': error,'job':job}
    return render(request, 'Edit_Job.html',d)

def Job_List(request):
    if not request.user.is_authenticated:
       return redirect('Employeer_login')
    
    user = request.user
    employeer = EmploymentProvideruser.objects.get(user=user)

    job = Job.objects.filter(Employeer=employeer)
    d={'job':job}

    return render(request, 'Job_List.html',d)

def Add_Job(request):
    if not request.user.is_authenticated:
       return redirect('Employeer_login')

    error = ""
    if request.method == 'POST':
        t = request.POST['title']
        sd = request.POST['sdate']
        ed = request.POST['edate']
        sal = request.POST['salary']
        wor = request.FILES['workplace_images']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']

        user = request.user

        employeer = EmploymentProvideruser.objects.get(user=user)


        try:
            Job.objects.create(Employeer= employeer , start_date=sd,end_date=ed,Title=t,salary=sal,Job_description=des,workplace_images=wor,experience=exp,location=loc,Skills=skills,date_of_creation=date.today())
            error = 'no'

        except:

            error = 'yes'

    d = {'error': error}

    return render(request, 'Add_Job.html',d)


def change_company_images(request,pid):
    if not request.user.is_authenticated:
        return redirect('Employeer_login')
    error = ""
    job=Job.objects.get(id=pid)
    if request.method=='POST':
        wimg=request.FILES['images']
        job.workplace_images=wimg
        try:
            job.save()
            error='no'
        except:
            error='yes'

    d={'error':error,'job':job}
    return render(request, 'change_company_images.html', d)


def latest_jobs(request):
    job = Job.objects.all().order_by('-start_date')
    d = {'job': job}
    return render(request, 'latest_jobs.html',d)

def employee_job_list(request):
    job=Job.objects.all().order_by('-start_date')
    user=request.user
    employee=Jobseekeruser.objects.get(user=user)
    data=Employee_Jobs.objects.filter(employee=employee)
    li=[]
    for i in data:
        li.append(i.job.id)

    d = {'job': job,'li':li}
    return render(request, 'employee_job_list.html',d)

def Job_Detail(request,pid):
    job = Job.objects.get(id=pid)


    d = {'job': job}
    return render(request, 'Job_Detail.html',d)

def Apply_for_job(request,pid):
    if not request.user.is_authenticated:
        return redirect('Employeer_login')
    error = ""
    user=request.user
    employee= Jobseekeruser.objects.get(user=user)
    job=Job.objects.get(id=pid)
    date1=date.today()
    if job.end_date<date1:
        error="close"
    elif job.start_date>date1:
        error="notopened"
    else:
        if request.method == 'POST':
            res = request.FILES['resume']
            Employee_Jobs.objects.create(job=job,employee=employee,document=res,applied_date=date.today())
            error="done"




    d={'error':error}
    return render(request, 'Apply_for_job.html', d)

def Applied_Employee_List(request):
    if not request.user.is_authenticated:
        return redirect('Employeer_login')
    data = Employee_Jobs.objects.all()
    status=""
    if request.path=="Accept_Application":
        status="Accept"
    else:
        status="Reject"


    
    d={'data':data,'status':status}
    return render(request, 'Applied_Employee_List.html', d)

def contact(request):

    return render(request, 'contact.html')


def delete_job(request,pid):
    if not request.user.is_authenticated:
       return redirect('Employeer_login')
    job=Job.objects.get(id=pid)
    job.delete()
    return redirect('Job_List')

def Accept_Application(request,pid):
    if not request.user.is_authenticated:
       return redirect('Employeer_login')
       error=""
    
    
    if "telephone" in request.POST and "mobile" in request.POST and "message" in request.POST:
        mob1=request.POST['telephone']
        password=request.POST['password']
        mob2=request.POST['mobile']
        msg=request.POST['message']
        
        
        zerosms.sms(phno=mob1,passwd=password,receivernum=mob2,message=msg)
        return HttpResponse("Message Send Successfully")
        error="yes"
    

    else:
        error="no"



    d={'error':error}

    return render(request,'Accept_Application.html',d)

def Reject_Application(request,pid):
    if not request.user.is_authenticated:
       return redirect('Employeer_login')

    emp=Employee_Jobs.objects.get(id=pid)
    emp.delete()
    return render(request,'Reject_Application.html')


def submit(request):
    status=""
    status="Accept"
    d={'status':status}
    return render(request, 'submit.html',d)
























