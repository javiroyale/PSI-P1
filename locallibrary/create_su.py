import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "locallibrary.settings")
django.setup()

User = get_user_model()

USERNAME = os.getenv("DJANGO_SUPERUSER_USERNAME", "alumnodb")
EMAIL = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
PASSWORD = os.getenv("DJANGO_SUPERUSER_PASSWORD", "alumnodb")

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD,
    )

