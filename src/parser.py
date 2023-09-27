from lexer import Token, TokenType
from typing import List


class FunctionDefinition:
    def __init__(self):
        self.name = "UNDEFINED"
        self.params = []
        self.return_type = None
        self.description = "UNDEFINED"  # Comment preceding function definition in C file

    def get_params_as_str(self):
        return ", ".join(self.params)



class ParseContext:
    def __init__(self):
        self.functions: List[FunctionDefinition] = []
        # TODO: Probably won't need it? :)
        #self.structs = []


def parse_token_list(token_list: List[Token]) -> ParseContext:
    ctx = ParseContext()

    for token in token_list:
        print(token)

    return ctx
