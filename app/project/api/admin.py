from django.contrib import admin

from project.api.models import Client, ClientInstaller, Alert, SecurityStandard, ClientResponse

admin.site.register(Client)
admin.site.register(ClientInstaller)
admin.site.register(Alert)
admin.site.register(SecurityStandard)
admin.site.register(ClientResponse)
