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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()


class Agent(models.Model):

    # owner = models.ForeignKey('auth.user', related_name='auth_user', on_delete=models.CASCADE,)

    class Meta:
        ordering = ['secure', '-last_response_received']

    user = models.ForeignKey(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agents',
    )
    computer_name = models.CharField(
        verbose_name='name',
        max_length=50,
        null=True,
        blank=True
    )
    last_response_received = models.DateTimeField(
        verbose_name='last_response_received',
        null=True,
        blank=True,
    )
    secure = models.BooleanField(
        verbose_name='secure',
        default=False,
    )
    date_created = models.DateTimeField(
        verbose_name='date_created',
        auto_now_add=True,
    )
    system_serial_number = models.CharField(
        verbose_name='system_serial_number',
        max_length=25,
        unique=True,
    )
    is_active = models.BooleanField(
        verbose_name='is_active',
        default=True,
    )

    def __str__(self):
        return f"agent-id: {self.id} | user: {self.user} | secure: {self.secure} | {self.system_serial_number}"


class AgentInstaller(models.Model):

    class Meta:
        ordering = ['-date_created']

    os_type = models.CharField(
        verbose_name='os_type',
        max_length=25,
    )
    version = models.CharField(
        verbose_name='version',
        max_length=25,
    )
    file = models.FileField(
        verbose_name='file',
        upload_to='uploads/',
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
        null=True,
        blank=True
    )
    date_created = models.DateTimeField(
        verbose_name='date_created',
        auto_now_add=True,
    )
    agent_responses = models.ForeignKey(
        verbose_name='agent_responses',
        to='api.AgentResponse',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    to = models.EmailField(
        verbose_name='alert_to',
        max_length=35,
        null=True,
        blank=True
    )
    subject = models.CharField(
        verbose_name='alert_subject',
        max_length=100,
    )
    content = models.TextField(
        verbose_name='alert_content',
    )
    sent = models.BooleanField(
        verbose_name='alert_sent',
        default=False,
    )

    def __str__(self):
        return f"{self.target_machine} | alert sent: {self.sent}"


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
        related_name='responses',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    agent_version = models.CharField(
        verbose_name='agent_version',
        max_length=50,
    )
    ip_address = models.CharField(
        verbose_name='ip_address',
        max_length=50,
        null=True,
        blank=True
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
        default=False,
    )
    antispyware_signature_last_updated = models.CharField(
        verbose_name='antispyware_signature_last_updated',
        max_length=50,
    )
    antivirus_enabled = models.BooleanField(
        verbose_name='antivirus_enabled',
        default=False,
    )
    antivirus_signature_last_updated = models.CharField(
        verbose_name='antivirus_signature_last_updated',
        max_length=50,
    )
    behavior_monitor_enabled = models.BooleanField(
        verbose_name='behavior_monitor_enabled',
        default=False,
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
        default=False,
    )
    nis_signature_last_updated = models.CharField(
        verbose_name='nis_signature_last_updated',
        max_length=50,
    )
    nis_signature_version = models.CharField(
        verbose_name='nis_signature_version',
        max_length=50,
    )
    on_access_protection_enabled = models.BooleanField(
        verbose_name='on_access_protection_enabled',
        default=False,
    )
    real_time_protection_enabled = models.BooleanField(
        verbose_name='real_time_protection_enabled',
        default=False,
    )
    disk_encryption_status = models.CharField(
        verbose_name='disk_encryption_status',
        max_length=50,
    )

    def __str__(self):
        return f"{self.date_created} | ip: {self.ip_address}"


class StartupApp(models.Model):
    name = models.CharField(
        verbose_name='app_name',
        max_length=255,
        null=True,
        blank=True
    )
    command = models.CharField(
        verbose_name='command',
        max_length=255,
        null=True,
        blank=True
    )
    location = models.CharField(
        verbose_name='location',
        max_length=255,
        null=True,
        blank=True
    )
    user = models.CharField(
        verbose_name='app_user',
        max_length=150,
        null=True,
        blank=True
    )
    agent_response = models.ForeignKey(
        verbose_name='agent_response',
        to='api.AgentResponse',
        related_name='startup_apps',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name} | command: {self.command}"


class InstalledApp(models.Model):
    name = models.CharField(
        verbose_name='app_name',
        max_length=255,
        null=True,
        blank=True
    )
    vendor = models.CharField(
        verbose_name='vendor',
        max_length=50,
        null=True,
        blank=True
    )
    version = models.CharField(
        verbose_name='version',
        max_length=50,
        null=True,
        blank=True
    )
    install_date = models.CharField(
        verbose_name='install_date',
        max_length=50,
        null=True,
        blank=True
    )
    agent_response = models.ForeignKey(
        verbose_name='agent_response',
        to='api.AgentResponse',
        related_name='installed_apps',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name} | install_date: {self.install_date}"


class SecurityStandard(models.Model):

    class Meta:
        ordering = ['-date_created']

    date_created = models.DateTimeField(
        verbose_name='date_created',
        auto_now_add=True,
    )
    date_updated = models.DateTimeField(
        verbose_name='date_updated',
        null=True,
        blank=True
    )
    os_type = models.CharField(  # should contain an array?
        verbose_name='os_type',
        max_length=50,
        null=True,
        blank=True
    )
    os_version = models.CharField(
        verbose_name='os_version',
        max_length=50,
        null=True,
        blank=True
    )
    system_manufacturer = models.CharField(
        verbose_name='system_manufacturer',
        max_length=50,
        null=True,
        blank=True
    )
    system_model = models.CharField(
        verbose_name='system_model',
        max_length=50,
        null=True,
        blank=True
    )
    system_type = models.CharField(
        verbose_name='system_type',
        max_length=50,
        null=True,
        blank=True
    )
    bios_version = models.CharField(
        verbose_name='bios_version',
        max_length=50,
        null=True,
        blank=True
    )
    antispyware_enabled = models.BooleanField(
        verbose_name='antispyware_enabled',
        default=True,
    )
    antispyware_signature_last_updated = models.CharField(
        verbose_name='antispyware_signature_last_updated',
        max_length=50,
        null=True,
        blank=True
    )
    antivirus_enabled = models.BooleanField(
        verbose_name='antivirus_enabled',
        default=True,
    )
    antivirus_signature_last_updated = models.CharField(
        verbose_name='antivirus_signature_last_updated',
        max_length=50,
        null=True,
        blank=True
    )
    behavior_monitor_enabled = models.BooleanField(
        verbose_name='behavior_monitor_enabled',
        default=True,
    )
    full_scan_age = models.TextField(
        verbose_name='full_scan_age',
        max_length=50,
        null=True,
        blank=True
    )
    quick_scan_age = models.TextField(
        verbose_name='quick_scan_age',
        max_length=50,
        null=True,
        blank=True
    )
    nis_enabled = models.BooleanField(
        verbose_name='nis_enabled',
        default=True,
    )
    nis_signature_last_updated = models.CharField(
        verbose_name='nis_signature_last_updated',
        max_length=50,
        null=True,
        blank=True
    )
    nis_signature_version = models.CharField(
        verbose_name='nis_signature_version',
        max_length=50,
        null=True,
        blank=True
    )
    on_access_protection_enabled = models.BooleanField(
        verbose_name='on_access_protection_enabled',
        default=True,
    )
    real_time_protection_enabled = models.BooleanField(
        verbose_name='real_time_protection_enabled',
        default=True,
    )
    disk_encryption_status = models.CharField(
        verbose_name='disk_encryption_status',
        max_length=50,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"security standards id: {self.id} | date created: {self.date_created}"
