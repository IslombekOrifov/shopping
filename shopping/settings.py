

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-znoqu+(!48o+&x7##!ls$x7os49q-7jsais+z6@=5zgbdyqwv0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
]

CSRF_TRUSTED_ORIGINS = ["https://ecom.pythonanywhere.com"]

# Application definition

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',

    'adminlte3',
    'adminlte3_theme',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'carts.apps.CartsConfig',
    'company.apps.CompanyConfig',
    'delivery.apps.DeliveryConfig',
    'discounts.apps.DiscountsConfig',
    'general.apps.GeneralConfig',
    'orders.apps.OrdersConfig',
    'products.apps.ProductsConfig',
    'wishlists.apps.WishlistsConfig',

    # payment
    'payment.apps.PaymentConfig',

    'rest_framework',
    'payme',

    'widget_tweaks',
    'colorfield',
    'ckeditor',
    # 'debug_toolbar',

]

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#     ]
# }

MIDDLEWARE = [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'carts.custom_middlware.CartItemSessionDeleteMiddleware',
]



PAYME: dict = {
    'PAYME_ID': '5e730e8e0b852a417aa49ceb',
    'PAYME_KEY': '#MWnwHNYATJo%W@XvO5nISiY&mG7PEuzDX18',
    'PAYME_URL': 'https://checkout.test.paycom.uz/api/',
    'PAYME_CALL_BACK_URL': 'https://582f-89-236-254-251.eu.ngrok.io', # merchant api callback url
    'PAYME_MIN_AMOUNT': 500, # integer field
    'PAYME_ACCOUNT': 'order_id',
}




# PAYME_RETURN = 'https://fbd9-89-236-254-251.eu.ngrok.io/payme/paycom'



#   debug_toolbar

# INTERNAL_IPS = [
#     # ...
#     "127.0.0.1",
#     # ...
# ]
# # This example is unlikely to be appropriate for your project.
# DEBUG_TOOLBAR_CONFIG = {
#     # Toolbar options
#     'RESULTS_CACHE_SIZE': 3,
#     'SHOW_COLLAPSED': True,
#     # Panel options
#     'SQL_WARNING_THRESHOLD': 100,   # milliseconds
# }

ROOT_URLCONF = 'shopping.urls'

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
                'general.context_processors.index',
                'carts.context_processors.cart',
                'accounts.context_processors.log_form_for_base',
            ],
        },
    },
]

WSGI_APPLICATION = 'shopping.wsgi.application'



# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', 
#         'NAME': 'shoppingdjango$default',
#         'USER': 'shoppingdjango',
#         'PASSWORD': 'admin12345',
#         'HOST': 'shoppingdjango.mysql.pythonanywhere-services.com',   # Or an IP Address that your DB is hosted on
#         # 'PORT': '3306',
#     }
# }


# authentication Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'accounts.authentications.EmailAuthBackend',
]


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Auth model
AUTH_USER_MODEL = 'accounts.CustomUser'


# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'islombekorifov0199@gmail.com'
EMAIL_HOST_USER = 'islombekorifov0199@gmail.com'
EMAIL_HOST_PASSWORD = 'bpsuzmrbmtfslkma'
EMAIL_PORT = 587
EMAIL_USE_TLS = True



# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


CART_SESSION_ID = 'cart'
CART_SESSION_LIFE_TIME = 900

WISHLIST_SESSION_ID = 'wishlist'

CURRENCY_SESSION_ID = 'currency'
CURRENCY_DEFAULT = 'usd'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [BASE_DIR / 'static_all']


# Media Files (image, files, videos)

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# ckeditor settings 

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = 'common.utils.get_ckeditor_upload_path'

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

LOGIN_URL = 'accounts:login'
LOGOUT_URL = 'accounts:logout'


DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_SCALE = 1
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# branintree
import braintree

BRAINTREE_MERCHANT_ID = 'j9sy46p8ffmz46ht'
BRAINTREE_PUBLIC_KEY = '87s8tqhy2r9kxysp'
BRAINTREE_PRIVATE_KEY = 'ab5ac5973b71fc664ce66f46648f36cb'


BRAINTREE_CONF = braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    merchant_id=BRAINTREE_MERCHANT_ID,
    public_key=BRAINTREE_PUBLIC_KEY,
    private_key=BRAINTREE_PRIVATE_KEY
)