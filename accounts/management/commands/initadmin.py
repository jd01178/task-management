from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.management import BaseCommand

User: AbstractUser = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            User.objects.create_superuser(
                email=getattr(settings, "DEFAULT_ADMIN_EMAIL"),
                password=getattr(settings, "DEFAULT_ADMIN_PASSWORD")
            )
            self.stdout.write(
                self.style.SUCCESS(f'{getattr(settings, "DEFAULT_ADMIN_EMAIL")}, has been created successfully.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Admin accounts can only be initialized if no Accounts exist')
            )
