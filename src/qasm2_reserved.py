"""
To improve robustness and ensure compliance with QASM2 syntax,
extra dialect might be added which would allow to automatically detection naming conflicts with reserved QASM2
keywords—such as qreg, creg, gate, or measure. When detected the node transformer can be used to rename conflicting
 identifiers to ensure that generated QASM2 is valid. This approach would increase reliability of the QASM2 outputs.
"""

import ast


def qasm_safe_renaming(tree, config=None):
    """
    Kirin-style dialect that renames Python variable names
    conflicting with QASM2 reserved words.
    """
    if config is None:
        config = {}

    reserved = {
        "qreg",
        "creg",
        "gate",
        "measure",
        "reset",
        "barrier",
        "opaque",
        "if",
        "else",
        "pi",
        "sin",
        "cos",
        "tan",
        "exp",
        "ln",
        "sqrt",
        "include",
        "openqasm",
        "qasm",
    }

    suffix = config.get("suffix", "_var")

    class RenameVisitor(ast.NodeTransformer):
        def __init__(self):
            self.renamed = {}

        def rename_if_reserved(self, name):
            if name in reserved:
                new_name = f"{name}{suffix}"
                self.renamed[name] = new_name
                return new_name
            return name

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store | ast.Load):
                node.id = self.renamed.get(node.id, self.rename_if_reserved(node.id))
            return node

        def visit_arg(self, node):
            node.arg = self.renamed.get(node.arg, self.rename_if_reserved(node.arg))
            return node

        def visit_FunctionDef(self, node):
            node.name = self.renamed.get(node.name, self.rename_if_reserved(node.name))
            self.generic_visit(node)
            return node

        def visit_ClassDef(self, node):
            node.name = self.renamed.get(node.name, self.rename_if_reserved(node.name))
            self.generic_visit(node)
            return node

    return RenameVisitor().visit(tree)


example_code = """
def gate(qreg, pi):
    creg = qreg + 1
    return creg + pi
"""

tree = ast.parse(example_code)

transformed_tree = qasm_safe_renaming(tree, config={"suffix": "_var"})

print("= Transformed Code =")
print(ast.unparse(transformed_tree))
