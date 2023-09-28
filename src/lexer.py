# This is a simple parser for C files - we could have used something like ply but that would require us to use regular expressions (which frankly are well suited for this problem)
# but I'm not a masochist, I would rather do it the simple way

# Warning: This is probably painfully slow
# Warning: This is probably more convoluted than it needs to be
# Warning: This code works :)

from typing import List, Optional, Union, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TokenType(Enum):
    """
    List of token types. It is not a comprehensive list. Contains only what we need in our specific use-case.
    Further simplified by the fact that function contents can be ignored.
    """
    tPreprocessor = 1
    tAngleOpen = 2
    tAngleClose = 3
    tKeyword = 4
    tName = 5  # If it doesn't fit anything else, then it's a name (e.g. a variable or function name)
    tParenOpen = 6
    tParenClose = 7
    tBraceOpen = 8
    tBraceClose = 9
    tAsterisk = 10
    tSemicolon = 11
    tStringLiteral = 12
    tLineComment = 13
    tBlockComment = 14
    tComma = 15


class Token:
    def __init__(self, token_type, value=None):
        self.token_type: TokenType = token_type
        self.value = value

    def __repr__(self):
        if self.value is None:
            return f"[{str(self.token_type)}]"
        return f"[{str(self.token_type)}]: {self.value}"


class TokenStream:
    def __init__(self, token_list: List[Token]):
        self.token_list = token_list
        self.current_token = 0

    def __len__(self):
        return len(self.token_list)

    def is_end_of_stream(self):
        return self.current_token >= len(self.token_list)

    def get_token(self) -> Optional[Token]:
        if self.is_end_of_stream():
            raise Exception("Can't get token, reached end of stream!")

        token = self.token_list[self.current_token]
        self.current_token += 1
        return token

    def peek_token(self) -> Token:
        if self.is_end_of_stream():
            raise Exception("Can't get token, reached end of stream!")

        token = self.token_list[self.current_token]
        return token


_type_keywords_list = ('void', 'int', 'float', 'double', 'char')
_keywords_list = _type_keywords_list + ("struct", "return")
_preprocessor_list = ("#include", "#if", "#endif", "#define", "#pragma")

def _check_for_simple_token(input: str, i: int) -> Union[Token, Tuple]:
    """ Check for single character token or whitespace """
    if input[i] == '*':
        token = Token(TokenType.tAsterisk)
        return token
    elif input[i] == '(':
        token = Token(TokenType.tParenOpen)
        return token
    elif input[i] == ')':
        token = Token(TokenType.tParenClose)
        return token
    elif input[i] == '{':
        token = Token(TokenType.tBraceOpen)
        return token
    elif input[i] == '}':
        token = Token(TokenType.tBraceClose)
        return token
    elif input[i] == '<':
        token = Token(TokenType.tAngleOpen)
        return token
    elif input[i] == '>':
        token = Token(TokenType.tAngleClose)
        return token
    elif input[i] == ';':
        token = Token(TokenType.tSemicolon)
        return token
    elif input[i] == ',':
        token = Token(TokenType.tComma)
        return token
    elif input[i].isspace():
        return None, True

    return None, False


def _get_next_token(input: str, i: int, token_list: List[Token]) -> int:

    token_check = _check_for_simple_token(input, i)
    if type(token_check) is not tuple:
        token_list.append(token_check)
        return i+1
    elif token_check[1] is True:
        return i+1
    elif input.startswith(_keywords_list, i):
        for idx in range(i+1, len(input)):
            token_check = _check_for_simple_token(input, idx)
            if type(token_check) is tuple:
                if token_check[1] is True:
                    end_idx = idx
                    break
            else:
                end_idx = idx
                break

        if end_idx == -1:
            return len(input)
        token = Token(TokenType.tKeyword, value=input[i:end_idx])
        token_list.append(token)
        return end_idx
    elif input.startswith(_preprocessor_list, i):
        end_i = input.find(' ', i + 1)
        token = Token(TokenType.tPreprocessor, value=input[i:end_i])
        token_list.append(token)
        return end_i + 1
    elif input.startswith('//', i):
        end_i = input.find('\n', i + 2)
        token = Token(TokenType.tLineComment, value=input[i:end_i])
        token_list.append(token)
        return end_i + 1
    elif input.startswith('/*', i):
        end_i = input.find('*/', i + 2) + 2
        token = Token(TokenType.tBlockComment, value=input[i:end_i])
        token_list.append(token)
        return end_i + 1
    elif input[i] == '"':
        end_i = input.find('"', i + 1)
        token = Token(TokenType.tStringLiteral, value=input[i:end_i])
        token_list.append(token)
        return end_i + 1
    else:
        end_idx = -1
        for idx in range(i+1, len(input)):
            token_check = _check_for_simple_token(input, idx)
            if type(token_check) is tuple:
                if token_check[1] is True:
                    end_idx = idx
                    break
            else:
                end_idx = idx
                break

        if end_idx == -1:
            return len(input)
        token = Token(TokenType.tName, value=input[i:end_idx])
        token_list.append(token)
        return end_idx


def get_token_stream(input: str) -> TokenStream:
    token_list = []

    i = 0
    input_len = len(input)
    while True:
        i = _get_next_token(input, i, token_list)
        if i >= input_len:
            break

    return TokenStream(token_list)
