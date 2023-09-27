import argparse
from ctypes import *
from typing import List

import lexer
import parser
import generator

import imagined_output

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate python bindings to a C file")
    parser.add_argument('--file', required=True, help='File to parse')
    parser.add_argument('--dll-name', required=True, help='Dll generated with input file')
    parser.add_argument('--output', required=True, help='Output library name')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()

    with open(args.file, 'r') as f:
        file_contents = f.read()

    #token_list = lexer.get_token_list(file_contents)
    #parsing_context = parser.parse_token_list(token_list)
    #struct_list = parsing_context.structs
    #function_list = parsing_context.functions


    #test_lib = cdll.LoadLibrary("test/test")

    #f_one = getattr(test_lib, 'my_function_one')
    #f_two = getattr(test_lib, 'my_function_two')
    #f_two.argtypes = [c_int]
    #f_two.restype = None
    #f_one()
    #f_two(1)
    #test_lib.my_function_two(23)

    aaaa = generator.FunctionDefinition()
    aaaa.name = "my_function_one"
    aaaa.description = "This is a test desc!"
    function_list = [aaaa]
    with open(f"{args.output}.py", 'w') as f:
        out_file_contents = generator.generate_bindings_python_file(function_list, args.dll_name)
        f.write(out_file_contents)

    from my_test_f import my_function_one
    my_function_one()

