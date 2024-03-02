from django.urls import path

from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views


from .views import *


app_name = "gardencalendar"

from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.conf import settings



urlpatterns = [
     
    path('', views.home, name='home'),

    path('profile/<int:user_pk>/', views.user_calendar, name='user_profile'),

    path('login/', views.login_user, name='login'),

    path('logout', auth_views.LogoutView.as_view(), name='logout'),

    path('admin/', admin.site.urls),

    path('register/', views.register, name='register'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('authenticate/<str:authentication_link>/', views.authenticate_user, name='authenticate_user'),

    url(r'^fullcalendar/', TemplateView.as_view(template_name="fullcalendar.html"), name='fullcalendar'),

    
]

