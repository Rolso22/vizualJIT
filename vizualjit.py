import ast
import json
import types

import json_converter
from json_converter import convert_to_json
from parser import Parser


def change_code():
    str1 = '''
def f(x, y):
    return x * y
    '''
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

my = compile_ast("test.json")  # without count
test_module(my)

change_code()
my = compile_ast("test2.json")  # with count
test_module(my)

# -----------------------------------------------------------

print()
str3 = '''
def f(x, y):
    return x * y
'''

fun = ast.parse(str3)
# print(json.dumps(json_converter.convert_to_json(fun), indent=3))

fun_comp = compile(fun, '<string>', mode="exec")

fun_module = types.ModuleType(
    'fun',
    'doc')
exec(fun_comp, fun_module.__dict__)

result = fun_module.f(3, 5)  # 3 * 5
print(result)


class ChangeFun(ast.NodeTransformer):

    def visit_Return(self, node):
        value = node.value
        return ast.Return(value=ast.BinOp(left=value.left,
                                          op=ast.Add(),
                                          right=value.right))


fun2 = ast.fix_missing_locations(ChangeFun().visit(fun))
# print(json.dumps(json_converter.convert_to_json(fun2), indent=3))

fun_comp = compile(fun, '<string>', mode="exec")

fun_module = types.ModuleType(
    'fun',
    'doc')
exec(fun_comp, fun_module.__dict__)

result = fun_module.f(3, 5)  # 3 + 5
print(result)
