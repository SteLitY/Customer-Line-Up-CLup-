from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i$9&j7#s)+xpi&kx#i5=bpo@sa#da@dfteoy=pmf$%z-2zi^ou'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'posts',
<<<<<<< HEAD
    # 'channels',
=======
    'channels',
>>>>>>> 065e83a003aa33fc1302fc4a32f2ec7172a9da0b
    # 'notifier',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
]

# CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'clup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/posts')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'clup.wsgi.application'
# ASGI_APPLICATION = 'clup.routing.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

def get_ssl_cert():
    current_path = Path(__file__).resolve().parent.parent
    return str(current_path / 'BaltimoreCyberTrustRoot.crt.pem')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'clup',
        'USER': 'admin499',
        'PASSWORD': 'CS499class',
        'HOST': 'lineup499.mysql.database.azure.com',
        'PORT': '3306',
        'OPTIONS' : {
        'ssl' : get_ssl_cert()
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

#Static files are contained here
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django_ses.SESBackend'

AWS_SES_REGION_NAME = 'us-east-1' #(ex: us-east-2)
AWS_ACCESS_KEY_ID = '' #cannot be posted on github. this is used for customer forgot password - David
AWS_SECRET_ACCESS_KEY = '' #cannot be posted on github. this is used for customer forgot password - David
AWS_SES_REGION_ENDPOINT ='email.us-east-1.amazonaws.com' #(ex: email.us-east-2.amazonaws.com)

# Channels config
#Tells us which backend needs to be used for 

<<<<<<< HEAD
# CHANNEL_LAYERS  = {
#     "default": {
#         # One of our dependencies
#         "BACKEND": "channels_redis.core.RedisChannelLayer", 
#         "CONFIG": {"hosts": [("localhost", 6379)],
#         }, 
#     },
# }
=======
CHANNEL_LAYERS  = {
    "default": {
        # One of our dependencies
        "BACKEND": "channels_redis.core.RedisChannelLayer", 
        "CONFIG": {"hosts": [("localhost", 6379)],
        }, 
    },
}
>>>>>>> 065e83a003aa33fc1302fc4a32f2ec7172a9da0b

# # Activate Django-Heroku.
# django_heroku.settings(locals())
# import dj_database_url
# DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)