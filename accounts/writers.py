from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

User: AbstractUser = get_user_model()


def create_user(args: dict) -> User:
    user = User.objects.create_user(**args)
    return user

