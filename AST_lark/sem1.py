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
import ast_tree as astt


symbol_count = 0
symbol_table = []

# Define the typ of the variable
from enum import Enum

class Type(Enum):
    NUMBER_TYPE = 1
    STRING_TYPE = 2
    BOOL_TYPE = 3
    LIST_TYPE = 4
    TUPLE_TYPE = 5
    NODE_TYPE = 6
    UNKNOWN_TYPE_PARAM = 7
    UNKNOWN_TYPE = 8

# Symbol table entry
class SymbolTableEntry:
    def __init__(self, name, typ, scope):
        self.name = name
        self.typ = typ
        self.scope = scope

# Symbol table
symbol_table = [None] * 10

def lookup_symbol(name):
    if name is None:
        return -1
    for i, symbol in enumerate(symbol_table):
        if symbol and symbol.name == name:
            return i
    return -1

def lookup_symbol_in_scope(name, scope):
    if name is None:
        return -1
    for i, symbol in enumerate(symbol_table):
        if symbol and symbol.name == name and symbol.scope == scope:
            return i
    return -1

def add_symbol(name, typ, scope):
    global symbol_count
    symbol = SymbolTableEntry(name, typ, scope)
    index = lookup_symbol(name)
    if index == -1:
        symbol_table[symbol_count] = symbol
        symbol_count += 1
    else:
        symbol_table[index] = symbol

# Example usage:
# add_symbol("variable1", "int", "global")
# add_symbol("variable2", "float", "local")

def semantic_analyze(node, current_scope):
    if node is None:
        return Type.UNKNOWN_TYPE

    if isinstance(node, str):
        str1 = node
    else:
        str1 = node.label
    print(str1)

    if str1 == 'VariableDeclaration':
        add_symbol(node.children[1],node.children[0],'global')
        print(type(node.children[1].label))
        if  len(node.children) > 2:
            print(type(node.children[2].label),"= hona chahiye =", node.children[0].label.split()[1], "meow moew")
            if node.children[0].label.split()[1] == "num": 
                if type(node.children[2].label) != int:
                    raise Exception('Type mismatch on variable declaration')
            else:
                if type(node.children[2].label) == int:
                    raise Exception('Type mismatch on variable declaration')
            # if (type(node.children[2].label) != node.children[0].label.split()[1]):

    if str1 == "assignment":
        lhs = node.children[0]
        rhs = node.children[1]

        if lhs.typ == "index":
            index = lookup_symbol_in_scope(lhs.children[0].value, current_scope)
            if index == -1:
                index = lookup_symbol_in_scope(lhs.children[0].value, "global")
                if index == -1:
                    print(f"Error: Variable {lhs.children[0].value} not declared")
                    exit(1)

            if symbol_table[index].typ == Type.UNKNOWN_TYPE_PARAM:
                symbol_table[index].typ = Type.LIST_TYPE

            if symbol_table[index].typ != Type.LIST_TYPE:
                print(f"Error: Variable {lhs.children[0].value} is not a list")
                exit(1)

            semantic_analyze(lhs.children[1], current_scope)
            return Type.NODE_TYPE

        index = lookup_symbol_in_scope(lhs.value, current_scope)
        typ = semantic_analyze(rhs, current_scope)

        if index != -1:
            symbol_table[index].typ = typ
            return symbol_table[index].typ

        add_symbol(lhs.value, typ, current_scope)
        return Type.NODE_TYPE

    elif str1 == "function":
        function_name = node.children[0].value
        index = lookup_symbol_in_scope(function_name, current_scope)

        if index != -1:
            print(f"Error: Function {function_name} already declared")
            exit(1)

        add_symbol(function_name, Type.UNKNOWN_TYPE, current_scope)

        for i in range(1, len(node.children)):
            semantic_analyze(node.children[i], function_name)

        return Type.NODE_TYPE

    elif str1 == "parameters":
        if len(node.children) == 2:
            add_symbol(node.children[0].value, Type.UNKNOWN_TYPE_PARAM, current_scope)
            typ = semantic_analyze(node.children[0], current_scope)
            index = lookup_symbol_in_scope(node.children[0].value, current_scope)
            symbol_table[index].typ = typ
            semantic_analyze(node.children[1], current_scope)
            return Type.NODE_TYPE

        add_symbol(node.children[0].value, Type.UNKNOWN_TYPE_PARAM, current_scope)
        typ = semantic_analyze(node.children[0], current_scope)
        index = lookup_symbol_in_scope(node.children[0].value, current_scope)
        symbol_table[index].typ = typ
        return Type.NODE_TYPE

    elif str1 == "return":
        typ = semantic_analyze(node.children[0], current_scope)
        index = lookup_symbol(current_scope)
        print("typ:", typ)
        symbol_table[index].typ = typ
        return Type.NODE_TYPE

    elif str1 == "function_call":
        index = lookup_symbol_in_scope(node.children[0].value, current_scope)

        if index == -1:
            index = lookup_symbol_in_scope(node.children[0].value, "global")

            if index == -1:
                print(f"Error: Function {node.children[0].value} not declared")
                exit(1)

        print("index:", index)
        typ = symbol_table[index].typ

        for i in range(1, len(node.children)):
            semantic_analyze(node.children[i], current_scope)

        return typ

    elif str1 in ("and", "or", "not", "equal_equal", "not_equal", "less", "less_equal", "greater", "greater_equal"):
        for child in node.children:
            semantic_analyze(child, current_scope)
        return Type.BOOL_TYPE

    elif str1 in ("plus", "minus", "times", "divide", "modulo"):
        left = semantic_analyze(node.children[0], current_scope)
        right = semantic_analyze(node.children[1], current_scope)

        if left == Type.UNKNOWN_TYPE_PARAM:
            index = lookup_symbol_in_scope(node.children[0].children[0].value, current_scope)
            symbol_table[index].typ = Type.NUMBER_TYPE
            left = Type.NUMBER_TYPE

        if right == Type.UNKNOWN_TYPE_PARAM:
            index = lookup_symbol_in_scope(node.children[1].value, current_scope)
            symbol_table[index].typ = Type.NUMBER_TYPE
            right = Type.NUMBER_TYPE

        if left != Type.NUMBER_TYPE or right != Type.NUMBER_TYPE:
            print("Error: Incompatible typs")
            exit(1)

        return Type.NUMBER_TYPE

    elif str1 == "term":
        return semantic_analyze(node.children[0], current_scope)

    elif str1 == "string":
        return Type.STRING_TYPE

    elif str1 == "tuple":
        semantic_analyze(node.children[0], current_scope)
        return Type.TUPLE_TYPE

    elif str1 == "list":
        semantic_analyze(node.children[0], current_scope)
        return Type.LIST_TYPE

    elif str1 == "index":
        index = lookup_symbol_in_scope(node.children[0].value, current_scope)

        if index == -1:
            index = lookup_symbol_in_scope(node.children[0].value, "global")
            if index == -1:
                print(f"Error: Variable {node.children[0].value} not declared")
                exit(1)

        if symbol_table[index].typ == Type.UNKNOWN_TYPE_PARAM:
            symbol_table[index].typ = Type.LIST_TYPE

        if symbol_table[index].typ != Type.LIST_TYPE:
            print(f"Error: Variable {node.children[0].value} is not a list")
            exit(1)

        semantic_analyze(node.children[1], current_scope)
        return Type.NUMBER_TYPE

    elif str1 == "for":
        add_symbol(node.children[0].value, Type.NUMBER_TYPE, current_scope)
        semantic_analyze(node.children[1], current_scope)
        semantic_analyze(node.children[2], current_scope)
        return Type.NODE_TYPE

    elif str1 == "range":
        lhs = semantic_analyze(node.children[0], current_scope)
        rhs = semantic_analyze(node.children[1], current_scope)

        if lhs == Type.UNKNOWN_TYPE_PARAM:
            index = lookup_symbol_in_scope(node.children[0].children[0].value, current_scope)
            symbol_table[index].typ = Type.NUMBER_TYPE
            lhs = Type.NUMBER_TYPE

        if rhs == Type.UNKNOWN_TYPE_PARAM:
            index = lookup_symbol_in_scope(node.children[1].value, current_scope)
            symbol_table[index].typ = Type.NUMBER_TYPE
            rhs = Type.NUMBER_TYPE

        if lhs != Type.NUMBER_TYPE or rhs != Type.NUMBER_TYPE:
            print("Error: Wrong typs for looping object")
            exit(1)

        return Type.NODE_TYPE

    elif str1 == "factor":
        semantic_analyze(node.children[0], current_scope)
        index = lookup_symbol_in_scope(node.children[0].value, current_scope)

        if symbol_table[index].typ != Type.NUMBER_TYPE:
            symbol_table[index].typ = Type.NUMBER_TYPE

        return Type.NUMBER_TYPE

    elif str1 == "identifier":
        index = lookup_symbol_in_scope(node.value, current_scope)

        if index == -1:
            index = lookup_symbol_in_scope(node.value, "global")
            if index == -1:
                print(f"Error: Variable {node.value} not declared")
                exit(1)

        return symbol_table[index].typ

    elif str1 == "number":
        return Type.NUMBER_TYPE

    else:
        if type(node) != str:
            for child in node.children:
                semantic_analyze(child, current_scope)
        else:
            return Type.NODE_TYPE

        return Type.NODE_TYPE
    
