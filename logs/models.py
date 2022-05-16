from django.db import models
from django.conf import settings
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
)
from django.dispatch import receiver

class AuthenticationLogs(models.Model):
    LOGIN = 'login'
    LOGOUT = 'logout'

    ACTIONS = [
        (LOGIN, 'login'),
        (LOGOUT, 'logout'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=16, choices=ACTIONS, default=LOGIN)
    date = models.DateTimeField(auto_now_add=True)

@receiver(user_logged_in)
def user_logged_in_cb(sender, request, user, **kwargs):
    AuthenticationLogs.objects.create(user=user, action=AuthenticationLogs.LOGIN)
    print('x'*64)
    print(AuthenticationLogs.LOGIN)
    print(user)
    print('x'*64)

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    AuthenticationLogs.objects.create(user=user, action=AuthenticationLogs.LOGOUT)
    print('x'*64)
    print(AuthenticationLogs.LOGOUT)
    print(user)
    print('x'*64)