from project.api.models import SecurityStandard
from _datetime import datetime


def compare_fn(agent_response):
    # get the relevant security standard
    standard = SecurityStandard.objects.filter(
        os_type=agent_response.os_type
    ).order_by("-date_created")[0]
    # what needs to be checked
    fields_to_check = {
        "booleans": [
            "antispyware_enabled",
            "antivirus_enabled",
            "behavior_monitor_enabled",
            "nis_enabled",
            "on_access_protection_enabled",
            "real_time_protection_enabled",
        ],
        "dates": [  # coming in as "21-Nov-18 12
            "antispyware_signature_last_updated",
            "antivirus_signature_last_updated",
            "nis_signature_last_updated",
        ],
        "times": [  # coming in as int (days, 65535 if never updated...)
            "full_scan_age",
            "quick_scan_age",
        ],
    }
    secure = True
    message = {"title": "BAB Security Report"}

    # check keys in standard vs response and adds error messages where needed
    # booleans:
    for key in fields_to_check["booleans"]:
        if not getattr(agent_response, key) == getattr(standard, key):
            secure = False
            message[key] = f'should be "{getattr(standard, key)}". Current value: "{getattr(agent_response, key)}"'
    # times:
    for key in fields_to_check["times"]:
        if getattr(agent_response, key) > getattr(standard, key):
            secure = False
            message[key] = f'should be at most {getattr(standard, key)} days. Current value: {getattr(agent_response, key)} days'
    # dates:
    for key in fields_to_check["dates"]:
        return True

    message["status"] = "ok" if secure else "DANGER"
    agent = agent_response.agent
    agent.secure = secure
    agent.last_response_received = datetime.now()
    agent.save()
    return message
