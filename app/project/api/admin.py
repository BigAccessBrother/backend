from django.contrib import admin

from project.api.models import Alert, SecurityStandard, Agent, AgentInstaller, \
    AgentResponse, InstalledApp, StartupApp

admin.site.register(Agent)
admin.site.register(AgentInstaller)
admin.site.register(Alert)
admin.site.register(SecurityStandard)
admin.site.register(AgentResponse)
admin.site.register(InstalledApp)
admin.site.register(StartupApp)
