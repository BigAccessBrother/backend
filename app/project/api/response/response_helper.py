from project.api.models import SecurityStandard
from _datetime import datetime


# what needs to be checked + type of check
fields_to_check = {
    "booleans": [
        "antispyware_enabled",
        "antivirus_enabled",
        "behavior_monitor_enabled",
        "nis_enabled",
        "on_access_protection_enabled",
        "real_time_protection_enabled",
    ],
    "days": [
        # coming in as int (days, 65535 or 4294967295 if never updated...)
        "full_scan_age",
        "quick_scan_age",
    ],
    "dates": [
        # coming in as "21-Nov-18 12"
        "antispyware_signature_last_updated",
        "antivirus_signature_last_updated",
        "nis_signature_last_updated",
    ],
}


# turn date strings into usable datetime
def get_time(string):
    return datetime.strptime(string[:9], '%d-%b-%y')


# compare provided agent_response to security standard
def compare_fn(agent_response):
    secure = True
    report = {}
    now = datetime.now()

    # get the latest security standard for matching OS_type
    standard = SecurityStandard.objects.filter(
        os_type=agent_response.os_type
    ).order_by("-date_created")[0]

    # check keys in standard vs response and add error messages where needed
    # booleans:
    for key in fields_to_check["booleans"]:
        if not getattr(agent_response, key) == getattr(standard, key):
            secure = False
            report[key] = f'should be "{getattr(standard, key)}". Current value: "{getattr(agent_response, key)}"'

    # days:
    for key in fields_to_check["days"]:
        if int(getattr(agent_response, key)) > int(getattr(standard, key)):
            secure = False
            report[key] = f'should be max {getattr(standard, key)} days. ' \
                          f'Current value: {getattr(agent_response, key)} days'

    # dates:
    for key in fields_to_check["dates"]:
        if (now - get_time(getattr(agent_response, key))).days > int(getattr(standard, key)):
            secure = False
            report[key] = f'should be max {getattr(standard, key)} ' \
                          f'days ago. Current value: {getattr(agent_response, key)}'

    # add report summary
    report["status"] = "ok" if secure else "DANGER"

    # update agent entry
    agent = agent_response.agent
    agent.secure = secure
    agent.last_response_received = now
    agent.save()

    # if not secure:
    # send email notification

    # return status report
    return report
