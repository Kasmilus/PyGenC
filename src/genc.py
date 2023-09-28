import argparse
from ctypes import *
from typing import List
import logging

from src import lexer
from src import parser
from src import generator

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate python bindings for a C DLL")
    parser.add_argument('--file', required=True, help='File to parse')
    parser.add_argument('--dll-name', required=True, help='Dll generated with input file')
    parser.add_argument('--output', required=True, help='Output library name')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)
    args = parse_args()

    with open(args.file, 'r') as f:
        file_contents = f.read()

    token_stream = lexer.get_token_stream(file_contents)
    parsing_context = parser.parse_token_list(token_stream)
    function_list = parsing_context.functions
    print(function_list)


    #test_lib = cdll.LoadLibrary("test/test")

    #f_one = getattr(test_lib, 'my_function_one')
    #f_two = getattr(test_lib, 'my_function_two')
    #f_two.argtypes = [c_int]
    #f_two.restype = None
    #f_one()
    #f_two(1)
    #test_lib.my_function_two(23)

    #aaaa = parser.FunctionDefinition()
    #aaaa.name = "my_function_one"
    #aaaa.description = "This is a test desc!"
    #function_list = [aaaa]
    with open(f"{args.output}.py", 'w') as f:
        out_file_contents = generator.generate_bindings_python_file(function_list, args.dll_name)
        f.write(out_file_contents)

    import my_test_f
    my_test_f.simple_function()
    val = my_test_f.function_with_return_value()
    assert val == 72
    #my_function_one()

