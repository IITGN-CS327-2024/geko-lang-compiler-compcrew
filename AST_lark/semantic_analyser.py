from ast_final import *
from ast_classes import *

# defining the stack for pushing and popping the scopes
# and variable names in the semantic analyser

# class Scope:
#     def __init__(self):
#         self.variables = {}
#         self.functions = {}
#         self.types = {}
#         self.parent = None
#         self.children = []

#     def add_variable(self, name, value):
#         self.variables[name] = value

#     def add_function(self, name, value):
#         self.functions[name] = value

#     def add_type(self, name, value):
#         self.types[name] = value

#     def get_variable(self, name):
#         if name in self.variables:
#             return self.variables[name]
#         elif self.parent is not None:
#             return self.parent.get_variable(name)
#         else:
#             return None

#     def get_function(self, name):
#         if name in self.functions:
#             return self.functions[name]
#         elif self.parent is not None:
#             return self.parent.get_function(name)
#         else:
#             return None

#     def get_type(self, name):
#         if name in self.types:
#             return self.types[name]
#         elif self.parent is not None:
#             return self.parent.get_type(name)
#         else:
#             return None

#     def add_child(self, child):
#         self.children.append(child)
#         child.parent = self

#     def __str__(self):
#         return f"Scope: {self.variables}, {self.functions}, {self.types}"


class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        print(f"Visiting {type(node).__name__}")
        print(f"Visitor: {visitor}")
        
        if visitor is None:
            raise SemanticError(f"No visit_{type(node).__name__} method")
        return visitor(node)

    def generic_visit(self, node):
        # print(f"No visit_{type(node).__name__} method")
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_NoneType(self, node):
        pass

    def visit_Program(self, node):
        for func_def in node.function_defs:
            self.visit(func_def)
        self.visit(node.main_function)

    def visit_MainFunc(self, node):
        for statement in node.statements:
            if statement is not None:
                self.visit(statement)

    def visit_VariableDeclaration(self, node):
        # Check if the variable is already declared
        if node.variable_name in self.symbol_table:
            raise SemanticError(f"Variable '{node.variable_name}' is already declared.")
        
        # Add the variable to the symbol table with its type
        self.symbol_table[node.variable_name] = node.data_type
        
        # If there's an initialization, check it
        if node.equal_to is not None:
            self.visit(node.equal_to)

    def visit_BinaryOperator(self, node):
        # left_value = self.visit(node.left)
        # right_value = self.visit(node.right)
        # Example check: both operands must be of integer type
        # if not isinstance(left_value, int) or not isinstance(right_value, int):
        #     raise SemanticError("Binary operation requires integer operands.")
        
        # # Implement operation logic based on the operator
        # if node.operator == '+':
        #     return left_value + right_value
        # elif node.operator == '-':
        #     return left_value - right_value
        # Add other operators as needed
        return node.operator

    def visit_Term(self, node):
        if node.value is not None:
            return node.value  # Assuming value is an integer for simplicity
        elif node.identifier is not None:
            if node.identifier not in self.symbol_table:
                raise SemanticError(f"Variable '{node.identifier}' not declared.")
            return self.symbol_table[node.identifier]
        else:
            # If it's a complex expression, further processing needed
            return self.visit(node.expression)
    def visit_Assignment(self, node):
        # Check if the variable is declared
        if node.variable_name not in self.symbol_table:
            raise SemanticError(f"Variable '{node.variable_name}' not declared.")
        
        # Check if the variable is being assigned a valid value
        self.visit(node.value)


    def visit_Expression(self, node):
        for term in node.terms:
            self.visit(term)

    def visit_ConditionalArgument(self, node):
        self.visit(node.expression.terms)

    def visit_ConditionalStatement(self, node):
        self.visit(node.conditional_argument)
        self.visit(node.conditional_block)
        for block in node.other_blocks:
            self.visit(block)
        self.visit(node.otherwise_block)

    def visit_Block(self, node):
        for statement in node.statements:
            self.visit(statement)
    
    def visit_UnaryStatement(self, node):
        # return node.value + 1 if node.post_unary_operator == '++' else node.value - 1 if node.post_unary_operator == '--' else node.value
        pass

    def visit_OtherwiseBlock(self, node):
        self.visit(node.conditional_block)

    def visit_list(self, node):
        for item in node:
            self.visit(item)
# Assuming 'ast' is an instance of your AST class Program
ast = Program(
    function_defs=[],
    main_function=MainFunc(
        statements=[
            VariableDeclaration(
                data_type='None num',
                variable_name='a',
                size_array=None,
                equal_to=[BinaryOperator(operator=None), Term(value='hello', identifier=None, expression=None, pre_unary_operator=None, post_unary_operator=None), None]
            ),
            Assignment(
                variable_name='a',
                assignment_operators='=',
                value=Expression(operator_if_exists=None, terms=[Term(value=5, identifier=None, expression=None, pre_unary_operator=None, post_unary_operator=None), None])
            ),
            ConditionalStatement(
                conditional_argument=ConditionalArgument(
                    is_special=None,
                    comparison_operator=None,
                    expression=Expression(
                        operator_if_exists=None,
                        terms=[
                            Term(value=None, identifier='a', expression=None, pre_unary_operator=None, post_unary_operator=None),
                            Expression(operator_if_exists='==', terms=[Term(value=5, identifier=None, expression=None, pre_unary_operator=None, post_unary_operator=None), None])
                        ]
                    )
                ),
                conditional_block=Block(statements=[UnaryStatement(pre_unary_operator=None, value='a', post_unary_operator='++'), None]),
                other_blocks=[],
                otherwise_block=OtherwiseBlock(conditional_block=[])
            ),
            None
        ]
    )
)

analyzer = SemanticAnalyzer()
try:
    analyzer.visit(ast)
    print("Semantic analysis completed successfully.")
except SemanticError as e:
    print(f"Semantic error: {e}")
