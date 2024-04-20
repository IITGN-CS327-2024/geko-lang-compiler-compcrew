from rich import print
from ast_final import *

class TreeNode:
    def __init__(self, label):
        self.label = label
        self.children = []

def build_tree(node):
    if isinstance(node, Program):
        root = TreeNode("Program")
        root.children.append(build_tree(node.main_function))
        return root
    elif isinstance(node, MainFunc):
        main_func_node = TreeNode("MainFunc")
        for stmt in node.statements:
            main_func_node.children.append(build_tree(stmt))
        return main_func_node
    elif isinstance(node, Array):
        array_node = TreeNode("Array")
        array_node.children.append(build_tree(node.size))
        return array_node
    elif isinstance(node, VariableDeclaration):
        var_decl_node = TreeNode("VariableDeclaration")
        var_decl_node.children.append(TreeNode(f"{node.data_type}"))
        var_decl_node.children.append(TreeNode(f"{node.variable_name}"))
        if node.size_array:
            var_decl_node.children.append(TreeNode(f"{node.size_array}"))
        if node.equal_to:
            equal_to_subtree = build_tree(node.equal_to)
            print("equal_to_subtree mai hai hum ab")
            var_decl_node.children.append(equal_to_subtree)
        # if node.initial_value:
        #     var_decl_node.children.append(build_tree(node.initial_value))
        # if node.equal_to:
        #     var_decl_node.children.append(TreeNode(build_tree(node.equal_to)))
        return var_decl_node
    elif isinstance(node, Assignment):
        assignment_node = TreeNode("Assignment")
        assignment_node.children.append(TreeNode(f"variable_name: {node.variable_name}"))
        assignment_node.children.append(TreeNode(f"assignment_operators: {node.assignment_operators}"))
        assignment_node.children.append(build_tree(node.value))
        return assignment_node
    elif isinstance(node, Expression):
        # expr_node = TreeNode("Expression")
        op_node = TreeNode("NoOp")
        if node.operator_if_exists:
            print("operator_if_exists mai hai hum ab")
            # expr_node.children.append(TreeNode(f"Operator: {node.operator_if_exists}"))
            op_node = TreeNode("BinOp")
            op_node = TreeNode(node.operator_if_exists)
            for term in node.terms:
                op_node.children.append(build_tree(term))
            return op_node
        else:
            print("operator_if_exists mai nahi hai hum ab")
            for term in node.terms:
                op_node.children.append(build_tree(term))
            return op_node
        #     expr_node.children.append(build_tree(term))
    elif isinstance(node, Term):
        # term_node = TreeNode("Term")
        # if node.value:
        #     term_node.children.append(TreeNode(f"value: {node.value}"))
        # if node.identifier:
        #     term_node.children.append(TreeNode(f"identifier: {node.identifier}"))
        # if node.expression:
        #     term_node.children.append(build_tree(node.expression))
        # if node.unary_operator:
        #     term_node.children.append(TreeNode(f"unary_operator: {node.unary_operator}"))
        # return term_node
        if node.value:
            return node.value
        elif node.identifier:
            return node.identifier
        elif node.expression:
            return build_tree(node.expression)
    elif isinstance(node, BinaryOperator):
        bin_op_node = TreeNode("BinaryOperator")
        bin_op_node.children.append(TreeNode(f"operator: {node.operator}"))
        return bin_op_node
    elif isinstance(node, UnaryOperator):
        unary_op_node = TreeNode("UnaryOperator")
        unary_op_node.children.append(TreeNode(f"operator: {node.operator}"))
        return unary_op_node
    else:
        return TreeNode(str(node))

def print_tree(node, indent=0):
    if type(node) is not TreeNode:
        print(" " * indent, node)
        return
    print(" " * indent, node.label)
    for child in node.children:
        print_tree(child, indent + 4)

# Assuming 'ast' is the root node of your Abstract Syntax Tree (AST)
tree_root = build_tree(ast)
print_tree(tree_root)
