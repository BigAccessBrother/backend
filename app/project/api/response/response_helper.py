from project.api.alert.alert_helper import create_alert
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
        # used to come in as "21-Nov-18 ..."
        # recently comes in as "12/3/2018 ..."
        "antispyware_signature_last_updated",
        "antivirus_signature_last_updated",
        "nis_signature_last_updated",
    ],
}

time_formats = ['%m/%d/%Y', '%d-%b-%y', '%d.%b.%y',
                '%d/%b/%y', '%m-%d-%Y', '%m.%d.%Y']


# turn date strings into usable datetime
def get_time(string):
    for fmt in time_formats:
        try:
            return datetime.strptime(string.split(' ')[0], fmt)
        except ValueError:
            pass
    raise ValueError('no matching datetime format')


# compare provided agent_response to security standard
def compare_fn(agent_response, initial=True):
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

    if initial:
        # update agent entry
        agent = agent_response.agent
        agent.secure = secure
        agent.last_response_received = now
        agent.save()

        if not secure:
            create_alert(report, agent)

    return report
