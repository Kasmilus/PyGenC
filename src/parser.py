from typing import List
import ctypes
import logging

from src import lexer

logger = logging.getLogger(__name__)



class FunctionDefinition:
    def __init__(self):
        self.name = "UNDEFINED"
        self.params = []
        self.params_repr = []
        self.return_type = None
        self.description = "UNDEFINED"  # Comment preceding function definition in C file

        #if ctypes_type is not None:
        #    return ctypes_type.__name__

    def __repr__(self):
        return f"({self.name}({self.get_params_as_str()}) -> {self.get_ret_type_as_str()})"

    def get_ret_type_as_str(self) -> str:
        ret_type = self.return_type
        if ret_type is not None:
            ret_type = ret_type.__name__
        return ret_type

    def get_params_as_str(self) -> str:
        assert len(self.params) == len(self.params_repr)
        return ", ".join(self.params_repr)

    def _get_ctypes_type_from_str(self, value: str, is_ptr: bool):
        ctypes_type = None
        if is_ptr:
            #ctypes_type = ctypes.POINTER(ctypes.c_char)
            logger.warning("IGNORING PTR! Need to figure out how to handle this.")
        if value == "void":
            ctypes_type = None
        elif value == "int":
            ctypes_type = ctypes.c_int
        elif value == "float":
            ctypes_type = ctypes.c_float
        elif value == "double":
            ctypes_type = ctypes.c_double
        elif value == "char":
            if is_ptr:
                ctypes_type = ctypes.c_char_p  # Ptr to null terminated str stream, TODO: will NOT work correctly for other data
            else:
                ctypes_type = ctypes.c_char

        return ctypes_type

    def add_param(self, param_type: str, param_name: str, is_ptr: bool) -> None:
        ctypes_type = self._get_ctypes_type_from_str(param_type, is_ptr)
        self.params.append(ctypes_type)
        if param_type == 'char':
            param_type = 'str'
        if param_name == 'str':
            raise Exception("Forbidden keyword used as param name!")
        self.params_repr.append(f"{param_name}: {param_type}")

    def set_return_type_from_str(self, value: str, is_ptr: bool) -> None:
        ctypes_type = self._get_ctypes_type_from_str(value, is_ptr)
        self.return_type = ctypes_type



class ParseContext:
    def __init__(self):
        self.functions: List[FunctionDefinition] = []
        # TODO: Probably won't need it? :)
        #self.structs = []


def _check_stream_for_ptr(token_stream: lexer.TokenStream) -> bool:
    """ Check if next token is a '*', and move past it if it is. """
    is_ptr = False
    if token_stream.peek_token().token_type == lexer.TokenType.tAsterisk:
        is_ptr = True
        token_stream.get_token()

    return is_ptr


def parse_token_list(token_stream: lexer.TokenStream) -> ParseContext:
    assert len(token_stream) > 0

    ctx = ParseContext()

    last_comment = None

    token = token_stream.get_token()
    while True:
        if token.token_type == lexer.TokenType.tKeyword:
            if token.value in lexer._type_keywords_list:
                # Could be a function or variable, we cna safely assume function (our specific use-case) - TODO: will probably have to change that assumption later
                func = FunctionDefinition()
                # Save return type
                is_ptr = _check_stream_for_ptr(token_stream)
                func.set_return_type_from_str(token.value, is_ptr)
                # Function name
                next_token = token_stream.get_token()
                assert next_token.token_type == lexer.TokenType.tName
                func.name = next_token.value
                next_token = token_stream.get_token()
                assert next_token.token_type == lexer.TokenType.tParenOpen
                # Function arguments
                next_token = token_stream.get_token()
                while next_token.token_type != lexer.TokenType.tParenClose:
                    # If it's one of multiple args, we will get a comma now
                    if next_token.token_type == lexer.TokenType.tKeyword and next_token.value == 'void':
                        if _check_stream_for_ptr(token_stream):
                            logger.error("Found a void* argument, can't deal with that!")
                            raise Exception("Void* argument")
                        break  # Single void arg
                    if next_token.token_type == lexer.TokenType.tComma:
                        next_token = token_stream.get_token()

                    assert next_token.token_type == lexer.TokenType.tKeyword
                    is_ptr = _check_stream_for_ptr(token_stream)
                    var_name_token = token_stream.get_token()
                    assert var_name_token.token_type == lexer.TokenType.tName
                    func.add_param(next_token.value, var_name_token.value, is_ptr)
                    # Get token for the next iteration
                    next_token = token_stream.get_token()

                if last_comment is not None:
                    func.description = last_comment

                ctx.functions.append(func)
        elif token.token_type == lexer.TokenType.tBraceOpen:
            while token.token_type != lexer.TokenType.tBraceClose:
                token = token_stream.get_token()  # Just eat up everything between braces, TODO: This will NOT be correct once we want to include structs
        else:
            pass  # Ignore other tokens

        if token.token_type == lexer.TokenType.tBlockComment or token.token_type == lexer.TokenType.tLineComment:
            last_comment = token.value
        else:
            last_comment = None

        # Get token for the next iteration
        if token_stream.is_end_of_stream():
            break
        token = token_stream.get_token()

    return ctx
