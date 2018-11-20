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
        related_name='agent_responses',  # what is related name here?
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
    file = models.TextField(
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


class SecurityStandard(models.Model):
    date_created = models.DateTimeField(
        verbose_name='date_created',
        auto_now_add=True,
    )
    date_updated = models.DateTimeField(
        verbose_name='date_updated',
        auto_now_add=True,
    )
    os_type = models.CharField(  # should contain an array?
        verbose_name='os_type',
        max_length=50,
    )
    os_version = models.CharField(
        verbose_name='os_version',
        max_length=30,
    )
    system_manufacturer = models.CharField(
        verbose_name='system_manufacturer',
        max_length=25,
    )
    system_mode = models.CharField(
        verbose_name='system_mode',
        max_length=25,
    )
    system_type = models.CharField(
        verbose_name='system_type',
        max_length=25,
    )
    bios_version = models.CharField(
        verbose_name='system_type',
        max_length=25,
    )
    antispyware_enabled = models.BooleanField(
        verbose_name='antispyware_enabled',
        blank=False,
    )
    antispyware_signature_last_updated = models.DateTimeField(
        verbose_name='antispyware_signature_last_updated',
        auto_now_add=True,
    )
    antivirus_enabled = models.BooleanField(
        verbose_name='antivirus_enabled',
        blank=False,
    )
    antivirus_signature_last_updated = models.DateTimeField(
        verbose_name='antivirus_signature_last_updated',
        auto_now_add=True,
    )
    behavior_monitor_enabled = models.BooleanField(
        verbose_name='behavior_monitor_enabled',
        blank=False,
    )
    full_scan_age = models.TextField(
        verbose_name='full_scan_age',
        max_length=50,
    )
    quick_scan_age = models.TextField(
        verbose_name='quick_scan_age',
        max_length=50,
    )
    nis_enabled = models.BooleanField(
        verbose_name='nis_enabled',
        blank=False,
    )
    nis_signature_last_updated = models.DateTimeField(
        verbose_name='nis_signature_last_updated',
        auto_now_add=True,
    )
    nis_signature_version = models.CharField(
        verbose_name='nis_signature_version',
        max_length=50,
    )
    on_access_protection_enabled = models.BooleanField(
        verbose_name='on_access_protection_enabled',
        blank=False,
    )
    real_time_protection_enabled = models.BooleanField(
        verbose_name='real_time_protection_enabled',
        blank=False,
    )
    protection_status = models.CharField(  # does it have to be a string?
        verbose_name='protection_status',
        max_length=25,
    )
    list_of_startup_apps = models.TextField(  # ???
        verbose_name='list_of_startup_apps',
    )
    list_of_installed_apps = models.TextField(  # ???
        verbose_name='list_of_installed_apps',
    )


class ClientResponse(models.Model):
    date_created = models.DateTimeField(
        verbose_name='date_created',
        auto_now_add=True,
    )
    system_serial_number = models.ForeignKey(
        verbose_name='system_serial_number',
        to='api.Client',
        on_delete=models.CASCADE,
    )
    alerts = models.ForeignKey(
        verbose_name='alerts',
        to='api.Alert',
        on_delete=models.CASCADE,
    )
    computer_name = models.CharField(
        verbose_name='computer_name',
        max_length=25,
    )
    client_version = models.CharField(
        verbose_name='client_version',
        max_length=25,
    )
    ip_address = models.CharField(
        verbose_name='ip_address',
        max_length=25,
    )
    os_type = models.CharField(  # should contain an array?
        verbose_name='os_type',
        max_length=50,
    )
    os_version = models.CharField(
        verbose_name='os_version',
        max_length=30,
    )
    system_manufacturer = models.CharField(
        verbose_name='system_manufacturer',
        max_length=25,
    )
    system_mode = models.CharField(
        verbose_name='system_mode',
        max_length=25,
    )
    system_type = models.CharField(
        verbose_name='system_type',
        max_length=25,
    )
    bios_version = models.CharField(
        verbose_name='system_type',
        max_length=25,
    )
    antispyware_enabled = models.BooleanField(
        verbose_name='antispyware_enabled',
        blank=False,
    )
    antispyware_signature_last_updated = models.DateTimeField(
        verbose_name='antispyware_signature_last_updated',
        auto_now_add=True,
    )
    antivirus_enabled = models.BooleanField(
        verbose_name='antivirus_enabled',
        blank=False,
    )
    antivirus_signature_last_updated = models.DateTimeField(
        verbose_name='antivirus_signature_last_updated',
        auto_now_add=True,
    )
    behavior_monitor_enabled = models.BooleanField(
        verbose_name='behavior_monitor_enabled',
        blank=False,
    )
    full_scan_age = models.TextField(
        verbose_name='full_scan_age',
        max_length=50,
    )
    quick_scan_age = models.TextField(
        verbose_name='quick_scan_age',
        max_length=50,
    )
    nis_enabled = models.BooleanField(
        verbose_name='nis_enabled',
        blank=False,
    )
    nis_signature_last_updated = models.DateTimeField(
        verbose_name='nis_signature_last_updated',
        auto_now_add=True,
    )
    nis_signature_version = models.CharField(
        verbose_name='nis_signature_version',
        max_length=50,
    )
    on_access_protection_enabled = models.BooleanField(
        verbose_name='on_access_protection_enabled',
        blank=False,
    )
    real_time_protection_enabled = models.BooleanField(
        verbose_name='real_time_protection_enabled',
        blank=False,
    )
    protection_status = models.CharField(  # does it have to be a string?
        verbose_name='protection_status',
        max_length=25,
    )
    list_of_startup_apps = models.TextField(  # ???
        verbose_name='list_of_startup_apps',
    )
    list_of_installed_apps = models.TextField(  # ???
        verbose_name='list_of_installed_apps',
    )

