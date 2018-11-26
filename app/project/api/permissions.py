from rest_framework import permissions

from project.api.models import Agent


class HasRegisteredAgent(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            Agent.objects.get(system_serial_number=request.data['system_serial_number'])
        except Agent.DoesNotExist:
            return False
        return True
