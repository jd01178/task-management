from django.urls import path

from accounts.api.views import EmployeeProfileRetrieveUpdateAPIView, ChangePasswordView

urlpatterns = [
    path('employee-profile/', EmployeeProfileRetrieveUpdateAPIView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
]
