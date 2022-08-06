import ast
import json
import types

from json_converter import convert_to_json
from parser import Parser


def change_code():
    str2 = '''
import json

def func1(json_str, filter_value):
    res = {}
    count = 0
    for k, v in json.loads(json_str).items():
        count += 1
        if v == filter_value:
            res[k] = v
    print("count: " + str(count))
    return json.dumps(res) 
    '''
    code = ast.parse(str2)
    # print(ast.dump(code, indent=3, include_attributes=False))
    print()
    print()

    json_ast = convert_to_json(code)
    # print(json.dumps(json_ast, indent=3))
    with open("test2.json", "w") as fp:
        fp.write(json.dumps(json_ast, indent=3))


def compile_ast(file):
    with open(file, "r") as fp:
        ast_json = fp.read()

    parser = Parser(json.loads(ast_json))
    tree = parser.parse()

    # --------------------
    # tree = ast.parse(str2)
    # --------------------
    # print(ast.dump(tree, indent=3, include_attributes=False))
    # print()
    # print(ast.unparse(tree))
    # print()
    comp = compile(tree, '<string>', mode="exec")

    my = types.ModuleType(
        'My module',
        'Documentation')
    exec(comp, my.__dict__)
    return my

def test_module(my):
    json_str = '''{"one": 1, "two": 2, "three": 3, "four": 4}'''
    filter_value = 3

    result = my.func1(json_str, filter_value)
    print(result)

# ----------------------------------------------------------
# experiments zone

str1 = '''
x = 5
y = 2
z = x + 3
if (x < 6 and y > 2) or y == 2 or x == 5:
    result = x + y + zz
'''

# ------------------------------------------------------------

my = compile_ast("test.json")
test_module(my)

change_code()
my = compile_ast("test2.json")
test_module(my)