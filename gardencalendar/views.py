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
import calendar
from datetime import date
import datetime

from .forms import *
from .models import *
from .forms import *


User = get_user_model()



def home(request):

     greeting="Lets make a garden!"

     return render(request, 'home.html',{

          '': greeting,})



def user_calendar(request, user_pk):

    user = get_object_or_404(User, pk=user_pk)

    def get_calendar_days_and_months():
            
            month_dictionary={
                        1:'January',
                        2:'February',
                        3:'March',
                        4:'April',
                        5:'May',
                        6:'June',
                        7:'July',
                        8:'August',
                        9:'September',
                        10:'October',
                        11:'November',
                        12:'December',
                    }

            day_dictionary={
                        0:'Monday',
                        1:'Tuesday',
                        2:'Wednesday',
                        3:'Thursday',
                        4:'Friday',
                        5:'Saturday',
                        6:'Sunday',
                    }
            
            today_data=date.today()

            year=today_data.year

            last_year=year-1

            month=today_data.month

            today=today_data.day

            day_of_week_int=today_data.weekday()

            day_of_week=day_dictionary[day_of_week_int]

            month_str=month_dictionary[month]

            blank_days=[]
            num_days_in_month=[]
            correlating_year=[]
            str_month=[]
            dates_list=[]
            dates_list_list=[]

            for i in range(1,4):
                for x in range(1,13):
                    month_info=calendar.monthrange(last_year,x)
                    blank_days.append(month_info[0])
                    num_days_in_month.append(month_info[1])
                    correlating_year.append(last_year)
                    str_month.append(month_dictionary[x])

                    dates_list.clear()

                    for days in range(1,month_info[1]):
                        dates=datetime.date(last_year,x,days)
                        dates_str=dates.strftime('%Y-%m-%d')
                        dates_list.append(dates_str)
                
                    dates_list_list.append(dates_list.copy())
    
                last_year+=1

            return(blank_days,num_days_in_month,correlating_year,str_month,dates_list_list)
                
    date_info=get_calendar_days_and_months()

    master_list=[]

    def find_todays_date_and_index():
        today_data=date.today()
        for index,sublist in enumerate(date_info[4]):
            if today_data.strftime('%Y-%m-%d') in sublist:
                print(f'TODAY IS FOUND {today_data} at {index}')
                return(index)
        return()

    def make_master_list():
        for item in range(0,len(date_info[0])):
                date_tuple=(date_info[0][item], date_info[1][item], date_info[2][item],date_info[3][item])
                master_list.append(date_tuple)

    make_master_list()

    todays_index=find_todays_date_and_index()

    today_is=date.today().strftime('%Y-%m-%d')


    todays_data=master_list[todays_index]

    num_blank_days=(date_info[0][todays_index])

    num_days_in_this_month=(date_info[1][todays_index])

    this_year_is=(date_info[2][todays_index])

    this_month_is=(date_info[3][todays_index])

    dates_in_this_month=(date_info[4][todays_index])      

    date_info=get_calendar_days_and_months()



    return render(request, 'user_calendar.html', {'user':user,
                                                  'this_year_is':this_year_is,
                                                  'this_month_is':this_month_is,
                                                  'today_is':today_is,
                                                  'num_blank_days_this_month':num_blank_days,
                                                  'num_days_in_this_month':num_days_in_this_month, 
                                                  'dates_in_this_month':dates_in_this_month,
                                                  'todays_index':todays_index,
                                                  'master_date_list':date_info,
                                                  })



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

            except:
                
                print("Sending email failed for some reason. :'(")
               

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
