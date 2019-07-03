"""
Django settings for ujuModels project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import pathlib

BASE_DIR = pathlib.Path(".").parent.resolve()
print(BASE_DIR)

SECRET_KEY = 'f_a0&tfpu!0)q3+c-v)z(65ef%=0!^k@9%fm2k$*4age+vx&c$'

INSTALLED_APPS = [
    'ujuModels.uju',
]

TIME_ZONE = 'Asia/Shanghai'
MONGO_URL = 'mongodb://127.0.0.1:27017'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spider',  # 你的数据库名称
        'USER': 'root',  # 你的数据库用户名
        'PASSWORD': '123456',  # 你的数据库密码
        'HOST': '127.0.0.1',  # 你的数据库主机，留空默认为localhost
        'PORT': '3306',  # 你的数据库端口
    }
}
BASE_DIR.joinpath("logs").mkdir(exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "thread": {
            "format": "%(asctime)s [%(threadName)s:%(thread)d] [%(filename)s:%(lineno)d] [%(levelname)s]- %(message)s"
        },
        "standard": {
            "format": "%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s]- %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR.joinpath("logs/default.log"),
            "formatter": "standard",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "default": {"handlers": ["default"], "level": "DEBUG", "propagate": True},
        "console": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
        #  'django.db.backends': {
        #  'handlers': ['console'],
        #  'propagate': True,
        #  'level': 'DEBUG',
        #  },
    },
}
