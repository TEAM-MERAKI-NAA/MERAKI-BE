from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

load_dotenv(BASE_DIR / ".env")
SECRET_KEY = os.environ["SECRET_KEY"]

# ← this reads your .env into os.environ

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# settings.py
AUTH_USER_MODEL = 'authentication.CustomUser'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Add your frontend domain here
    "http://127.0.0.1:3000",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'ckeditor_uploader',
    'django_ckeditor_5',
    'drf_spectacular',
    'authentication',
    'corsheaders',
    'news',
    'guide',
    'rssparser',
    'currencyrates',
    'reminder',
    'userprofile',
    'budgettracker',
    'community',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
CORS_ALLOW_ALL_ORIGINS = True


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.postgresql",
        "NAME":     os.environ.get("POSTGRES_DB"),
        "USER":     os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST":     os.environ.get("POSTGRES_HOST"),
        "PORT":     os.environ.get("POSTGRES_PORT")
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field



from datetime import timedelta

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# settings.py (SMTP Backend)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Example for Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply.immigrationhub@gmail.com'
EMAIL_HOST_PASSWORD = 'mofn jjyb fvhg mxzw'

PASSWORD_RESET_TIMEOUT_DAYS = 1

#ck editor
#configuration file for ckeditor
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_MEDIA_USE_FULL_URL = True
customColorPalette = [
    {
        'color': 'hsl(4, 90%, 58%)',
        'label': 'Red'
    },
    {
        'color': 'hsl(340, 82%, 52%)',
        'label': 'Pink'
    },
    {
        'color': 'hsl(291, 64%, 42%)',
        'label': 'Purple'
    },
    {
        'color': 'hsl(262, 52%, 47%)',
        'label': 'Deep Purple'
    },
    {
        'color': 'hsl(231, 48%, 48%)',
        'label': 'Indigo'
    },
    {
        'color': 'hsl(207, 90%, 54%)',
        'label': 'Blue'
    },
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
        ],
    },
}

# Swagger Documentation Settings
SPECTACULAR_SETTINGS = {
    'TITLE': '🌟 ImmigrationHub API Documentation',
    'DESCRIPTION': '''
<div style="max-width: 1200px; margin: 0 auto;">
    <h1 style="text-align: center; color: #2c3e50; margin: 10px 0;">Welcome to ImmigrationHub API</h1>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 20px 0;">
        <div style="background: white; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <h3 style="color: #2c3e50; margin: 0 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid #3498db;">🚀 Key Features</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; font-size: 13px;">
                <div>🔐 <strong>Auth</strong></div>
                <div>👤 <strong>Profile</strong></div>
                <div>📰 <strong>RSS</strong></div>
                <div>📚 <strong>Guides</strong></div>
                <div>💱 <strong>Currency</strong></div>
                <div>⏰ <strong>Reminder</strong></div>
                <div>💰 <strong>Budget</strong></div>
                <div>👥 <strong>Community</strong></div>
            </div>
        </div>
        <div style="background: white; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <h3 style="color: #2c3e50; margin: 0 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid #e74c3c;">🔑 Authentication</h3>
            <div style="font-size: 13px;">
                <p style="margin: 0 0 8px 0;">JWT authentication required:</p>
                <code style="display: block; background: #f8f9fa; padding: 8px; border-radius: 4px; font-size: 12px;">Authorization: Bearer &lt;token&gt;</code>
            </div>
        </div>
        <div style="background: white; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="font-size: 13px;">
                <div style="margin-top: 12px; text-align: center; font-size: 12px; color: #7f8c8d;">
                    <hr style="border: none; border-top: 1px solid #eee; margin: 8px 0;">
                    © 2025 ImmigrationHub. All rights reserved.
                </div>
            </div>
        </div>
    </div>
</div>
''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
        'defaultModelsExpandDepth': 3,
        'defaultModelExpandDepth': 3,
        'defaultModelRendering': 'example',
        'displayRequestDuration': True,
        'docExpansion': 'none',
        'filter': True,
        'syntaxHighlight.theme': 'monokai',
        'tryItOutEnabled': True,
        'requestSnippetsEnabled': True,
        'layout': 'BaseLayout',
        'showExtensions': True,
        'showCommonExtensions': True,
        'tagsSorter': 'alpha',
        'operationsSorter': 'method',
        'syntaxHighlight': {
            'activated': True,
            'theme': 'monokai'
        },
        'displayRequestDuration': True,
        'filter': True,
        'requestSnippetsEnabled': True,
    },
    'SWAGGER_UI_DIST': '//unpkg.com/swagger-ui-dist@latest',
    'SWAGGER_UI_FAVICON_HREF': 'static/web/immigrationhub/favicon.ico',
    'REDOC_UI_DIST': '//cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js',
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
    'ENABLE_DJANGO_DEPLOY_CHECK': False,
    'DISABLE_ERRORS_AND_WARNINGS': True,
    'TAGS': [
        {
            'name': 'auth',
            'description': '🔐 **Authentication & Authorization**\n\nSecure endpoints for user authentication, registration, and token management.',
        },
        {
            'name': 'profile',
            'description': '👤 **User Profile Management**\n\nEndpoints for managing user profiles and preferences.',
        },
        {
            'name': 'rssparser',
            'description': '📰 **RSS Feed Integration**\n\nEndpoints for news and articles integration.',
        },
        {
            'name': 'guide',
            'description': '📚 **Immigration Guides**\n\nAccess to comprehensive immigration resources.',
        },
        {
            'name': 'currencyrates',
            'description': '💱 **Currency Rates**\n\nReal-time currency conversion endpoints.',
        },
        {
            'name': 'reminder',
            'description': '⏰ **Reminder System**\n\nEndpoints for managing notifications and reminders.',
        },
        {
            'name': 'budget',
            'description': '💰 **Budget Management**\n\nEndpoints for tracking expenses and financial planning.',
        },
        {
            'name': 'community',
            'description': '👥 **Community**\n\nEndpoints for user interaction and community features.',
        }
    ],
    'SECURITY': [
        {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': '''
# 🔒 JWT Authentication

Include your JWT token in the Authorization header:

```
Authorization: Bearer <your_token>
```

Example token format:
```
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
                '''
            }
        }
    ],
    'EXTENSIONS_INFO': {
        'x-logo': {
            'url': '/static/web/immigrationhub/logo.png',
            'backgroundColor': '#FFFFFF',
            'altText': 'ImmigrationHub Logo'
        }
    }
}

# Email Verification
FRONTEND_URL = 'http://localhost:3000'  # Change this to your frontend URL in production
