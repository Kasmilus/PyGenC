from typing import List

from src.parser import FunctionDefinition


def generate_bindings_python_file(functions: List[FunctionDefinition], dll_name: str) -> str:
    header = "#This file was automatically generated with genc.py\n"
    imports = "from pathlib import Path\n" \
              "from ctypes import *\n" \
              "from typing import List\n"
    load_lib = f"_lib_handle = cdll.LoadLibrary((Path(__file__).parent / \"{dll_name}\").as_posix())\n"
    create_function = "" \
                      "def _create_function_object(func_name: str, arguments: List, return_type ) -> CFUNCTYPE:\n" \
                      "    func = getattr(_lib_handle, func_name)\n" \
                      "    func.argtypes = arguments\n" \
                      "    func.restype = return_type\n" \
                      "    return func\n"

    # Create dictionary with ctypes function objects (actual callables to the DLL)
    func_list = "_functions = {"
    for f in functions:
        func_list += f"\n    \"{f.name}\": _create_function_object(\"{f.name}\", {f.params}, {f.return_type}),"
    func_list += "\n}\n"

    # Create definitions calling objects in the func_list dictionary. This is so we can get useful type info when using this lib from an IDE.
    func_definitions = ""
    for f in functions:
        func_definitions += "\n"
        func_definitions += f"def {f.name}({f.get_params_as_str()}) -> {f.return_type}:\n"
        func_definitions += '    """\n'
        func_definitions += f"    {f.description}\n"
        func_definitions += '    """\n'
        func_definitions += f"    return _functions[\"{f.name}\"]()\n"
    func_definitions += "\n"

    final_str = f"{header}\n{imports}\n{load_lib}\n{create_function}\n{func_list}\n###\n{func_definitions}"
    return final_str
