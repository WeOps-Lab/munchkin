# settings.py
import os

SECRET_KEY = os.getenv("SECRET_KEY")
APP_CODE = os.getenv("APP_CODE")
# 使用时区
USE_TZ = True
# 时区设置
TIME_ZONE = "Asia/Shanghai"
# 语言设置
LANGUAGE_CODE = "zh-Hans"
# 国际化设置
USE_I18N = True
# 本地化设置
USE_L10N = True

# 定义支持的语言
LANGUAGES = (
    ("en", "English"),
    ("zh-Hans", "简体中文"),
)
HTTP_LANGUAGE = "HTTP_ACCEPT_LANGUAGE"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
SESSION_COOKIE_NAME = f"{APP_CODE}_sessionid"
# CSRF配置
CSRF_COOKIE_NAME = f"{APP_CODE}_csrftoken"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 指定翻译文件的目录
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    # "version_log",
    "apps.core",
)
ASGI_APPLICATION = "asgi.application"

CELERY_IMPORTS = ()

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # 跨域检测中间件， 默认关闭
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # django国际化中间件
    "django.middleware.locale.LocaleMiddleware",
    "apps.core.middlewares.app_exception_middleware.AppExceptionMiddleware",
    "apps.core.middlewares.drf_middleware.DisableCSRFMiddleware",
    # 'apps.core.middlewares.keycloak_auth_middleware.KeyCloakAuthMiddleware',
)

ROOT_URLCONF = "urls"

DEBUG = os.getenv("DEBUG", "0") == "1"
if DEBUG:
    INSTALLED_APPS += (
        "corsheaders",
        "rest_framework_swagger",
        "drf_yasg",
    )  # noqa
    # 该跨域中间件需要放在前面
    MIDDLEWARE = ("corsheaders.middleware.CorsMiddleware",) + MIDDLEWARE  # noqa
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True

# 缓存配置
REDIS_CACHE_URL = os.environ.get("REDIS_CACHE_URL", "")

CACHES = {
    "db": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
    },
    "login_db": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "account_cache",
    },
    "dummy": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
    "locmem": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    "redis": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_CACHE_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
    },
}
CACHES["default"] = CACHES["redis"]

# 模板页面配置
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (os.path.join(BASE_DIR, "templates"),),
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.web_env.custom_settings",
            ],
        },
    }
]

# 数据库配置
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),  # 替换为你的数据库名称
        "USER": os.getenv("DB_USER"),  # 替换为你的数据库用户
        "PASSWORD": os.getenv("DB_PASSWORD"),  # 替换为你的数据库密码
        "HOST": os.getenv("DB_HOST"),  # 通常是 'localhost' 或者是数据库服务器的 IP 地址
        "PORT": os.getenv("DB_PORT"),  # 通常是 '5432'，如果你使用的是默认端口的话
    }
}

# DRF 配置

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "config.drf.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 10,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "NON_FIELD_ERRORS_KEY": "params_error",
    "DEFAULT_RENDERER_CLASSES": ("config.drf.renderers.CustomRenderer",),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
}

AUTH_TOKEN_HEADER_NAME = "HTTP_AUTHORIZATION"

# keycladk配置
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
KEYCLOAK_URL_API = os.getenv("KEYCLOAK_URL_API")
KEYCLOAK_ADMIN_USERNAME = os.getenv("KEYCLOAK_ADMIN_USERNAME")
KEYCLOAK_ADMIN_PASSWORD = os.getenv("KEYCLOAK_ADMIN_PASSWORD")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")

# 本地设置
try:
    from local_settings import *  # noqa
except ImportError:
    pass
