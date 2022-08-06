from _ast import AST


def convert_to_json(node):
    assert isinstance(node, AST)
    to_return = dict()
    class_name = node.__class__.__name__
    if class_name in ["Load", "Store", "Delete", "Eq", "NotEq", "Lt", "LtE",
                      "Gt", "GtE", "Is", "IsNot", "In", "NotIn", "UAdd",
                      "USub", "Not", "Invert", "Add", "Sub", "Mult", "Div",
                      "FloorDiv", "Mod", "Pow", "And", "Or"]:
        return class_name
    to_return["ast_type"] = class_name
    for attr in dir(node):
        if attr.startswith("_") or attr in ["col_offset", "end_col_offset", "lineno", "end_lineno",
                                            "type_comment", "type_ignores", "returns", "dims",
                                            "posonlyargs", "kwonlyargs", "kw_defaults", "kwarg",
                                            "vararg", "annotation", "n", "s", "kind"]:
            continue
        to_return[attr] = get_value(getattr(node, attr))
    return to_return


def get_value(attr_value):
    if attr_value is None:
        return attr_value
    if isinstance(attr_value, (int, float, bool, str)):
        return attr_value
    if isinstance(attr_value, list):
        return [get_value(x) for x in attr_value]
    if isinstance(attr_value, AST):
        return convert_to_json(attr_value)
