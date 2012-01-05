from django.contrib.auth.models import User

def parse_user_list(text):
    lines = text.split('\n')

    for line in lines:
        stripped_line = line.strip()
        if len(stripped_line) > 0:
            yield line.strip().split(':')
        else:
            continue

def create_users_from_list(text):
    for username, password in parse_user_list(text):
        User.objects.create_user(username, '', password)
