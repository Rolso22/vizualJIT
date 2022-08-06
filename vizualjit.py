import types, ast
from parser import Parser
from json_converter import convert_to_json
import json

# ----------------------------------------------------------
# experiments zone

str2 = '''
import json, ast

def func1(json_str, filter_value):
    res = {}
    for k, v in json.loads(json_str).items():
        if v == filter_value:
            res[k] = v
    return json.dumps(res) 
'''

str1 = '''
x = 5
y = 2
z = x + 3
if (x < 6 and y > 2) or y == 2 or x == 5:
    result = x + y + zz
'''

code = ast.parse(str1)
# print(ast.dump(code, indent=3))
# print()
# print()
#
# json_ast = convert_to_json(code)
# print(json.dumps(json_ast, indent=3))

# ------------------------------------------------------------

with open("test.json", "r") as fp:
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

json_str = '''{"1": 1, "2": 2, "3": 3, "4": 4}'''
filter_value = 3

result = my.func1(json_str, filter_value)
print(result)
