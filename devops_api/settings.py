"""
Django settings for devops_api project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j3y1w*--r&+3bjstq#w)fbx9o7_jmewtg5nf5zodo-q0ed1+kz'
SALT_KEY = "uW_Ab2r93qN3auGB"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # 支持跨域
    'rest_framework',
    'apps.account',
    'apps.order'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 支持跨域
    'django.middleware.common.CommonMiddleware',  # 支持跨域
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'devops_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
AUTH_USER_MODEL = "account.User"

WSGI_APPLICATION = 'devops_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'devops_api',
#         'USER': 'django',
#         'PASSWORD': '123456',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 支持跨域 +++++
# 跨域增加忽略
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = ()

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

# 支持跨域 ----


#下面就是logging的配置
LOGGING = {
    'version': 1,  # 指明dictConnfig的版本，目前就只有一个版本
    'disable_existing_loggers': False,  # 表示是否禁用所有的已经存在的日志配置
    'formatters': {  # 格式器
        'verbose': {  # 详细
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'standard': {  # 标准
            'format': '[%(asctime)s] [%(levelname)s] %(message)s'
        },
    },
    # handlers：用来定义具体处理日志的方式，可以定义多种，"default"就是默认方式，"console"就是打印到控制台方式。file是写入到文件的方式，注意使用的class不同
    'handlers': { # 处理器，在这里定义了两个个处理器INFO
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',   # 文件重定向的配置，将打印到控制台的信息都重定向出去 python manage.py runserver >> /home/aea/log/test.log
            # 'stream': open('/home/aea/log/test.log','a'),  #虽然成功了，但是并没有将所有内容全部写入文件，目前还不清楚为什么
            'formatter': 'standard'   # 制定输出的格式，注意 在上面的formatters配置里面选择一个，否则会报错
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "log",'devops_api.log'),  #这是将普通日志写入到日志文件中的方法，
            'formatter': 'standard'
        },
        'default': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "log",'devops_api.log'),     #日志输出文件
            'maxBytes': 1024*1024*5,                  #文件大小
            'backupCount': 5,                         #备份份数
            'formatter':'standard',                   #使用哪种formatters日志格式
        },
        # 上面两种写入日志的方法是有区别的，前者是将控制台下输出的内容全部写入到文件中，这样做的好处就是我们在views代码中的所有print也会写在对应的位置
        # 第二种方法就是将系统内定的内容写入到文件，具体就是请求的地址、错误信息等，小伙伴也可以都使用一下然后查看两个文件的异同。
    },
    'loggers': {  # log记录器，配置之后就会对应的输出日志
        # django 表示就是django本身默认的控制台输出，就是原本在控制台里面输出的内容，在这里的handlers里的file表示写入到上面配置的file-/home/aea/log/jwt_test.log文件里面
        # 在这里的handlers里的console表示写入到上面配置的console-/home/aea/log/test.log文件里面
        'django': {
            'handlers': ['console','file'],
            # 这里直接输出到控制台只是请求的路由等系统console，当使用重定向之后会把所有内容输出到log日志
            'level': 'INFO',
            'propagate': True,
        },
        'django.request ':{
            'handlers': ['console','file'],
            'level': 'WARNING',  # 配合上面的将警告log写入到另外一个文件
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file'], # 指定file handler处理器，表示只写入到文件
            'level':'INFO',
            'propagate': True,
        },
    },
}