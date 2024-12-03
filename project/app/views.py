from django.shortcuts import render,redirect
from .models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
import re
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings



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
            return render(req, 'Client/clientreg.html')
        try:
            data=Client.objects.create(username=name,Email=email,phonenumber=phonenumber,location=location,password=password)
            data.save()
            subject = 'Registration details '
            message = 'ur account uname {}  and password {}'.format(name,password)
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list,fail_silently=False)  
            return redirect(login)
        except:
            messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'Client/clientreg.html')

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
        return render(req,'Client/clienthome.html')
    
def advocatehome(req):
    if 'advocate' in req.session:
        return render(req,'advocatehome.html')
    




##profile of user
def clientprofile(req):
    if 'user' in req.session:
        return render(req,'Client/clientprofile.html',{'data':get_client(req)})
    else:
        return redirect(login)
    

###profile update
def updateclientprofile(req):
    if 'user' in req.session:
        try:
            data = Client.objects.get(Email=req.session['user'])
        except Client.DoesNotExist:
            return redirect(login)

        if req.method == 'POST':
            name = req.POST['username']
            phonenumber = req.POST['phonenumber']
            location = req.POST['location']
            if not re.match(r'^[789]\d{9}$', phonenumber):
                return render(req, 'updateclientprofile.html', {
                    'data': data,
                    'error_message': 'Invalid phone number'
                })
            Client.objects.filter(Email=req.session['user']).update(username=name, phonenumber=phonenumber, location=location)
            return redirect(clientprofile)
        return render(req, 'Client/updateclientprofile.html', {'data': data})

    else:

        return redirect(login)
    




##profile of advocate
def advocateprofile(req):
    if 'advocate' in req.session:
        return render(req,'advocateprofile.html',{'data':get_advocate(req)})
    else:
        return redirect(login)
    

###profile update
def updateadvocateprofile(req):
    if 'advocate' in req.session:
        try:
            data = Advocate.objects.get(Email=req.session['advocate'])
        except Advocate.DoesNotExist:
            return redirect(login)

        if req.method == 'POST':
            name = req.POST['name']
            phonenumber = req.POST['phonenumber']
            location = req.POST['location']
            if not re.match(r'^[789]\d{9}$', phonenumber):
                return render(req, 'updateadvocateprofile.html', {
                    'data': data,
                    'error_message': 'Invalid phone number'
                })
            Advocate.objects.filter(Email=req.session['advocate']).update(name=name, phonenumber=phonenumber, location=location)
            return redirect(advocateprofile)
        return render(req, 'updateadvocateprofile.html', {'data': data})

    else:

        return redirect(login)
    




def viewadvocates(req):
    data=Advocate.objects.all()
    return render(req,'Client/viewadvocates.html', {'data':data})

def viewclients(req):
    data=Client.objects.all()
    return render(req,'viewclients.html', {'data':data})






def filecase(req,id):
    if req.method == 'POST':
        subject = req.POST['subject']
        description = req.POST['description'] 
        if 'user' in req.session:
            client = Client.objects.get(pk=id)
            advocate = Advocate.objects.get(pk=id)
            case = Case.objects.create(
            client=client,
            advocate=advocate,
            subject=subject,
            description=description
        )
        case.save()
        return redirect(clienthome)  
    
    else:
        advocates = Advocate.objects.all()
        return render(req, 'Client/filecase.html', {'advocates': advocates})




    


def viewcases(req):
    if req.method == 'POST':
        advocate_id = req.POST['advocate_id']
        advocate = Advocate.objects.get(id=advocate_id)
        
        cases = Case.objects.filter(advocate=advocate)
        
        return render(req, 'viewcases.html', {'cases': cases})
    else:
        advocates = Advocate.objects.all()
        return render(req, 'viewcases.html', {'advocates': advocates})
    

def bookings(req):
        cases = Case.objects.all()
        return render(req,'Client/bookings.html',{'cases':cases})



def bookinghistory(req):
        cases = Case.objects.all()
        return render(req,'bookinghistory.html',{'cases':cases})
