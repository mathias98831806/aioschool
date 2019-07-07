# -*- coding: utf-8 -*-

from django.db import models

class Person(models.Model):
	registration_number = models.CharField(max_length=10)
	last_name = models.CharField(max_length=30)
	first_name = models.CharField(max_length=30)
	birth_date = models.DateField()
	email = models.EmailField()
	home_phone_number = models.CharField(max_length=20)
	cellphone_number = models.CharField(max_length=20)
	# Dans un cas réel, nous ne devrions pas stocker le mot de passe en clair.
	password = models.CharField(max_length=32)
	friends = models.ManyToManyField('self')
	faculty = models.ForeignKey('Faculty', on_delete='cascade')

	def __str__(self):
		return self.first_name + " " + self.last_name

class Message(models.Model):
	author = models.ForeignKey('Person', on_delete='cascade')
	content = models.TextField()
	publication_date = models.DateField()

	#Définition des champs
	def __str__(self):
		if len(self.content) > 20:
			return self.conten[:19] + "..."
		else:
			return self.content


class Faculty(models.Model):
	name = models.CharField(max_length=30)
	color = models.CharField(max_length=6)
	# Définition des champs
	def __str__(self):
		return self.name

class Campus(models.Model):
	name = models.CharField(max_length=30)
	address = models.CharField(max_length=60)

	def __str__(self):
		return self.name

class Job(models.Model):
	title = models.CharField(max_length=30)

	def __str__(self):
		return self.title

class Cursus(models.Model):
	title = models.CharField(max_length=30)

	def __str__(self):
		return self.title


class Employee(Person):
	office = models.CharField(max_length=30)
	campus = models.ForeignKey('Campus', on_delete='cascade')
	job = models.ForeignKey('Job',on_delete='cascade')

class Student(Person):
	cursus = models.ForeignKey('Cursus', on_delete='cascade')
	year = models.IntegerField()