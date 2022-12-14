import ast
from constants import *


class Parser:

    def __init__(self, json_ast):
        self.json_ast = json_ast
        self.python_ast = ast.parse("")
        self.node_dict = {
            Constants.CONSTANT: self.constant_node,
            Constants.NAME_v: self.name_node,
            Constants.IMPORT: self.import_node,
            Constants.FUNCTION_DEF: self.function_def_node,
            Constants.ASSIGN: self.assign_node,
            Constants.AUG_ASSIGN: self.aug_assign_node,
            Constants.DICT: self.dict_node,
            Constants.RETURN: self.return_node,
            Constants.CALL: self.call_node,
            Constants.ATTRIBUTE: self.attribute_node,
            Constants.SUBSCRIPT: self.subscript_node,
            Constants.IF: self.if_node,
            Constants.COMPARE: self.compare_node,
            Constants.FOR: self.for_node,
            Constants.TUPLE: self.tuple_node,
            Constants.EXPR: self.expr_node,
            Constants.LIST: self.list_node,
            Constants.UNARY_OP: self.unary_op_node,
            Constants.BIN_OP: self.bin_op_node,
            Constants.BOOL_OP: self.bool_op_node,
        }
        self.name_ctx = {
            Constants.STORE: ast.Store(),
            Constants.LOAD: ast.Load(),
            Constants.DELETE: ast.Delete()
        }
        self.comparison_ops = {
            Constants.EQ: ast.Eq(),
            Constants.NOT_EQ: ast.NotEq(),
            Constants.LT: ast.Lt(),
            Constants.LTE: ast.LtE(),
            Constants.GT: ast.Gt(),
            Constants.GTE: ast.GtE(),
            Constants.IS: ast.Is(),
            Constants.IS_NOT: ast.IsNot(),
            Constants.IN: ast.In(),
            Constants.IN_NOT: ast.NotIn()
        }

        self.unary_ops = {
            Constants.UADD: ast.UAdd(),
            Constants.USUB: ast.USub(),
            Constants.NOT: ast.Not(),
            Constants.INVERT: ast.Invert()
        }

        self.bin_ops = {
            Constants.ADD: ast.Add(),
            Constants.SUB: ast.Sub(),
            Constants.MULT: ast.Mult(),
            Constants.DIV: ast.Div(),
            Constants.FLOOR_DIV: ast.FloorDiv(),
            Constants.MOD: ast.Mod(),
            Constants.POW: ast.Pow()
        }

        self.bool_ops = {
            Constants.AND: ast.And(),
            Constants.OR: ast.Or()
        }

    def parse(self):
        body = self.json_ast[Constants.BODY]
        self.python_ast.body = self.body_parse(body)
        for node in self.python_ast.body:
            ast.fix_missing_locations(node)
        return self.python_ast

    def body_parse(self, body):
        ast_body = []
        for node in body:
            res = self.node_analyze(node)
            ast_body.append(res)
        return ast_body

    def node_analyze(self, node):
        return self.node_dict[node[Constants.AST_TYPE]](node)

    def constant_node(self, node):
        return ast.Constant(value=node[Constants.VALUE])

    def name_node(self, node):
        return ast.Name(id=node[Constants.ID],
                        ctx=self.name_ctx[node[Constants.CTX]])

    def import_node(self, node):
        return ast.Import(names=[ast.alias(name=name[Constants.NAME],
                                           asname=name[Constants.ASNAME]) for name in node[Constants.NAMES]])

    def function_def_node(self, node):
        return ast.FunctionDef(name=node[Constants.NAME],
                               args=self.get_arguments_from_function(node[Constants.ARGS]),
                               body=self.body_parse(node[Constants.BODY]),
                               decorator_list=[])

    def arg_node(self, node):
        return ast.arg(arg=node[Constants.ARG])

    def get_arguments_from_function(self, args):
        return ast.arguments(args=[self.arg_node(arg) for arg in args[Constants.ARGS]],
                             posonlyargs=[],
                             kwonlyargs=[],
                             kw_defaults=[],
                             defaults=[ast.Constant(value=value) for value in args[Constants.DEFAULTS]])

    def assign_node(self, node):
        return ast.Assign(targets=self.get_targets_from_assign(node[Constants.TARGETS]),
                          value=self.node_analyze(node[Constants.VALUE]))

    def aug_assign_node(self, node):
        return ast.AugAssign(target=self.node_analyze(node[Constants.TARGET]),
                             op=self.bin_ops[node[Constants.OP]],
                             value=self.node_analyze(node[Constants.VALUE]))

    def get_targets_from_assign(self, targets):
        return [self.node_analyze(target) for target in targets]

    def dict_node(self, node):
        return ast.Dict(keys=[self.node_analyze(key) for key in node[Constants.KEYS]],
                        values=[self.node_analyze(value) for value in node[Constants.VALUES]])

    def return_node(self, node):
        return ast.Return(value=self.node_analyze(node[Constants.VALUE]))

    def call_node(self, node):
        return ast.Call(func=self.node_analyze(node[Constants.FUNC]),
                        args=self.get_nodes_from_list(node[Constants.ARGS]),
                        keywords=[])

    def attribute_node(self, node):
        return ast.Attribute(value=self.node_analyze(node[Constants.VALUE]),
                             attr=node[Constants.ATTR],
                             ctx=self.name_ctx[node[Constants.CTX]])

    def subscript_node(self, node):
        return ast.Subscript(value=self.name_node(node[Constants.VALUE]),
                             slice=self.node_analyze(node[Constants.SLICE]),
                             ctx=self.name_ctx[node[Constants.CTX]])

    def if_node(self, node):
        return ast.If(test=self.node_analyze(node[Constants.TEST]),
                      body=self.body_parse(node[Constants.BODY]),
                      orelse=self.body_parse(node[Constants.ORELSE]))

    def compare_node(self, node):
        return ast.Compare(left=self.node_analyze(node[Constants.LEFT]),
                           ops=self.get_comparison_ops(node[Constants.OPS]),
                           comparators=self.get_nodes_from_list(node[Constants.COMPARATORS]))

    def unary_op_node(self, node):
        return ast.UnaryOp(op=self.unary_ops[node[Constants.OP]],
                           operand=self.node_analyze(node[Constants.OPERAND]))

    def bin_op_node(self, node):
        return ast.BinOp(left=self.node_analyze(node[Constants.LEFT]),
                         op=self.bin_ops[node[Constants.OP]],
                         right=self.node_analyze(node[Constants.RIGHT]))

    def bool_op_node(self, node):
        return ast.BoolOp(op=self.bool_ops[node[Constants.OP]],
                          values=self.get_nodes_from_list(node[Constants.VALUES]))

    def get_comparison_ops(self, ops):
        return [self.comparison_ops[op] for op in ops]

    def for_node(self, node):
        return ast.For(target=self.node_analyze(node[Constants.TARGET]),
                       iter=self.node_analyze(node[Constants.ITER]),
                       body=self.body_parse(node[Constants.BODY]),
                       orelse=self.body_parse(node[Constants.ORELSE]))

    def tuple_node(self, node):
        return ast.Tuple(elts=self.get_nodes_from_list(node[Constants.ELTS]),
                         ctx=self.name_ctx[node[Constants.CTX]])

    def get_nodes_from_list(self, node_list):
        return [self.node_analyze(node) for node in node_list]

    def expr_node(self, node):
        return ast.Expr(value=self.node_analyze(node[Constants.VALUE]))

    def list_node(self, node):
        return ast.List(elts=self.get_nodes_from_list(node[Constants.ELTS]),
                        ctx=self.name_ctx[node[Constants.CTX]])

    def set_node(self, node):
        return ast.Set(elts=self.get_nodes_from_list(node[Constants.ELTS]))
