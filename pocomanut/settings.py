# pocomanut/settings.py (VERSÃO PARA PYTHONANYWHERE)

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Configurações de Segurança ---
# No PythonAnywhere, você definirá a SECRET_KEY como uma variável de ambiente.
# Para desenvolvimento local, ele usa a chave padrão.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-sua-chave-local-aqui')

# O DEBUG será False no PythonAnywhere e True localmente.
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = []
# Adiciona automaticamente o host do PythonAnywhere quando em produção.
if 'PYTHONANYWHERE_DOMAIN' in os.environ:
    ALLOWED_HOSTS.append(os.environ['PYTHONANYWHERE_DOMAIN'])
else:
    # Permite hosts locais para desenvolvimento.
    ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])


# --- Aplicações Instaladas ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Nossos apps
    'core.apps.CoreConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'django_htmx',
    'crispy_forms',
    'crispy_bootstrap5',
]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise é útil e compatível com PythonAnywhere, pode manter.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'pocomanut.urls'

# --- Templates e Crispy Forms ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

WSGI_APPLICATION = 'pocomanut.wsgi.application'


# --- Banco de Dados ---
# Manteremos a configuração do MySQL para desenvolvimento local.
# No PythonAnywhere, você irá sobrescrever isso na interface web deles.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pocomanut_db',
        'USER': 'root',
        'PASSWORD': 'sua_senha_mysql_local',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# --- Validadores de Senha ---
AUTH_PASSWORD_VALIDATORS = [ ... ] # (Mantenha como está)

# --- Internacionalização ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# --- Arquivos Estáticos e de Mídia (Configuração Universal) ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- Configurações Padrão ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
