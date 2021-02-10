from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from datetime import datetime,timedelta,date
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from . import forms,models
# Create your views here.
from .models import *
from .forms import 	*
#from .filters import OrderFilter

def AdminregisterPage(request):
	if request.user.is_authenticated:
		return redirect('adminlogin')
	else:
		#form = CustomUserManager()
		form=CreateAdminForm()
		if request.method == 'POST':
			form = CreateAdminForm(request.POST)
			#form = CustomUserManager(request.POST)
			if form.is_valid():

				user=form.save(commit=False)
				user.is_staff= True
				user.is_superuser=True
				user.save()
				password=form.cleaned_data.get('password')
				username = form.cleaned_data.get('username')
                #password=form.cleaned_data.get('password')
				user=authenticate(username=username,password=password)
				login(request,user)
				#my_admin_group=Group.objects.get_or_create(name='ADMIN')
				#my_admin_group[0].user_set.add(user)
				messages.success(request, 'Account was created for ' + user)

				return redirect('adminlogin')
			

			
    
		context = {'form':form}
		return render(request, 'accounts/adminregister.html', context)

def AdminloginPage(request):
	if request.user.is_authenticated:
		if user.is_superuser:
			return redirect('adminmainpage')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				if user.is_superuser:
					login(request, user)
				else:
					return HttpResponse("YOU ARE NOT AN ADMIN . IF YOU ARE NEW STAFF MEMBER PLEASE SIGN UP.")

				return redirect('adminmainpage')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
	
		return render(request, 'accounts/adminlogin.html', context)
@login_required(login_url='adminlogin')
def logoutUser(request):
    logout(request)
    return redirect('adminlogin')


def is_admin(user):
	return user.groups.filter(name='ADMIN').exists()


def adminhome(request):
    return render(request,'mainpage.html',{})
@login_required(login_url='adminlogin')
def adminmainpage(request):
	return render(request,'adminmainpage.html',{})





def StudentregisterPage(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.student.first_name = form.cleaned_data.get('first_name')
        user.student.last_name = form.cleaned_data.get('last_name')
        user.student.email = form.cleaned_data.get('email')
        user.student.RegisteredNo=form.cleaned_data.get('RegisteredNo')
        user.student.branch=form.cleaned_data.get('branch')
        user.student.BloodGroup=form.cleaned_data.get('BloodGroup')
        user.student.Current_Semester=form.cleaned_data.get('Current_Semester')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('studentlogin')
    else:
        form = SignUpForm()

    return render(request,'accounts/studentregister.html',{'form':form})


def is_student(user):
	return user.groups.filter(name='STUDENT').exists()

def StudentloginPage(request):

	
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user= authenticate(request, username=username, password=password)

		if user is not None:
			if user.is_superuser:
				return HttpResponse("YOU ARE NOT A STUDENT . PLEASE LOGIN AS ADMIN.")
			else:
				login(request,user)

			return redirect('studentmainpage')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	
	return render(request, 'accounts/studentlogin.html', context)


def studenthome(request):
    return render(request,'studententrypage.html',{})


@login_required(login_url='studentlogin')
#@user_passes_test(is_student)
def studentmainpage(request):
	

	return render(request,'studentmainpage.html',{})


@login_required(login_url='studentlogin')
def logoutStudent(request):
    logout(request)
    return redirect('studentlogin')

@login_required(login_url='studentlogin')
def BookListView(request):
	books=models.Book.objects.all()
	return render(request,'book_list1.html',{'books':books})

@login_required(login_url='studentlogin')
def student_BookListView(request):
    student=models.Student.objects.filter(user=request.user)
    issuedbook=models.IssuedBook.objects.filter(RegisteredNo=student[0].RegisteredNo)
    li1=[] ;li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].RegisteredNo,student[0].branch,book.nameofbook,book.author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
		#calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        d1=float(d)
        fine=0
        if d1>15:
            day=d1-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)
    return render(request,'student_booklist1.html',{'li1':li1,'li2':li2})	
	
@login_required(login_url='studentlogin')
def student_profile(request):
	return render(request,'studentprofile2.html',locals())

@login_required(login_url='studentlogin')
def borrow_request(request):
	form=BorrowRequestForm(request.POST)
	if form.is_valid():
		obj=form.save(commit=False)
		obj.save()
		return redirect("borrowsuccess")
	return render(request,'borrowrequest.html',{'form':form})



@login_required(login_url='studentlogin')
def borrowsuccess(request):
	return render(request,'borrowsuccess.html',{})


@login_required(login_url='adminlogin')
def addbook(request):
	form=BookModelForm(request.POST,request.FILES)
	if form.is_valid():
		obj=form.save(commit=False)
		obj.save()
		form=BookForm()
	return render(request,'addbook.html',{'form':form})


#@login_required(login_url='studentlogin')
def onlinebooks(request):
	return render(request,'onlinebooks.html',locals())