# Create the Lark parser
parser = Lark(grammar, start='start', parser = 'lalr')#, lexer = lexer_lark)

code = """
define num main() {

    yield 0;
}
"""

# parser_lark_dir = os.path.dirname(__file__)

tokens = lexer_lark.lexer(code)

# ----------------------------------------------------------------------------------------------------------------------------

tokenised_code = ""

for token in tokens:
    # print(typ(token[0]))
    tokenised_code += token[0] + " "

#---------------------------------------

tree = parser.parse(tokenised_code)

# graph_of_tree = lark.tree.pydot__tree_to_graph(tree)
graph = pydot.graph_from_dot_data(lark.tree.pydot__tree_to_graph(tree).to_string())
# Final function to be used: 
geko_ast.final_iteration(tree, tokens, graph=graph[0])
ast_builder = geko_ast.ASTBuilder()
# rich.print(tree)
# print(tree)
ast = ast_builder.transform(tree)

def print_symbol_table():
    print("Symbol Table")
    print("------------")
    for symbol in symbol_table:
        if symbol is not None:
            print(type(symbol.typ))
            print("Name:", symbol.name.label, "\t Type:", symbol.typ.label, "\t Scope:", symbol.scope)
    print()

# Define the global scope or other initial scope
current_scope = "global"

# Traverse the AST and perform semantic analysis
# def traverse_and_analyze(node, current_scope):
#     print(node)
#     for child in node.children:
#         traverse_and_analyze(child, current_scope)
semantic_analyze(astt.tree_root, current_scope)
print_symbol_table()
# traverse_and_analyze(ast, global_scope)