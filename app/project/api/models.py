from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile',
    )
    # is_admin = models.BooleanField(
    #     verbose_name='is_admin',
    #     blank=False,
    #     null=False,
    # )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()


class Agent(models.Model):

    # owner = models.ForeignKey('auth.User', related_name='auth_user', on_delete=models.CASCADE,)

    user = models.ForeignKey(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user',
    )
    computer_name = models.CharField(
        verbose_name='name',
        max_length=25,
    )
    last_response_received = models.DateTimeField(
        verbose_name='last_response_received',
        auto_now_add=True,
    )
    secure = models.BooleanField(
        verbose_name='secure',
        blank=False,
    )
    date_created = models.DateTimeField(
        verbose_name='date_created',
        auto_now_add=True,
    )
    system_serial_number = models.CharField(
        verbose_name='system_serial_number',
        max_length=25,
    )
    is_active = models.BooleanField(
        verbose_name='is_active',
        blank=False,
    )

    def __str__(self):
        return f"agent-id: {self.id} | user: {self.user} | secure: {self.secure} | {self.system_serial_number}"


class AgentInstaller(models.Model):
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
        to='api.agent',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(
        verbose_name='date_created',
        auto_now_add=True,
    )
    agent_responses = models.ForeignKey(
        verbose_name='agent_responses',
        to='api.AgentResponse',
        on_delete=models.CASCADE,
    )
    to = models.EmailField(  # should it be email field?
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


class AgentResponse(models.Model):

    class Meta:
        ordering = ['-date_created']

    date_created = models.DateTimeField(
        verbose_name='date_created',
        auto_now_add=True,
    )
    agent = models.ForeignKey(
        verbose_name='agent',
        to='Agent',
        related_name='agent',
        on_delete=models.CASCADE,
    )
    agent_version = models.CharField(
        verbose_name='agent_version',
        max_length=50,
    )
    ip_address = models.CharField(
        verbose_name='ip_address',
        max_length=50,
    )
    os_type = models.CharField(  # should contain an array?
        verbose_name='os_type',
        max_length=50,
    )
    os_version = models.CharField(
        verbose_name='os_version',
        max_length=50,
    )
    system_manufacturer = models.CharField(
        verbose_name='system_manufacturer',
        max_length=50,
    )
    system_model = models.CharField(
        verbose_name='system_model',
        max_length=50,
    )
    system_type = models.CharField(
        verbose_name='system_type',
        max_length=50,
    )
    bios_version = models.CharField(
        verbose_name='bios_version',
        max_length=50,
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
    full_scan_age = models.CharField(
        verbose_name='full_scan_age',
        max_length=50,
    )
    quick_scan_age = models.CharField(
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
        max_length=50,
    )

    def __str__(self):
        return f"{self.date_created} | {self.computer_name} | ip: {self.ip_address}"


class StartupApps(models.Model):
    name = models.CharField(
        verbose_name='app_name',
        max_length=25,
        null=True,
    )
    command = models.CharField(
        verbose_name='command',
        max_length=50,
        null=True,
    )
    location = models.CharField(
        verbose_name='location',
        max_length=50,
        null=True,
    )
    user = models.CharField(
        verbose_name='app_user',
        max_length=50,
        null=True,
    )
    agent_response = models.ForeignKey(
        verbose_name='agent_response',
        to='api.AgentResponse',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name} | command: {self.command}"


class InstalledApps(models.Model):
    name = models.CharField(
        verbose_name='app_name',
        max_length=50,
        null=True,
    )
    vendor = models.CharField(
        verbose_name='vendor',
        max_length=50,
        null=True,
    )
    version = models.CharField(
        verbose_name='version',
        max_length=25,
        null=True,
    )
    install_date = models.CharField(
        verbose_name='install_date',
        max_length=25,
        null=True,
    )
    agent_response = models.ForeignKey(
        verbose_name='agent_response',
        to='api.AgentResponse',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name} | install_date: {self.install_date}"


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
    system_model = models.CharField(
        verbose_name='system_mode',
        max_length=25,
    )
    system_type = models.CharField(
        verbose_name='system_type',
        max_length=25,
    )
    bios_version = models.CharField(
        verbose_name='system_type',
        max_length=50,
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

    def __str__(self):
        return f"security standards id: {self.id} | date created: {self.date_created}"
