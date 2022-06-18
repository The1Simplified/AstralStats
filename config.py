import secrets

class Config:
    SECRET_KEY = f'{secrets.token_hex(16)}'
