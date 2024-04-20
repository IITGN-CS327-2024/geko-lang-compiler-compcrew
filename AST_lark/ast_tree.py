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
        for stmt in node.statements[:-1]:
            main_func_node.children.append(build_tree(stmt))
        return main_func_node
    elif isinstance(node, ShowStatement):
        show_node = TreeNode("Show")
        for expr in node.expressions:
            show_node.children.append(build_tree(expr))
        return show_node
    elif isinstance(node, EnterStatement):
        enter_node = TreeNode("Enter")
        enter_node.children.append(TreeNode(node.string))
        enter_node.children.append(TreeNode(node.enter_value))
        return enter_node
    elif isinstance(node, Array):
        array_node = TreeNode("Array")
        array_node.children.append(build_tree(node.size))
        return array_node
    elif isinstance(node, VariableDeclaration):
        var_decl_node = TreeNode("VariableDeclaration")
        var_decl_node.children.append(TreeNode(f"{node.data_type}"))
        var_decl_node.children.append(TreeNode(f"{node.variable_name}"))
        if node.size_array is not None:
            var_decl_node.children.append(TreeNode(f"{node.size_array}"))
        if node.equal_to:
            if (type(node.equal_to) is list):
                if (node.equal_to[0].__class__.__name__ == 'EnterStatement'):
                    var_decl_node.children.append(build_tree(node.equal_to[0]))
                elif (len(node.equal_to) == 3):
                    for elements in node.equal_to:
                        if elements is not None:
                            equal_to_subtree = build_tree(elements)
                            if equal_to_subtree is not None:
                                var_decl_node.children.append(equal_to_subtree)
                else:
                    expr = TreeNode("Equation")
                    var_decl_node.children.append(expr)
                    for elements in node.equal_to:
                        if elements is not None:
                            equal_to_subtree = build_tree(elements)
                            if equal_to_subtree is not None:
                                expr.children.append(TreeNode(equal_to_subtree))
            else:
                var_decl_node.children.append(build_tree(node.equal_to))
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
        # op_node = TreeNode("NoOp")
        if node.operator_if_exists:
            print("operator_if_exists mai hai hum ab")
            # expr_node.children.append(TreeNode(f"Operator: {node.operator_if_exists}"))
            op_node = TreeNode("BinOp")
            op_node = TreeNode(node.operator_if_exists)
            for term in node.terms:
                op_node.children.append(build_tree(term))
            return op_node
        else:
            # print("operator_if_exists mai nahi hai hum ab")
            for term in node.terms:
                return build_tree(term)
        #     expr_node.children.append(build_tree(term))
    elif isinstance(node, Term):
        if node.value:
            return node.value
        elif node.identifier:
            return node.identifier
        # elif node.expression:
        #     return build_tree(node.expression)
    elif isinstance(node, ConditionalStatement):
        cond_node = TreeNode("Conditions")
        cond_node.children.append(build_tree(node.conditional_argument))
        cond_node.children.append(build_tree(node.conditional_block))
        for other in node.other_blocks:
            cond_node.children.append(build_tree(other))
        cond_node.children.append(build_tree(node.otherwise_block))
        return cond_node
    elif isinstance(node, ConditionalArgument):
        inside_given_node = TreeNode("GivenArg")
        if node.is_special is not None:
            print("CompCrew")
        if node.comparison_operator is not None:
            print("CompCrew1")
        if node.expression is not None:
            inside_given_node.children.append(build_tree(node.expression))
        return inside_given_node
    elif isinstance(node, BinaryOperator):
        # bin_op_node = TreeNode("BinaryOperator")
        # bin_op_node.children.append(TreeNode(f"operator: {node.operator}"))
        if node.operator is not None:
            return node.operator
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
