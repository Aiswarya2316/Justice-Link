from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Advocate, Booking
from django.contrib.auth.decorators import login_required
from .forms import BookingForm  # Create a BookingForm

def advocate_list(request):
    advocates = Advocate.objects.all()
    return render(request, 'advocate_list.html', {'advocates': advocates})

@login_required
def book_advocate(request, advocate_id):
    advocate = Advocate.objects.get(id=advocate_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.advocate = advocate
            booking.client = request.user
            booking.save()
            return redirect('advocate_list')
    else:
        form = BookingForm()
    return render(request, 'book_advocate.html', {'form': form, 'advocate': advocate})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('advocate_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

