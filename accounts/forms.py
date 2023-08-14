from django.contrib.auth import logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, ReadOnlyPasswordHashField
from django.forms import forms, ModelForm, ChoiceField

from accounts.models import Employee

User = get_user_model()


class UserAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is None or self.user_cache.is_staff:
            logout(self.request)
            raise forms.ValidationError('Invalid username or password or both', code='invalid login')


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['name', 'email', 'password1', 'password2']


USER_TYPES = [
    ('EMP', 'Main User'),
]


class UserRegistrationForm(UserCreationForm):
    type = ChoiceField(choices=USER_TYPES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['name', 'email', 'type', 'password1', 'password2']


class UserAdminChangeForm(ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admins
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'is_active']

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.upper()

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['name']


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['image', 'phone_number', 'nationality', 'gender', 'bio', 'website']
