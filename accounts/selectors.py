from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

User: Optional[AbstractUser] = get_user_model()


def get_users_queryset(user_type: Optional[str] = None, is_active: Optional[bool] = None,
                       exclude_types: Optional[list] = None) -> QuerySet[User]:
    queryset = User.objects.select_related('profile').all().exclude(is_staff=True)
    if user_type:
        queryset = queryset.filter(type=user_type)
    if is_active:
        queryset = queryset.filter(is_active=is_active)
    if exclude_types:
        type_index: int = 0
        while len(exclude_types) >= 1:
            queryset = queryset.exclude(type=exclude_types[type_index])
            exclude_types.pop()
    return queryset


def get_user(user_id: Optional[int] = None) -> Optional[User]:
    user: Optional[User] = None
    if user_id:
        user = get_object_or_404(User, id=user_id)
    return user
