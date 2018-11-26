from django.http import HttpResponseForbidden
from rest_framework import permissions

from project.api.models import Agent


class HasRegisteredAgent(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.data['system_serial_number'] in (agent['system_serial_number'] for agent in Agent):
            print('serialnumber is registered')
            return True
        else:
            return HttpResponseForbidden()
