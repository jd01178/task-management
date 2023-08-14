from typing import Optional

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy


def restrict_access(function=None, user_type: Optional[str] = None, redirect_field_name=REDIRECT_FIELD_NAME,
                    login_url: Optional[str] = reverse_lazy('accounts:login')):
    """
    Decorator for views that checks that the logged-in user is the selected user_type,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and not u.is_staff and u.type == user_type,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def decorate_url_patterns(patterns, user_type: str, login_url: Optional[str] = 'accounts:login'):
    decorated_patterns = []
    for pattern in patterns:
        callback = pattern.callback
        pattern.callback = restrict_access(function=callback, user_type=user_type, login_url=login_url)
        pattern._callback = restrict_access(function=callback, user_type=user_type, login_url=login_url)
        decorated_patterns.append(pattern)
    return decorated_patterns
