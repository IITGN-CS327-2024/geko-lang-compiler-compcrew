from lark import Lark
import ast_lexer_lark as lexer_lark
import sys
import os
# ----------------------------------------------------------------------------------------------------------------------------
import lark
import pydot
from typing import *
import rich
from ast_classes import *
import ast_final as geko_ast
from ast_grammar import grammar

# Define symbol table and symbol classes
class Symbol:
    def _init(self, name, type_):
        self.name = name
        self.type_ = type_

class VariableSymbol(Symbol):
    pass

class FunctionSymbol(Symbol):
    def _init(self, name, type, parameters):
        super()._init(name, type)
        self.parameters = parameters

class SymbolTable:
    symbols = {}
    def _init_(self):
        self.symbols = {}

    def add_symbol(self, name, symbol):
        if name in self.symbols:
            raise Exception(f"Duplicate symbol found: {name}")
        self.symbols[name] = symbol

    def lookup(self, name):
        return self.symbols.get(name)

# Define a basic semantic analyzer
class SemanticAnalyzer:
    symbol_table = SymbolTable()
    def _init_(self, symbol_table=None):
        self.symbol_table = symbol_table 

    def analyze(self, ast):
        self.visit(ast)

    def visit(self, node):
        if (node.__class__.__name__ != 'NoneType'):
            method_name = f'visit_{node.__class__.__name__}'
            visitor = getattr(self, method_name, self.generic_visit)
            return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{node.__class__.__name__} method defined")

    def visit_Program(self, node):
        self.visit(node.main_function)

    def visit_MainFunc(self, node):
        for statement in node.statements:
            self.visit(statement)

    # def visit_StatementList(self, node):
    #     for statement in node.statements:
    #         self.visit(statement)

    def visit_VariableDeclaration(self, node):
        tp = node.data_type
        print(tp)
        # if (tp == "None num") {
        #     tp = "int"
        # }
        identifier = node.variable_name
        self.symbol_table.add_symbol(identifier, VariableSymbol())
        type_rhs = 123242
        if (node.equal_to):
            val = node.equal_to
            print(val)
            if (val[1].__class__.__name__ == 'Term'):
                type_rhs = self.visit(val[1])
                print(type_rhs)
        print('#####################')
        print(type_rhs)
        print('#####################')
        if (tp != type_rhs):
            raise Exception(f"RHS value doesnot match the type of '{identifier}")
        # self.visit(node.equal_to)


    def visit_Assignment(self, node):
        identifier = node.identifier
        symbol = self.symbol_table.lookup(identifier)
        if symbol is None:
            raise Exception(f"Variable '{identifier}' not declared")
        self.visit(node.value)

    def visit_FunctionDefinition(self, node):
        name = node.identifier
        type_ = node.return_data[0]
        parameters = [(param.type_.type_, param.identifier) for param in node.parameter_list.parameters]
        self.symbol_table.add_symbol(name, FunctionSymbol(name, type_, parameters))
        for statement in node.statement_list:
            self.visit(statement)

    def visit_FunctionCall(self, node):
        name = node.identifier
        symbol = self.symbol_table.lookup(name)
        if symbol is None:
            raise Exception(f"Function '{name}' not declared")
        # Check argument types
        parameters = symbol.parameters
        if len(parameters) != len(node.expression):
            raise Exception(f"Function '{name}' expects {len(parameters)} arguments, but {len(node.expression)} provided")
        for arg, (param_type, _) in zip(node.expression, parameters):
            if arg.type_ != param_type:
                raise Exception(f"Argument type mismatch in function call to '{name}'")

    def visit_Expression(self, node):
        if (len(node.terms) == 2):
            left = self.visit(node.terms[0])
            right = 0
        if (node.operator_if_exists is not None):
            operator = node.operator_if_exists
            if operator in {'+', '-', '*', '/', '%'}:
                if left.type_ != 'int' or right.type_ != 'int':
                    raise Exception(f"Operands of arithmetic operator '{operator}' must be of type 'int'")
                # Assign the result type of the arithmetic expression as 'int'
                return VariableSymbol(None, 'int')

            elif operator in {'==', '!=', '<', '<=', '>', '>='}:
                if left.type_ != right.type_:
                    raise Exception(f"Operands of comparison operator '{operator}' must have the same type")
                # Assign the result type of the comparison expression as 'bool'
                return VariableSymbol(None, 'bool')

            elif operator in {'and', 'or', 'not'}:
                if left.type_ != 'bool' or right.type_ != 'bool':
                    raise Exception(f"Operands of boolean operator '{operator}' must be of type 'bool'")
                # Assign the result type of the boolean expression as 'bool'
                return VariableSymbol(None, 'bool')

    def visit_Factor(self, node):
        if node.factor[0] == 'identifier':
            symbol = self.symbol_table.lookup(node.factor[1])
            if symbol is None:
                raise Exception(f"Variable '{node.factor[1]}' not declared")
            return symbol
        elif node.factor[0] == 'number':
            return VariableSymbol(None, 'int')
        elif node.factor[0] == 'string':
            return VariableSymbol(None, 'str')
        elif node.factor[0] == 'true' or node.factor[0] == 'false':
            return VariableSymbol(None, 'bool')

    def visit_Condition(self, node):
        left_type = self.visit(node.left).type_
        right_type = self.visit(node.right).type_
      
        if left_type != right_type:
            raise Exception("Type mismatch in condition: Left and right operands must have the same type")

    def visit_IfStatement(self, node):
        self.visit(node.condition)
        self.visit(node.if_statement)
        for condition, statement_list in node.elif_statement:
            self.visit(condition)
            self.visit(statement_list)
        if node.else_statement:
            self.visit(node.else_statement)

    def visit_WhileStatement(self, node):
        self.visit(node.condition)
        self.visit(node.statement_list)

    def visit_TryExcept(self, node):
        self.visit(node.try_block)
        self.visit(node.except_block)

    def visit_Print(self, node):
        self.visit(node.value)
    
    def visit_Term(self, node):
        if (node.value):
            return (type(node.value))
        # value = node.value
        # print(type(value))
        identifier = node.identifier
        expression = self.visit(node.expression)
        unary_operator = node.unary_operator

    
        

    def visit_CompoundTypes(self, node):
        # Ensure the type of the compound data matches the declared type
        declared_type = node.compound_type
        for data_node in node.data:
            actual_type = self.visit(data_node).type_
            if declared_type != actual_type:
                raise Exception(f"Type mismatch in compound type: Expected {declared_type} but got {actual_type}")
    
    # def visit_NoneType

    # def visit_CompoundTypeAccess(self, node):
    #     # Check if the compound identifier exists and if the access is valid
    #     compound_symbol = self.symbol_table.lookup(node.identifier)
    #     if compound_symbol is None:
    #         raise Exception(f"Compound type '{node.identifier}' not declared")

    #     access_type = node.compound_type_access
    #     if isinstance(access_type, str):
    #         # Single identifier access
    #         if not isinstance(compound_symbol, CompoundSymbol):
    #             raise Exception(f"Cannot access field '{access_type}' in non-compound type '{node.identifier}'")
    #         if access_type not in compound_symbol.fields:
    #             raise Exception(f"Field '{access_type}' does not exist in compound type '{node.identifier}'")
    #     else:
    #         # Nested access
    #         nested_compound = self.visit_CompoundTypeAccess(access_type[1])
    #         if not isinstance(nested_compound, CompoundSymbol):
    #             raise Exception(f"Cannot access field '{access_type[0]}' in non-compound type '{nested_compound.name}'")
    #         if access_type[0] not in nested_compound.fields:
    #             raise Exception(f"Field '{access_type[0]}' does not exist in compound type '{nested_compound.name}'")

# Create the Lark parser
parser = Lark(grammar, start='start', parser = 'lalr')#, lexer = lexer_lark)

code = """
define num main() {
    num a = 5;
    str x = 6;
    yield 0;
}
"""

# parser_lark_dir = os.path.dirname(__file__)

tokens = lexer_lark.lexer(code)

# ----------------------------------------------------------------------------------------------------------------------------

tokenised_code = ""

for token in tokens:
    # print(type(token[0]))
    tokenised_code += token[0] + " "

#---------------------------------------

tree = parser.parse(tokenised_code)

# graph_of_tree = lark.tree.pydot__tree_to_graph(tree)
graph = pydot.graph_from_dot_data(lark.tree.pydot__tree_to_graph(tree).to_string())
# Final function to be used: 
geko_ast.final_iteration(tree, tokens, graph=graph[0])
ast_builder = geko_ast.ASTBuilder()
rich.print(tree)
# print(tree)
ast = ast_builder.transform(tree)
rich.print(ast)
try:
    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.analyze(ast)  # Pass your AST root here
    print('Semantically Correct!')
except EOFError:
    print("File could not be opened!")