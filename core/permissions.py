from rest_framework import permissions


class IsEmployeeUser(permissions.BasePermission):
    """
    Permission to check that the logged in user is actually
    a employee user.
    """

    def has_permission(self, request, view):
        """
        Return `True` if a user is employee, `False` otherwise.
        """
        return request.user.type == 'EMP'

