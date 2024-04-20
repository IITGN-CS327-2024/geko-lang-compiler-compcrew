from ast_final import *
from ast_classes import *

class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        # Initializes the symbol table stack with a global scope
        self.scopes = [{}]

    def enter_scope(self):
        # Enter a new scope by adding a scope to the stack
        self.scopes.append({})

    def exit_scope(self):
        # Exit a scope by popping the scope stack
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise SemanticError("Trying to exit the global scope")

    def declare_variable(self, name, data_type):
        # Declare a variable in the current scope
        if name in self.scopes[-1]:
            raise SemanticError(f"Variable '{name}' already declared in this scope")
        self.scopes[-1][name] = data_type

    def check_variable_declared(self, name):
        # Check if a variable is declared in any accessible scope
        for scope in reversed(self.scopes):
            if name in scope:
                return True
        raise SemanticError(f"Variable '{name}' not declared")

    def visit_VariableDeclaration(self, node):
        self.declare_variable(node.variable_name, node.data_type)

    def visit_UnaryStatement(self, node):
        self.check_variable_declared(node.value)

    def visit_Assignment(self, node):
        self.check_variable_declared(node.variable_name)

    def visit_ConditionalStatement(self, node):
        self.enter_scope()
        self.visit(node.conditional_argument.expression)
        for statement in node.conditional_block.statements:
            self.visit(statement)
        self.exit_scope()

    def visit(self, node):
        # General visit method that calls specific methods based on node type
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # Generic visit method for all unhandled node types
        raise NotImplementedError(f"No visit method defined for {type(node).__name__}")

    def visit_Program(self, node):
        # Visit the main function and any function definitions
        self.visit(node.main_function)
        for func in node.function_defs:
            self.visit(func)

    def visit_MainFunc(self, node):
        self.enter_scope()
        for statement in node.statements:
            if statement:
                self.visit(statement)
        self.exit_scope()

    def visit_FunctionDef(self, node):
        self.enter_scope()
        for statement in node.statements:
            self.visit(statement)
        self.exit_scope()

    def visit_VariableDeclaration(self, node):
        self.declare_variable(node.variable_name, node.data_type)
    
    def visit_Expression(self, node):
        for term in node.terms:
            self.visit(term)
    
    def visit_Term(self, node):
        if node.identifier:
            self.check_variable_declared(node.identifier)

    def visit_NoneType(self, node):
        pass
    

# Assuming 'ast' is an instance of your AST class Program
# ast = Program(
#     function_defs=[],
#     main_function=MainFunc(
#         statements=[
#             VariableDeclaration(
#                 data_type='None num',
#                 variable_name='a',
#                 size_array=None,
#                 equal_to=[BinaryOperator(operator=None), Term(value='hello', identifier=None, expression=None, pre_unary_operator=None, post_unary_operator=None), None]
#             ),
#             Assignment(
#                 variable_name='a',
#                 assignment_operators='=',
#                 value=Expression(operator_if_exists=None, terms=[Term(value=5, identifier=None, expression=None, pre_unary_operator=None, post_unary_operator=None), None])
#             ),
#             ConditionalStatement(
#                 conditional_argument=ConditionalArgument(
#                     is_special=None,
#                     comparison_operator=None,
#                     expression=Expression(
#                         operator_if_exists=None,
#                         terms=[
#                             Term(value=None, identifier='a', expression=None, pre_unary_operator=None, post_unary_operator=None),
#                             Expression(operator_if_exists='==', terms=[Term(value=4, identifier=None, expression=None, pre_unary_operator=None, post_unary_operator=None), None])
#                         ]
#                     )
#                 ),
#                 conditional_block=Block(statements=[UnaryStatement(pre_unary_operator=None, value='b', post_unary_operator='++'), None]),
#                 other_blocks=[],
#                 otherwise_block=OtherwiseBlock(conditional_block=[])
#             ),
#             None
#         ]
#     )
# )

analyzer = SemanticAnalyzer()
try:
    analyzer.visit(ast)
    print("Semantic analysis completed successfully.")
except SemanticError as e:
    print(f"Semantic error: {e}")
