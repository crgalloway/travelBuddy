# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
	return redirect('/main')

def main(request):
	context = {}
	if 'activeUser' in request.session:
		context['userName'] = user.objects.get(id=request.session['activeUser']).name
	return render(request, 'travelBuddy_app/main.html',context)

def register(request):
	response = user.objects.userValidate(request.POST)
	if len(response['errors']) < 1:
		request.session['activeUser'] = response['user'].id
		return redirect('/travels')
	else:
		for error in response['errors']:
			messages.error(request, error)
		return redirect('/main')

def login(request):
	response = user.objects.loginValidate(request.POST)
	if response['status']:
		request.session['activeUser'] = response['user'].id
		return redirect('/travels')
	else:
		messages.warning(request,"Invalid email/password combination")
		return redirect('/main')

def travels(request):
	if not 'activeUser' in request.session:
		messages.error(request,"You must be logged in")
		return redirect('/main')
	context = {
		'activeName': user.objects.get(id=request.session['activeUser']).name,
		'yourPlans': trip.objects.all().filter(travelers=request.session['activeUser']),
		'otherPlans': trip.objects.all().exclude(travelers=request.session['activeUser'])
	}
	return render(request, 'travelBuddy_app/travels.html', context)

def destination(request,number):
	if not 'activeUser' in request.session:
		messages.error(request,"You must be logged in")
		return redirect('/main')
	context = {
		'trip': trip.objects.get(id=number),
		'travelers': user.objects.filter(going_on=trip.objects.get(id=number)).exclude(started=trip.objects.get(id=number))
	}
	return render(request, 'travelBuddy_app/destination.html', context)

def add(request):
	if not 'activeUser' in request.session:
		messages.error(request,"You must be logged in")
		return redirect('/main')
	return render(request, 'travelBuddy_app/add.html')

def logout(request):
	request.session.clear()
	return redirect('/main')

def join(request,number):
	joiner = user.objects.get(id=request.session['activeUser'])
	trip.objects.get(id=number).travelers.add(joiner)
	return redirect('/travels')

def addTrip(request):
	response = trip.objects.tripValidator(request.POST)
	if response['status']:
		return redirect('/travels')
	else:
		for error in response['errors']:
			messages.error(request, error)
		return redirect('/travels/add')