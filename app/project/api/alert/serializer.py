from rest_framework import serializers

from project.api.models import Alert


class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = ['id', 'target_machine', 'subject', 'content', 'to', 'created', 'sent']
        read_only_fields = ['id']

