# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt, datetime
now = datetime.datetime.now()
today = now.date()

class userManager(models.Manager):
	def userValidate(self,postData):
		response = {
			'status': True
		}
		errors = []
		if len(postData['name']) == 0 or len(postData['username']) == 0 or len(postData['password1']) == 0 or len(postData['password2']) == 0:
			errors.append("All fields are required")
		if len(postData['name']) < 3:
			errors.append("Name must be at least 3 characters")
		if len(postData['username']) < 3:
			errors.append("Username must be at least 3 characters")
		if len(postData['password1']) < 8:
			errors.append("Password must be at least 8 characters")
		if postData['password1'] != postData['password2']:
			errors.append("Password confirmation must match")
		response['username'] = user.objects.filter(username=postData['username'])
		if len(response['username']) > 0:
			errors.append("Username already taken")
		if len(errors) > 0:
			response['status'] = False
		else:
			hashedPw = bcrypt.hashpw(postData['password1'].encode(), bcrypt.gensalt())
			response['user'] = user.objects.create(name=postData['name'],username=postData['username'],password=hashedPw)
		response['errors'] = errors
		return response
	def loginValidate(self,postData):
		response = {
			'status': True,
			'login': user.objects.filter(username=postData['username'])
		}
		if len(response['login']) == 1 and bcrypt.checkpw(postData['password1'].encode(), response['login'][0].password.encode()):
			response['user'] = response['login'][0]
		else:
			response['status'] = False
		return response

class tripManager(models.Manager):
	def tripValidator(request,postData):
		response = {
			'status': True
		}
		errors = []
		if len(postData['dest']) == 0 or len(postData['desc']) == 0 or len(postData['start']) == 0 or len(postData['end']) == 0:
			errors.append("All fields are required")
		started_by = user.objects.get(id=postData['userID'])
		if len(postData['start']) > 0 and len(postData['end']) > 0:
			start = datetime.date(*[int(i) for i in postData['start'].split("-")])
			end = datetime.date(*[int(i) for i in postData['end'].split("-")])
			if start <= today:
				errors.append("Trip start date must be after today")
			if start > end:
				errors.append("Trip end date must be after the start date")
		if len(errors) > 0:
			response['status'] = False
		else:
			response['trip'] = trip.objects.create(dest=postData['dest'],desc=postData['desc'],start=start,end=end,started_by=started_by)
			response['travel'] = response['trip'].travelers.add(started_by)
		response['errors'] = errors
		return response


class user(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = userManager()

class trip(models.Model):
	dest = models.CharField(max_length=255)
	desc = models.CharField(max_length=255)
	start = models.DateTimeField()
	end = models.DateTimeField()
	started_by = models.ForeignKey(user,related_name="started")
	travelers = models.ManyToManyField(user, related_name="going_on")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = tripManager()