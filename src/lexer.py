# This is a simple parser for C files - we could have used something like ply but that would require us to use regular expressions (which frankly are well suited for this problem)
# but I'm not a masochist, I would rather do it the simple way

from typing import List
from enum import Enum


def TokenType(Enum):
    Struct = 1,
    Type = 2,


class Token:
    def __init__(self, token_type, value):
        self.token_type: TokenType = token_type
        self.value = value


def get_token_list(input: str) -> List[Token]:
    return []