"""
This module serves as the application extension which provide utility and helper classes and functions.
"""

import secrets
from hashlib import blake2s


class HashBuilder:
    def __init__(self):
        pass
        
    def generate_hash(self, str_data: str) -> str:
        """
        This function generates hashed password
        """
        if str_data == None: return
        b = bytes(str_data, 'utf-8')
        return blake2s(b).hexdigest()

    def generate_token(self):
        """
        This function generates hashed strings
        for generating token values
        """
        return secrets.token_urlsafe(64)
