from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,BaseUserManager
#User1=User.objects.get(username='username')
#User1.is_admin= True
#User1.is_superuser = True
#User1.is_staff= True
#User1.save()
from django import forms
from . import models
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Book,Borrower,Student




    
class CreateAdminForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username', 'email', 'password1', 'password2']

class CreateStudentForm(forms.Form):
	username= forms.CharField(label='username',max_length=30)
	email=forms.EmailField(label='Email')
	password1=forms.CharField(label='Password',widget=forms.PasswordInput())
	password2=forms.CharField(label='Password(Again)',widget=forms.PasswordInput())

	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1=self.cleaned_data['password1']
			password2=self.cleaned_data['password2']
			if password1==password2:
				return password2
		raise forms.ValidationError('Passwords do not match.')


	def clean_username(self):
		username=self.cleaned_data['username']
		if not re.search(r'^\w+$',username):
			raise forms.ValidationError('Username can only contain alphabetic char and the underscore')
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		raise forms.ValidationError('Username already taken')


class BookModelForm(forms.ModelForm):
	class Meta:
		model= Book
		fields=['nameofbook','isbn','author','category']


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrower
        exclude = ['issue_date', 'return_date']
 
 
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'