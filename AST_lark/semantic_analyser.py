from ast_final import *
from ast_classes import *

class SemanticError(Exception):
    pass

dict_of_types = { 
    'int':'num',
    'str':'str',
    'list':'list',
    'tuple':'tup',
    'bool':'flag'
}

                
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

    def declare_variable(self, name, data_type, mutability):
        # Declare a variable in the current scope
        if name in self.scopes[-1]:
            raise SemanticError(f"Variable '{name}' already declared in this scope")
        self.scopes[-1][name] = {'type': data_type, 'mutability': mutability}

    def check_variable_declared(self, name):
        # Check if a variable is declared in any accessible scope
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise SemanticError(f"Variable '{name}' not declared")

    def type_of_expression(self, expression):
        if isinstance(expression, str):
            if expression.startswith('~') and expression.endswith('~'):
                return 'string'
            else:
                # Handling direct variable name references
                var_info = self.check_variable_declared(expression)
                return var_info['type']
        elif isinstance(expression, UnaryOperator):
            operand_type = self.type_of_expression(expression.operand)
            return operand_type
        # elif isinstance(expression, Term):
        elif expression.__class__.__name__ == 'Term':
            if expression.value:
                print(type(expression.value))
                return type(expression.value).__name__
            if expression.expression:
                return self.type_of_expression(expression.expression)
            if expression.identifier:
                var_info = self.check_variable_declared(expression.identifier)
                return var_info['type']
            # else:
            #     return self.type_of_expression(expression.value)
        elif expression.__class__.__name__ == "Expression":
            expr_type_list = []
            for term in expression.terms:
                if term:
                    temp = self.type_of_expression(term)
                    expr_type_list.append(temp)
            return expr_type_list
        elif isinstance(expression, BinaryOperator):
            # Handle binary operations like +, -, *, etc.
            # You need to determine the resulting type based on the operation
            # This is a simplified example and might need adjustment based on your language's rules
            left_type = self.type_of_expression(expression.left)
            right_type = self.type_of_expression(expression.right)
            # Assuming for simplicity that the result type is the same as the operand type
            return left_type if left_type == right_type else None
        elif isinstance(expression, (int, float)):
            return 'num'
    # Add more comprehensive handling here based on your expression AST node types

    # You should add more comprehensive handling here based on your expression AST node types


    def visit_VariableDeclaration(self, node):
        # node.data_type might contain "None num", "let num", or "fix num"
        mutability, type_name = node.data_type.split()
        print(mutability)
        print(type_name)
        print(node.equal_to)
        test_lst = []
        for i in node.equal_to[:-1]:
            if (isinstance(i, Term)):
                print(1)
                expr_type = self.type_of_expression(i)
                test_lst.append(expr_type)
        # change expr_type according to dict_of_types
        print('###################################')
        print(len(test_lst))
        print(test_lst)
        test_lst = flatten_list(test_lst)
        print(test_lst)
        print('###################################')
        for i in range(len(test_lst)):
            # print(j)
            print(dict_of_types['int'])
            print(2)
            # if j in dict_of_types:
            #     j = dict_of_types[j]
            if test_lst[i] == 'int':
                test_lst[i] = dict_of_types['int']
            elif test_lst[i] == 'str':
                test_lst[i] = dict_of_types['str']
            elif test_lst[i] == 'bool':
                test_lst[i] = dict_of_types['bool']
            if test_lst[i] != type_name:
                raise SemanticError(f"Type mismatch: variable '{node.variable_name}' declared as '{type_name}' but assigned '{test_lst[i]}'")
        print(test_lst)
        self.declare_variable(node.variable_name, type_name, mutability)

    def visit_UnaryStatement(self, node):
        self.check_variable_declared(node.value)

    def visit_Assignment(self, node):
        var_info = self.check_variable_declared(node.variable_name)
        expr_type = self.type_of_expression(node.value)
        if expr_type != var_info['type']:
            raise SemanticError(f"Type mismatch: variable '{node.variable_name}' expected '{var_info['type']}' but got '{expr_type}'")
        if var_info['mutability'] == 'fix':
            raise SemanticError(f"Cannot assign to constant variable '{node.variable_name}'")
        
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

    # def visit_VariableDeclaration(self, node):
    #     self.declare_variable(node.variable_name, node.data_type)
    
    def visit_Expression(self, node):
        for term in node.terms:
            self.visit(term)
    
    def visit_Term(self, node):
        if node.identifier:
            self.check_variable_declared(node.identifier)

    def visit_NoneType(self, node):
        pass

analyzer = SemanticAnalyzer()
try:
    analyzer.visit(ast)
    print("Semantic analysis completed successfully.")
except SemanticError as e:
    print(f"Semantic error: {e}")
