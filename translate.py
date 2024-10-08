import argparse
import dis
import json
import inspect
import os

BYTECODE = 'bytecode'
JSON = 'json'

def get_bytecode(code):
    """
    Recursively converts the Python code object to a list representation of its bytecode.
    """
    bytecode_constants = []
    for const in code.co_consts:
        if isinstance(const, type(code)):
            const = get_bytecode(const)
        bytecode_constants.append(const)
    return [
        list(code.co_names),
        bytecode_constants,
        list(code.co_code),
        list(code.co_varnames)
    ]

def get_json(code):
    """
    Converts the Python bytecode to a JSON-compatible list structure.
    """
    bytecode = dis.Bytecode(code)
    json_representation = []
    skip_next = False

    for instruction in bytecode:
        if skip_next:
            skip_next = False
            continue

        arg_val = instruction.argval
        if isinstance(arg_val, type(code)):
            arg_val = get_json(arg_val)
            skip_next = True

        if instruction.opname == 'IMPORT_NAME':
            del json_representation[-2:]  # Remove the last two entries for import cleanup

        json_representation.append({
            "opname": instruction.opname,
            "argval": arg_val,
            "arg": instruction.arg,
            "offset": instruction.offset,
            "argrepr": instruction.argrepr,
            "varnames": list(code.co_varnames),
            "argcount": code.co_argcount
        })

    return json_representation

def parse_arguments():
    """
    Parses command-line arguments for file name and command (bytecode or json).
    """
    parser = argparse.ArgumentParser(description='Display bytecode or JSON representation of Python code')
    parser.add_argument('file_name', type=str, help='Name of the Python file to process')
    parser.add_argument('command', type=str, choices=[BYTECODE, JSON], help='Output format: bytecode or JSON')
    return parser.parse_args()

def main():
    """
    Main entry point for the script. Reads the input file, compiles it, and outputs either bytecode or JSON.
    """
    args = parse_arguments()

    # Check if the file exists before attempting to read it
    if not os.path.isfile(args.file_name):
        print(f"Error: File '{args.file_name}' not found.")
        return

    try:
        with open(args.file_name, "r") as f:
            code_content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    try:
        compiled_code = compile(code_content, "<string>", "exec")
    except Exception as e:
        print(f"Error compiling code: {e}")
        return

    if args.command == JSON:
        print(json.dumps(get_json(compiled_code), indent=4))
    elif args.command == BYTECODE:
        print(json.dumps(get_bytecode(compiled_code), indent=4))

if __name__ == '__main__':
    main()
