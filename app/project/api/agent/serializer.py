from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from rest_framework import serializers

from project.api.models import Agent


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'user', 'computer_name', 'last_response_received', 'secure', 'date_created',
                  'system_serial_number', 'is_active']
        read_only_fields = ['id', 'user', 'date_created']



