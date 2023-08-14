from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('accounts.api.urls')),
    path('api/v1/', include('task.api.urls')),
    path('admin/', admin.site.urls),
    path('', include('task.urls')),
    path('', include('accounts.urls')),

    # password reset
    path('reset-password/', PasswordResetView.as_view(
        template_name="accounts/forgot-password.html",
        html_email_template_name="email/password-reset.html",
        subject_template_name="email/password_reset_subject.txt",
    ), name="password_reset"),
    path('reset-password-done/', PasswordResetDoneView.as_view(template_name="accounts/confirm-mail.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="accounts/reset-password.html"),
         name="password_reset_confirm"),
    path('reset-password-complete/', PasswordResetCompleteView.as_view(template_name="accounts/reset-completed.html"),
         name="password_reset_complete"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
               static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
