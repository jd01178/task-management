from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import CustomUserManager
from core.utils import TimeStampModel, convert_to_webp


class User(AbstractUser):
    class UserTypes(models.TextChoices):
        EMPLOYEE = 'EMP', _('Main User')
        STAFF = 'STF', _('Staff')
    first_name = None
    last_name = None
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=5, choices=UserTypes.choices, default=UserTypes.STAFF)
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']


class AbstractProfileModel(TimeStampModel):
    class GenderTypes(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    image = models.ImageField(upload_to='profiles/%Y/%m/', null=True, blank=True)
    nationality = CountryField(blank_label='select country', default="KE")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone_number = PhoneNumberField(blank=True)
    gender = models.CharField(max_length=2, choices=GenderTypes.choices, default=GenderTypes.FEMALE,
                              null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.image:
            self.image = convert_to_webp(self.image)
        super(AbstractProfileModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Employee(AbstractProfileModel):
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(blank=True)
    dob = models.DateField(null=True, blank=True)
