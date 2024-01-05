from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

#These last two are needed for serving files locally. So basically if you dont want to use S3 then we can just serve the files from your local computer.
from django.conf import settings
from django.conf.urls.static import static


"""
Since we are in our base urls file, I included the urls file from our app and the built in django password handelers. 

accounts, password reset, ect.
"""

urlpatterns = [

    path("", include("gardencalendar.urls")),


    path('admin/', admin.site.urls),

    

    path('accounts/', include('django.contrib.auth.urls')),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('logout', auth_views.LogoutView.as_view(), name='logout'),


    

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

