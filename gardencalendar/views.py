from django.shortcuts import render,redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from collections import OrderedDict
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse

from .forms import AuthenticationForm
from .models import *
from .forms import *


User = get_user_model()



def home(request):

     greeting="Lets make a garden!"

     return render(request, 'home.html',{

          '': greeting,})



def user_calendar(request, user_pk):

    user = get_object_or_404(User, pk=user_pk)

    user_data={
         'name':'Perry',
         'plants':['carrots','broccoli','potatos']

    }

    return render(request, 'user_calendar.html', {'user_data': user_data, 'user':user})



def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(request, username=username, password=password)



        if user is not None:

            login(request, user)

            return redirect('gardencalendar:home')

        else:

            error_message = "Invalid credentials"

            return render(request, 'Error.html', {'error_message': error_message})

    else:

        return render(request, 'login.html')



def register(request):

    """

    This creates a user model based on the User_Profile model which is the base User model extended.

    """

    if request.method == 'POST':

        form = Registration(request.POST)

        if form.is_valid():

            user_data = form.cleaned_data

            new_user = User_Profile.objects.create_user(

                username=user_data['username'],

                email=user_data['email'],

                password=user_data['password'],

            )

            try:

                registration_link = request.build_absolute_uri(

                    reverse('authenticate_user', args=[str(new_user.authentication_link)])

                )

                print(f"\n\nyour registration link is --->  {registration_link} <---\n\n")

                

                send_mail(

                    f"Welcome {new_user.username}",

                    f"Welcome to the Garden buddy!!\n\n Here is how to get registered:\n\nBelow is your authentication key.\n\ncopy this:\n\n{new_user.authentication_key} \n\nClick the link below to complete your registration:\n\n{registration_link}",

                    "admin@ilovecookbooks.org",

                    [new_user.email],

                    fail_silently=False,

                )

            except:
               
               registration_link = request.build_absolute_uri(

                    reverse('gardencalendar:authenticate_user', args=[str(new_user.authentication_link)])

                )

               print(f"\n\nyour registration link is --->  {registration_link} <---\n\n")

                

               send_mail(

                    f"Welcome {new_user.username}",

                    f"Welcome to the Garden buddy!!\n\n Here is how to get registered:\n\nBelow is your authentication key.\n\ncopy this:\n\n{new_user.authentication_key} \n\nClick the link below to complete your registration:\n\n{registration_link}",

                    "admin@ilovecookbooks.org",

                    [new_user.email],

                    fail_silently=False,

                )

            return redirect('gardencalendar:login')

    else:

        form = Registration()

    return render(request, 'registration.html', {'form': form})





def authenticate_user(request, authentication_link):

    user_profile = get_object_or_404(User_Profile, authentication_link=authentication_link)



    if request.method == 'POST':

        form = AuthenticationForm(request.POST)

        if form.is_valid():

            authentication_key = form.cleaned_data['authentication_key']



            # Check if the provided authentication key matches the one in the user profile

            if authentication_key == user_profile.authentication_key:

                user_profile.is_verified = 'Y'

                user_profile.save()

                return render(request, 'auth_success.html', {'user_profile': user_profile})



    else:

        form = AuthenticationForm()



    return render(request, 'auth.html', {'form': form, 'user_profile': user_profile})
