from rest_framework import serializers

from project.api.models import AgentResponse, Agent, StartupApp, InstalledApp
from project.api.response.response_helper import compare_fn


class StartupAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = StartupApp
        fields = '__all__'


class InstalledAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstalledApp
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    report = serializers.SerializerMethodField(read_only=True)

    # needs to be reworked depending on necessity of the company
    #
    # startup_apps = serializers.SerializerMethodField(read_only=True)
    # installed_apps = serializers.SerializerMethodField(read_only=True)
    #
    # def get_startup_apps(self, obj):
    #     apps = obj.startup_apps.all()
    #     return [StartupAppSerializer(app).data for app in apps]
    #
    # def get_installed_apps(self, obj):
    #     apps = obj.installed_apps.all()
    #     return [InstalledAppSerializer(app).data for app in apps]

    def get_report(self, obj):
        return compare_fn(obj, initial=False)

    class Meta:
        model = AgentResponse
        fields = ['id', 'agent', 'agent_version', 'os_type', 'ip_address', 'date_created',
                  'os_version', 'system_manufacturer', 'system_model', 'system_type', 'bios_version',
                  'antispyware_enabled', 'antispyware_signature_last_updated', 'antivirus_enabled',
                  'antivirus_signature_last_updated', 'behavior_monitor_enabled', 'full_scan_age', 'quick_scan_age',
                  'nis_enabled', 'nis_signature_last_updated', 'nis_signature_version', 'on_access_protection_enabled',
                  'real_time_protection_enabled', 'disk_encryption_status', 'report']
        read_only_fields = ['id', 'date_created', 'report', 'agent', 'ip_address']

    def create(self, validated_data):
        # create the AgentResponse entry
        number = self.initial_data.get('system_serial_number')
        agent = Agent.objects.get(system_serial_number=number)
        ip_address = self.context.get('request').META.get('REMOTE_ADDR')
        agent_response = AgentResponse.objects.create(
            ip_address=ip_address,
            agent=agent,
            **validated_data,
        )

        # create all the apps
        for app in self.initial_data.get('startup_apps'):
            StartupApp.objects.create(
                name=app.get('name'),
                command=app.get('command'),
                location=app.get('location'),
                user=app.get('user'),
                agent_response=agent_response
            )
        for app in self.initial_data.get('installed_apps'):
            InstalledApp.objects.create(
                name=app.get('name'),
                vendor=app.get('vendor'),
                version=app.get('version'),
                install_date=app.get('install_date'),
                agent_response=agent_response
            )

        return agent_response
