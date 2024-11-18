from django.shortcuts import render,redirect
from .models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
import re


# Create your views here.

def get_client(req):
    data=Client.objects.get(Email=req.session['user'])
    return data


def get_advocate(req):
    data=Advocate.objects.get(Email=req.session['advocate'])
    return data

def login(req):
    if 'user' in req.session:
        return redirect(clienthome)
    if 'advocate' in req.session:
        return redirect(advocatehome)
    

    if req.method=='POST':
        Email=req.POST['Email']
        password=req.POST['password']
        try:
            data=Client.objects.get(Email=Email,password=password)
            req.session['user']=data.Email
            return redirect(clienthome)
        except Client.DoesNotExist:
            data=Advocate.objects.get(Email=Email,password=password)
            req.session['advocate']=data.Email

            return redirect(advocatehome)
    else:
        messages.warning(req, "INVALID INPUT !")
    return render(req,'login.html')
    

def logout(req):
    if 'user' in req.session:
        del req.session['user']
    if 'advocate' in req.session:
        del req.session['advocate']
    return redirect(login)


def clientreg(req):

    if req.method=='POST':
        name=req.POST['username']
        email=req.POST['Email']
        phonenumber=req.POST['phonenumber']
        location=req.POST['location']
        password=req.POST['password']
         # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.warning(req, "Invalid email format, please enter a valid email.")
            return render(req, 'clientreg.html')

        # Validate phone number (assuming 10-digit numeric format)
        if not re.match(r'^\d{10}$', phonenumber):
            messages.warning(req, "Invalid phone number. Please enter a valid 10-digit phone number.")
            return render(req, 'clientreg.html')
        try:
            data=Client.objects.create(username=name,Email=email,phonenumber=phonenumber,location=location,password=password)
            data.save()
            return redirect(login)
        except:
            messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'clientreg.html')

def advocatereg(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['Email']
        phonenumber=req.POST['phonenumber']
        location=req.POST['location']
        password=req.POST['password']
        bio=req.POST['bio']
        try:
            data=Advocate.objects.create(name=name,Email=email,phonenumber=phonenumber,location=location,password=password,bio=bio)
            data.save()
            return redirect(login)
        except:
            messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'advocatereg.html')


def clienthome(req):
    if 'user' in req.session:
        return render(req,'clienthome.html')
    
def advocatehome(req):
    if 'advocate' in req.session:
        return render(req,'advocatehome.html')
    
