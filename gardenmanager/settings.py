import os
from pathlib import Path
import dj_database_url
from pathlib import Path
import boto3

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# N O T E  :Create your key within your environment variable!!
SECRET_KEY = os.environ.get('DJANGO_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



"""
If you want to host on Heroku unquote this. I just went ahead and prepared it for deployment since I'm already here.


IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ

# SECURITY WARNING: don't run with debug turned on in production!
if not IS_HEROKU_APP:

    print("not a heroku app")
    DEBUG = True


if IS_HEROKU_APP:

    print("heroku app true?")
    DEBUG=True

    print(f"debug status == {DEBUG}")
    ALLOWED_HOSTS = ["*"]
   
   # SSL SETTINGS for Django Projects
    
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True


else:
    ALLOWED_HOSTS = []

"""


"""
H O O K I N G     U P    S-3    B E L O W
"""

############## A M A Z O N   M E D I A   P A T H S###################
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')            #
AWS_SECRET_ACCESS_KEY =os.environ.get('AWS_SECRET_ACCESS_KEY')     #
AWS_STORAGE_BUCKET_NAME =os.environ.get('S3_BUCKET')               #
DJANGO_STATIC = True                                               #
DJANGO_STATIC_FILE_PROXY = 'cloudfront.file_proxy'                 #

CLOUDFRONT_PUB_KEY=os.getenv('CLOUDFRONT_PUB')                     #
CLOUDFRONT_SECRET=os.getenv('CLOUDFRONT_SECRET')                   #
AWS_DEFAULT_ACL='public-read'

CLOUDFRONT_URL = 'https://d17usxoyp786nd.cloudfront.net/'          #
MEDIA_URL = CLOUDFRONT_URL
AWS_S3_CUSTOM_DOMAIN = CLOUDFRONT_URL   

DJANGO_STATIC = True
DJANGO_STATIC_FILE_PROXY = 'cloudfront.file_proxy'
COMPRESS_ENABLED= True                                             #
COMPRESS_URL= CLOUDFRONT_URL                                       #

############### E N D   O F    A M A Z O N   S E T T I N G S ######


INSTALLED_APPS = [
    'djangobower',
    'schedule',
    'gardencalendar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Installing whitenoise middleware to serve static files in production
    "whitenoise.middleware.WhiteNoiseMiddleware",

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gardenmanager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #Added my path to the templates here
        'DIRS': [os.path.join(BASE_DIR,'gardencalendar', 'templates','gardencalendar')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gardenmanager.wsgi.application'

"""
This is how to set up the database if you want to use Heroku.


if IS_HEROKU_APP:

    print("is a herokue app is True")


    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        ),
    }

    
else:

    DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',#<- Defines the Mysql backend in django.
        'NAME': SCHEMA_NAME, #<--------- Name of schema in MySQL 
        'USER': DB_USER,     #<--------- User Name 
        'PASSWORD': DB_PASSWORD,  #<- Password
        'HOST': '127.0.0.1',  #<---------Stays 127.0.0.1 Unless you host your Mysql DB on a server.
        'PORT': '3306', #<----------------Port 3306 is the standard port for mysql
        'OPTIONS': {  
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
        }      
        
    }  
} 

"""



"""
This is a default sqlite database. You may want to swap to it for troubleshooting.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""

#AUTH USER MODEL is needed because we are going to edit the base user model from the start.
AUTH_USER_MODEL = 'gardencalendar.User_Profile'



#Now I'm defining the credentials for the database here. You will need to create them in your environment.
#SCHEMA_NAME= os.environ.get('SCHEMA_NAME')
SCHEMA_NAME='garden_buddy'
DB_USER= os.environ.get('DB_USER')
DB_PASSWORD= os.environ.get('DB_PASSWORD')

DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',#<- Defines the Mysql backend in django.
        'NAME': SCHEMA_NAME, #<--------- Name of schema in MySQL 
        'USER': DB_USER,     #<--------- User Name 
        'PASSWORD': DB_PASSWORD,  #<- Password
        'HOST': '127.0.0.1',  #<---------Stays 127.0.0.1 Unless you host your Mysql DB on a server.
        'PORT': '3306', #<----------------Port 3306 is the standard port for mysql
        'OPTIONS': {  
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
        }      
        
    }  
} 


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',

]




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATICFILES_FINDERS = [

    'django.contrib.staticfiles.finders.FileSystemFinder',

    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'Djangobower.finders.BowerFinder',

]

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'gardencalendar', 'static','gardencalendar')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'gardencalendar')


BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR,'components')

BOWER_INSTALLED_APPS = (
    'jquery',
    'jquery-ui',
    'bootstrap'
)

print(f"Bower components root--->  {BOWER_COMPONENTS_ROOT}")

STORAGES = {
    # Enable WhiteNoise's GZip and Brotli compression of static assets:
    # https://whitenoise.readthedocs.io/en/latest/django.html#add-compression-and-caching-support
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



#How to set  up email (optional)

EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER=os.environ.get('email')
EMAIL_HOST_PASSWORD=os.environ.get('mailpass')
EMAIL_USE_TLS= True
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'

