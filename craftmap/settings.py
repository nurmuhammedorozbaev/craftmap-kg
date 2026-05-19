import os
from pathlib import Path
import dj_database_url  # для подключения PostgreSQL на Render

# 📁 Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Секретный ключ — хранится в переменных окружения
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-secret-key")

# ⚙️ Режим отладки
DEBUG = os.environ.get("DEBUG", "True") == "True"

# 🌐 Разрешённые хосты
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com"]

# 📦 Установленные приложения
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",          # кастомный User работает через AUTH_USER_MODEL
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",               # если используешь DRF
    "backend",                      # твоё приложение
]

# 🧱 Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # для статики
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 📍 Основные настройки проекта
ROOT_URLCONF = "craftmap.urls"
WSGI_APPLICATION = "craftmap.wsgi.application"

# 🗄️ База данных — SQLite локально, PostgreSQL на Render
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=False
    )
}

# ⚡ Кэш
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# 🎨 Шаблоны
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        }, 
    },
]

# 📂 Статика
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "backend" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 🖼️ Медиа
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# 🧩 Авто‑ID
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 👤 Кастомный пользователь
AUTH_USER_MODEL = "backend.CustomUser"
