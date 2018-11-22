from project.api.models import SecurityStandard


def compareFn(agent_response):
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

    message = {
        "title": "BAB Security Report",
        "status": "ok"
    }
    # check keys in standard vs response and adds error messages where needed
    for key in fields_to_check:
        if not getattr(agent_response, key) == getattr(standard, key):
            message.update(status="DANGER")
            message[key] = f'should be "{getattr(standard, key)}". Current value: "{getattr(agent_response, key)}"'

    return message