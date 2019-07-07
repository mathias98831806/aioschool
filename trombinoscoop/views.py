# -*- coding: utf-8 -*-

from datetime import datetime
from trombinoscoop.forms import LoginForm, StudentProfileForm, EmployeeProfileForm
from trombinoscoop.models import Person, Student, Employee
from django.shortcuts import render, redirect

def get_logged_user_from_request(request):
	if 'logged_user_id' in request.session:
		logged_user_id = request.session['logged_user_id']
		# On cherche un etudiant
		if len(Student.objects.filter(id=logged_user_id)) == 1:
			return Student.objects.get(id=logged_user_id)
		# On cherche un Employe
		elif len(Employee.objects.filter(id=logged_user_id)) == 1:
			return Employee.objects.get(id=logged_user_id)
		# Si on n'a rien trouvé
		else:
			return None
	else:
		return None

def welcome(request):
	logged_user = get_logged_user_from_request(request)
	if logged_user:
		return render(request, 'welcome.html', {'logged_user': logged_user})

	else:
		return redirect('/login')

def login(request):
	# Teste si le formulaire a été envoyé
	logged_user = get_logged_user_from_request(request)
	if logged_user:
		return render(request, 'welcome.html', {'logged_user': logged_user})
		
	else:
		if len(request.POST) > 0:
			form = LoginForm(request.POST)
			if form.is_valid():
				user_email = form.cleaned_data['email']
				logged_user = Person.objects.get(email=user_email)
				request.session['logged_user_id'] = logged_user.id
				return redirect('/welcome')
			else:
				return render(request, 'login.html', {'form': form})
		else:
			form = LoginForm()
			return render(request, 'login.html', {'form': form})
		
	

def register(request):
	if len(request.GET) > 0 and 'profileType' in request.GET:
		employeeForm = EmployeeProfileForm(prefix="st")
		studentForm = StudentProfileForm(prefix="em")
		if request.GET['profileType'] == 'student':
			studentForm = StudentProfileForm(request.GET, prefix="st")
			if sutudentForm.is_valid():
				studentForm.save()
				return redirect('/login')
		elif request.GET['profileType'] == 'employee':
			employeeForm = EmployeeProfileForm(request.GET, prefix="em")
			if employeeForm.is_valid():
				employeeForm.save()
				return redirect('/login')
		# Le formulaire n'est pas valide
		return render(request, 'user_profile.html', {'form': form})
	else:
		studentForm = StudentProfileForm(prefix="st")
		employeeForm = EmployeeProfileForm(prefix="em")
		return render(request, 'user_profile.html', {'studentForm': studentForm, 
													'employeeForm': employeeForm})
