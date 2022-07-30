import ast
import types
from parser import *
import json

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
if (x < 6 and y > 2) or y == 2 or x == 5:
    pass
'''

code = ast.parse(str1)
print(ast.dump(code, indent=3))
print()
print()
print()

# ------------------------------------------------------------

with open("test.json", "r") as fp:
    ast_json = fp.read()

parser = Parser(json.loads(ast_json))
tree = parser.parse()
print(ast.dump(tree, indent=3, include_attributes=False))
comp = compile(tree, '<string>', mode="exec")

my = types.ModuleType(
    'My module',
    'Documentation')
exec(comp, my.__dict__)

json_str = '''{"1": 1, "2": 2, "3": 3, "4": 4}'''
filter_value = 3

result = my.func1(json_str, filter_value)
print(result)
