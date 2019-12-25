"""
This module serves as the application extension which provide utility and helper classes and functions.
"""

import random
import string
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
        # Ascii letters
        letters = string.ascii_letters
        # rl stands for random letters
        rl = ''.join(random.choice(letters) for i in range(8))
        return self.generate_hash(rl)
