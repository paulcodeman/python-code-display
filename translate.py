import argparse
import dis
import json
import inspect

BYTECODE = 'bytecode'
JSON = 'json'

def get_bytecode(code):
    consts = code.co_consts
    array = []
    for v in consts:
        if type(v).__name__ == 'code':
            v = get_bytecode(v)
        array.append(v)
    return [list(code.co_names), list(array), list(code.co_code), list(code.co_varnames)]

def get_json(code):
    d = dis.Bytecode(code)
    array = []
    oCode = 0
    for v in d:

        # omission text string name
        if oCode:
            oCode = 0
            continue
            #----

        val = v.argval
        if type(val).__name__ == 'code':
            val = get_json(val)
            oCode = 1

        #params = inspect.getargspec(code)

        # omission import function
        if v.opname == 'IMPORT_NAME':
            del array[-2:]
            #----

        array.append([v.opname, val, v.arg, v.offset, v.argrepr, oCode, list(code.co_varnames), code.co_argcount])
    return array

def parse_arguments():
    parser = argparse.ArgumentParser(description='Display bytecode or JSON representation of Python code')
    parser.add_argument('name', type=str, help='Name of the Python file')
    parser.add_argument('command', type=str, choices=[BYTECODE, JSON], help='Command to run')
    return parser.parse_args()

def main():
    args = parse_arguments()
    with open(args.name, "r") as f:
        code = f.read()
    o = compile(code, "<string>", "exec")

    if args.command == JSON:
        print(json.dumps(get_json(o)))
    elif args.command == BYTECODE:
        print(json.dumps(get_bytecode(o)))

if __name__ == '__main__':
    main()
