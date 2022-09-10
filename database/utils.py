from re import search
from secrets import token_hex


def is_valid_email(email: str):
    return True if search(r'^[a-z0-9]+[\."\-a-z0-9_]*[a-z0-9]+@(gmail|hotmail|yahoo|duck|protonmail|pm)\.(com|in|us|uk|ru|tw|au|jp)$', email) else False


def generate_token():
    return token_hex(256)


def generate_web_token():
    return token_hex(512)


def mask_email(email: str):
    username, domain_part = email.split('@')
    domain, top_level = domain_part.split('.')
    return f'{username[0]+"x"*(len(username)-1)}@{domain[0]+"x"*(len(domain)-1)}.{top_level[0]+"x"*(len(top_level)-1)}'
