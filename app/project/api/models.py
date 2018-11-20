from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Client(models.Model):
    user = models.ForeignKey(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clients',
    )
    name = models.CharField(
        verbose_name='name',
        max_length=25,
    )
    mac_address = models.CharField(
        verbose_name='name',
        max_length=64,
    )
    agent_responses = models.ForeignKey(
        verbose_name='agent_responses',
        to='api.ClientResponse',
        on_delete=models.CASCADE,
        related_name='',  # what is related name here?
    )
    last_response_received = models.DateTimeField(
        verbose_name='last_response_received',
        auto_now_add=True,
    )
    secure = models.BooleanField(
        verbose_name='secure',
        blank=False,
    )
    alerts = models.ForeignKey(
        verbose_name='alerts',
        to='api.Alert',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(
        verbose_name='date_created',
        auto_now_add=True,
    )


class ClientInstaller(models.Model):
    os_type = models.CharField(
        verbose_name='os_type',
        max_length=25,
    )
    version = models.CharField(
        verbose_name='version',
        max_length=25,
    )
    file = models.CharField(
        verbose_name='file',

    )
    date_created = models.DateTimeField(
        verbose_name='date_created',
        auto_now_add=True,
    )


class Alert(models.Model):
    target_machine = models.ForeignKey(
        verbose_name='target_machine',
        to='api.Client',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(
        verbose_name='date_created',
        auto_now_add=True,
    )
    agent_responses = models.ForeignKey(
        verbose_name='agent_responses',
        to='api.ClientResponse',
        on_delete=models.CASCADE,
    )
    to = models.EmailField(  #should it be email field?
        verbose_name='alert_to',
        max_length=35,
    )
    subject = models.CharField(
        verbose_name='alert_subject',
        max_length=35,
    )
    content = models.TextField(
        verbose_name='alert_content',
    )
    sent = models.BooleanField(
        verbose_name='alert_sent',
        blank=False,
    )

