from project.api.models import SecurityStandard
from _datetime import datetime


def compare_fn(agent_response):
    # get the relevant security standard
    standard = SecurityStandard.objects.filter(
        os_type=agent_response.os_type
    ).order_by("-date_created")[0]
    # what needs to be checked
    fields_to_check = [
        "antispyware_enabled",
        "antivirus_enabled",
        "behavior_monitor_enabled",
        "nis_enabled",
        "on_access_protection_enabled",
        "real_time_protection_enabled",
        "protection_status"
    ]
    secure = True
    message = {"title": "BAB Security Report"}
    # check keys in standard vs response and adds error messages where needed
    for key in fields_to_check:
        if not getattr(agent_response, key) == getattr(standard, key):
            secure = False
            message[key] = f'should be "{getattr(standard, key)}". Current value: "{getattr(agent_response, key)}"'

    message["status"] = "ok" if secure else "DANGER"
    agent = agent_response.agent
    agent.secure = secure
    agent.last_response_received = datetime.now()
    agent.save()
    return message
