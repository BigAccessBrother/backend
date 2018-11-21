from rest_framework import serializers

from project.api.models import SecurityStandard


class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityStandard
        fields = ['id', 'date_created', 'date_updated', 'os_type', 'os_version', 'system_manufacturer', 'system_model',
                  'system_type', 'bios_version', 'antispyware_enabled',
                  'antispyware_signature_last_updated', 'antivirus_enabled', 'antivirus_signature_last_updated',
                  'behavior_monitor_enabled', 'full_scan_age', 'quick_scan_age', 'nis_enabled',
                  'nis_signature_last_updated', 'nis_signature_version', 'on_access_protection_enabled',
                  'real_time_protection_enabled', 'protection_status']
        read_only_fields = ['id']
