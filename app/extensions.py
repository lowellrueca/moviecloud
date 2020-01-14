"""
This module serves utility classes and functions.
"""
import secrets
from hashlib import blake2s


async def generate_hash(data: str):
    """
    Generates and return hashed strings
    """
    if str_data == None: return
        b = bytes(str_data, 'utf-8')
        return blake2s(b).hexdigest()


async def generate_token():
    """
    Generates and return random string token
    """
    return secrets.token_urlsafe(128)
