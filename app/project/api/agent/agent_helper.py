def name_agent(email, count):
    name = email.split('@')[0]
    return f'{name} #{count + 1}' if count else name
