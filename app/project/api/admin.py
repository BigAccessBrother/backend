from django.contrib import admin

from project.api.models import Alert, SecurityStandard, Agent, AgentInstaller, \
    AgentResponse, InstalledApps, StartupApps

admin.site.register(Agent)
admin.site.register(AgentInstaller)
admin.site.register(Alert)
admin.site.register(SecurityStandard)
admin.site.register(AgentResponse)
admin.site.register(InstalledApps)
admin.site.register(StartupApps)