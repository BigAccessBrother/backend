def name_agent(email, count):
    name = email
    machine_count = ''
    if count == 1:
        machine_count = ', 2nd computer'
    elif count == 2:
        machine_count = ', 3rd computer'
    elif count > 2:
        machine_count = f', {count}th computer'
    return name + machine_count
