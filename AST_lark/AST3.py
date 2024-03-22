from lark import Lark
from lark.lexer import Lexer, Token
from lark.exceptions import UnexpectedToken
import re
import ast_lexer as lexer_lark
import sys
import os
# ----------------------------------------------------------------------------------------------------------------------------
import lark
import pydot
from IPython.display import display
# ----------------------------------------------------------------------------------------------------------------------------
from lark import Transformer, v_args
from dataclasses import dataclass
from typing import List, Optional, Union
# ----------------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass
from typing import *

# ----------------------------------------------------------------------------------------------------------------------------
# Dataclasses for the AST

@dataclass
class Program:
    function_defs: List['FunctionDef']
    main_function: 'FunctionDef'

@dataclass
class FunctionDef:
    function_type: str
    function_name: str
    parameters: List['Parameter']
    function_block: 'FunctionBlock'

@dataclass
class FunctionBlock:
    statements: List['Statement']
    return_value: Union['Expression', 'FunctionCall']

@dataclass
class Parameter:
    data_type: Optional[str]
    parameter_name: str
    array_size: Optional[int]

@dataclass
class VariableDeclaration:
    data_type: str
    variable_name: str
    initial_value: Optional[Union['Expression', 'ListAppendTail', 'CompoundVar']]

@dataclass
class Assignment:
    variable_name: str
    assignment_operators: str
    value: Union['Expression', 'SpecialFunction', 'LetInStatement']

@dataclass
class CompoundArray:
    data_type: str
    identifier: str
    size: Optional[int]

@dataclass
class UnaryOperator:
    operator: str

@dataclass
class AssignmentOperator:
    operator: str


@dataclass
class SpecialFunction:
    function_type: str
    arguments: Optional[List['Expression']]

@dataclass
class Expression:
    terms: List['Term']
    operations: Optional[List['BinaryOperator']]

@dataclass
class Term:
    value: Union[str, int, bool]
    identifier: Optional[str]
    expression: Optional['Expression']
    unary_operator: Optional[str]

@dataclass
class BinaryOperator:
    operator: str

@dataclass
class ConditionalStatement:
    condition: Union['SpecialFunction', 'Expression']
    conditional_block: Union['YieldBlock', 'Block']
    other_blocks: List['OtherBlock']
    otherwise_block: Optional['OtherwiseBlock']

@dataclass
class OtherBlock:
    condition: Union['SpecialFunction', 'Expression']
    conditional_block: Union['YieldBlock', 'Block']

@dataclass
class OtherwiseBlock:
    conditional_block: Union['YieldBlock', 'Block']

@dataclass
class LoopStatement:
    loop_type: str
    condition: Optional[Union['Expression', 'ConditionalArgument']]
    block: 'Block'

@dataclass
class ConditionalArgument:
    condition: Union['SpecialFunction', 'Expression']
    comparison_operator: Optional[str]

@dataclass
class TryCatchStatement:
    try_block: 'Block'
    catch_string: str
    catch_block: 'Block'

@dataclass
class YieldBlock:
    statements: List['Statement']
    expression: 'Expression'

@dataclass
class FunctionCall:
    function_name: str
    arguments: List['Expression']

@dataclass
class LetInStatement:
    data_type: str
    variable_name: str
    value: Union['Term', 'Expression', 'LetInBraces']

@dataclass
class LetInBraces:
    let_in: Union['LetInStatement', 'Expression']

@dataclass
class Block:
    statements: List['Statement']

@dataclass
class ListAppendTail:
    elements: List['Expression']
    identifier: Optional[str]

@dataclass
class CompoundVar:
    value: Optional[Union['ListAppendTail', 'Expression']]

@dataclass
class ShowStatement:
    expressions: List['Expression']

@dataclass
class Statement:
    statement_type: str
    value: Optional[Union[
        'Block', 'VariableDeclaration', 'Assignment', 'ShowStatement',
        'ConditionalStatement', 'LoopStatement', 'ValueChangeArray',
        'PopStatement', 'TryCatchStatement', 'FunctionCall', 'FunctionDef'
    ]]

@dataclass
class ValueChangeArray:
    identifier: str
    index: int
    assignment_operators: str
    value: 'Expression'

@dataclass
class PopStatement:
    string_value: str

#================================
from lark import Visitor, Tree, Token
from dataclasses import dataclass
from typing import List, Optional, Union

# AST node classes (imported from the previous code)

class ASTBuilder(Visitor):
    def __default__(self, tree):
        children = [self.transform(child) for child in tree.children]
        return self.create_node(tree.data, children)

    def create_node(self, node_type, children):
        if node_type == "program":
            function_defs = [child for child in children[:-1] if isinstance(child, FunctionDef)]
            main_function = children[-1] if isinstance(children[-1], FunctionDef) else None
            return Program(function_defs, main_function)
        elif node_type == "func_def":
            function_type = str(children[0])
            function_name = str(children[1])
            parameters = children[3]
            function_block = children[5]
            return FunctionDef(function_type, function_name, parameters, function_block)
        elif node_type == "function_block":
            statements = children[1]
            return_value = children[3]
            return FunctionBlock(statements, return_value)
        elif node_type == "parameter_list":
            parameters = children[0] if children else []
            return parameters
        elif node_type == "parameters":
            if not children:
                return []
            parameters = [children[0]]
            parameters.extend(children[2])
            return parameters
        elif node_type == "parameter":
            if len(children) == 1:
                parameter_name = str(children[0])
                return Parameter(None, parameter_name, None)
            else:
                data_type = str(children[0])
                parameter_name = str(children[1])
                array_size = int(children[2].value) if len(children) > 2 else None
                return Parameter(data_type, parameter_name, array_size)
        elif node_type == "variable_declaration":
            data_type = str(children[0])
            variable_name = str(children[1])
            initial_value = children[2] if len(children) > 2 else None
            return VariableDeclaration(data_type, variable_name, initial_value)
        elif node_type == "compound_array":
            if len(children) == 1:
                return CompoundArray(str(children[0]), None)
            else:
                data_type = str(children[0])
                identifier = str(children[1])
                array_size = int(children[3].value) if len(children) > 3 else None
                return CompoundArray(data_type, identifier, array_size)
        elif node_type == "compound_var":
            if not children:
                return CompoundVar(None)
            else:
                value = children[0]
                return CompoundVar(value)
        elif node_type == "list_append_tail":
            if children[0].data == "expressions":
                elements = children[1]
                identifier = None
            elif children[0].data == "TAIL":
                elements = None
                identifier = str(children[2])
            elif children[0].data == "APPEND":
                elements = [children[2]]
                identifier = str(children[4])
            return ListAppendTail(elements, identifier)
        elif node_type == "assignment_statement":
            variable_name = str(children[0])
            assignment_operators = str(children[1])
            value = children[2]
            return Assignment(variable_name, assignment_operators, value)
        elif node_type == "show_statement":
            expressions = children[2]
            return ShowStatement(expressions)
        elif node_type == "block":
            statements = children[1]
            return Block(statements)
        elif node_type == "value_change_array":
            identifier = str(children[0])
            index = int(children[2].value)
            assignment_operators = str(children[3])
            value = children[4]
            return ValueChangeArray(identifier, index, assignment_operators, value)
        elif node_type == "expressions":
            if not children:
                return []
            expressions = [children[1]]
            expressions.extend(children[2])
            return expressions
        elif node_type == "expression":
            terms = children[0] if children else []
            operations = children[1] if len(children) > 1 else None
            return Expression(terms, operations)
        elif node_type == "terms":
            if not children:
                return []
            operators = [children[0]]
            terms = [children[1]]
            terms.extend(children[2])
            return [operator for operator in operators for _ in terms], terms
        elif node_type == "term":
            if isinstance(children[0], Token):
                value = children[0].value
                if children[0].type == "IDENTIFIER":
                    identifier = value
                    value = None
                elif children[0].type in ["NUM_LITERAL", "YAY", "NAY"]:
                    identifier = None
                else:
                    raise ValueError(f"Unexpected token type: {children[0].type}")
                expression = None
                unary_operator = None
            elif children[0] == "string":
                value = children[0].children[0].value
                identifier = None
                expression = None
                unary_operator = None
            elif children[0] == "expression":
                value = None
                identifier = None
                expression = children[0]
                unary_operator = None
            elif children[0] == "unary_operators":
                value = None
                identifier = str(children[1])
                expression = None
                unary_operator = str(children[0])
            elif children[0] == "IDENTIFIER":
                value = None
                identifier = str(children[0])
                expression = children[2] if len(children) > 2 else None
                unary_operator = str(children[1]) if len(children) > 1 else None
            return Term(value, identifier, expression, unary_operator)
        elif node_type == "binary_operators":
            return BinaryOperator(str(children[0]))
        elif node_type == "unary_operators":
            return UnaryOperator(str(children[0]))
        elif node_type == "assignment_operators":
            return AssignmentOperator(str(children[0]))
        elif node_type == "conditional_block":
            return children[0]
        elif node_type == "conditional_argument":
            if children[0].data == "special_function":
                condition = children[0]
                comparison_operator = str(children[1]) if len(children) > 1 else None
            else:
                condition = children[0]
                comparison_operator = None
            return ConditionalArgument(condition, comparison_operator)
        elif node_type == "conditional_statement":
            condition = children[2]
            conditional_block = children[4]
            other_blocks = children[5]
            otherwise_block = children[6] if len(children) > 6 else None
            return ConditionalStatement(condition, conditional_block, other_blocks, otherwise_block)
        elif node_type == "other_block":
            if not children:
                return []
            condition = children[2]
            conditional_block = children[4]
            other_blocks = children[5] if len(children) > 5 else []
            return [OtherBlock(condition, conditional_block)] + other_blocks
        elif node_type == "otherwise_block":
            return OtherwiseBlock(children[0])
        elif node_type == "loop_statement":
            if children[0].data == "ITER":
                loop_type = "iter"
                condition = [children[2], children[4]]
                block = children[6]
            elif children[0].data == "WHILE":
                loop_type = "while"
                condition = children[2]
                block = children[4]
            elif children[0].data == "REPEAT":
                loop_type = "repeat"
                condition = children[4]
                block = children[2]
            return LoopStatement(loop_type, condition, block)
        elif node_type == "pop_statement":
            string_value = children[2].children[0].value
            return PopStatement(string_value)
        elif node_type == "try_catch_statement":
            try_block = children[1]
            catch_string = children[4].children[0].value
            catch_block = children[6]
            return TryCatchStatement(try_block, catch_string, catch_block)
        elif node_type == "yield_block":
            statements = children[1]
            expression = children[3]
            return YieldBlock(statements, expression)
        elif node_type == "function_call":
            function_name = str(children[0])
            arguments = children[2]
            return FunctionCall(function_name, arguments)
        elif node_type == "argument_list":
            if not children:
                return []
            arguments = [children[0]]
            arguments.extend(children[1])
            return arguments
        elif node_type == "let_in_braces":
            let_in = children[0]
            return LetInBraces(let_in)
        elif node_type == "let_in":
            if isinstance(children[0], LetInStatement):
                return children[0]
            else:
                return children[0]
        elif node_type == "let_in_statement":
            data_type = str(children[1])
            variable_name = str(children[2])
            if children[4].data == "OPEN_BRACES":
                value = children[5]
            else:
                value = children[4]
            if len(children) > 6:
                value = LetInBraces(value)
            return LetInStatement(data_type, variable_name, value)
        elif node_type == "statement":
            statement_type = children[0].data
            value = children[0]
            return Statement(statement_type, value)
        elif node_type == "special_function":
            function_type = children[0].data
            if function_type == "IDENTIFIER":
                if len(children) == 3:
                    arguments = [children[2]]
                else:
                    start = int(children[2].value)
                    end = int(children[4].value)
                    arguments = [start, end]
            else:
                arguments = [str(children[2])] if len(children) > 2 else []
            return SpecialFunction(function_type, arguments)
        elif node_type == "data_type":
            return str(children[0]) if children else None
        elif node_type == "num_str_flag":
            return str(children[0])
        elif node_type == "basic_data_type":
            fix_let = str(children[0]) if children else None
            data_type = str(children[1])
            return f"{fix_let} {data_type}" if fix_let else data_type
        elif node_type == "fix_let":
            return str(children[0]) if children else None
        elif node_type == "compound_data_type":
            return str(children[0])
        elif node_type == "string":
            return children[1].value
        elif node_type == "skip_stop":
            return str(children[0])

    def transform(self, tree):
        if isinstance(tree, Tree):
            return self.__default__(tree)
        elif isinstance(tree, Token):
            return tree.value
        else:
            raise ValueError(f"Unexpected input: {tree}")




  


# ----------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------

def read_geko_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
# --------------------------------------------------------------------------------------------
    
# we have to perform dfs on the tree to get the leaf nodes and then we can append the value
def dfs(tree_node, leaf_nodes):
    if isinstance(tree_node, Token):
        leaf_nodes.append(tree_node)
    else:
        for child in tree_node.children:
            dfs(child, leaf_nodes)

# --------------------------------------------------------------------------------------------

# USE THIS FUNCTION, THIS WORKS:
def final_iteration(tree_node, tokens,graph, parent_node=None):
    if isinstance(tree_node, lark.Tree):
        for child in tree_node.children:
            final_iteration(child, tokens,graph, parent_node=tree_node)
            # ye to ho gaya childs ka
    else:
        # Handle leaf nodes (tokens)
        if isinstance(tree_node, lark.Token):
            new_token = tokens.pop(0)
            new_node = (new_token[0], new_token[1])
            tree_node.value = new_node[1]

        else:
            print("Unknown leaf node type:", tree_node)
    # return graph
# --------------------------------------------------------------------------------------------
            
# Grammar for the parser
grammar = """
start                   :   program
program	                :	DEFINE NUM MAIN OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_BRACES statements YIELD NUM_LITERAL END_OF_LINE CLOSE_BRACES
                        |   func_def program
func_def                :   DEFINE function_type IDENTIFIER OPEN_PARENTHESIS parameter_list CLOSE_PARENTHESIS function_block

function_block	        :	OPEN_BRACES statements YIELD return_value END_OF_LINE CLOSE_BRACES
function_type	        :	NUM | STR | FLAG | VOID
parameter_list	        :	parameter parameters | epsilon
return_value	        :	expression | function_call
parameters	            :	ELEMENT_SEPERATOR parameter parameters 
                        |   epsilon
parameter	            :	compound_data_type IDENTIFIER | basic_data_type IDENTIFIER choose_array
choose_array            :   OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET | epsilon                        

statements	            :	statement statements
                        |   epsilon
equal_to                :   EQUAL_TO post_equal_to | epsilon
post_equal_to           :   ENTER OPEN_PARENTHESIS string CLOSE_PARENTHESIS 
                        |   expression
                        |   special_function
                        |   let_in_statement 
                        
special_function        :   IDENTIFIER OPEN_BRACKET NUM_LITERAL SLICING_COLON NUM_LITERAL CLOSE_BRACKET
                        |   LENGTH OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS
                        
                        |   HEAD OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS
                        |   ISEMPTY OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS
                        |   function_call

data_type	            :  	basic_data_type 
                        |   compound_data_type 
                        |   epsilon
num_str_flag	        :	NUM | STR | FLAG
basic_data_type	        :	fix_let num_str_flag
fix_let	                :	FIX | LET | epsilon
compound_data_type	    :	LIST | TUP


string	                :	TILDE STRING_LITERAL TILDE
array	                :	basic_data_type IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET

variable_declaration	:	basic_data_type IDENTIFIER equal_to
                        |   compound_array compound_var

compound_array          :   compound_data_type IDENTIFIER
                        |   array 

compound_var            :   EQUAL_TO list_append_tail
                        |   EQUAL_TO compound_element BINARY_OPERATOR compound_element
                        |   epsilon

compound_element        :   IDENTIFIER
                        |   OPEN_BRACKET expression expressions CLOSE_BRACKET

list_append_tail        :   OPEN_BRACKET expression expressions CLOSE_BRACKET
                        |   TAIL OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS
                        |   APPEND OPEN_PARENTHESIS expression ELEMENT_SEPERATOR IDENTIFIER CLOSE_PARENTHESIS

assignment_statement	:	IDENTIFIER assignment_operators post_equal_to
show_statement	        :	SHOW OPEN_PARENTHESIS expression expressions CLOSE_PARENTHESIS
block	                :	OPEN_BRACES statements CLOSE_BRACES
value_change_array	    :	IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET assignment_operators expression

expressions             :   ELEMENT_SEPERATOR expression expressions
                        |   epsilon
expression	            :   term terms | epsilon
terms	                :	binary_operators term terms 
                        |   epsilon
                        
term	                :   IDENTIFIER
                        |   NUM_LITERAL
                        |   string
                        |   YAY
                        |   NAY
                        |   OPEN_PARENTHESIS expression CLOSE_PARENTHESIS
                        |   unary_operators IDENTIFIER
                        |   IDENTIFIER UNARY_OPERATOR
                        |   IDENTIFIER OPEN_BRACKET expression CLOSE_BRACKET
                        |   LENGTH
                        
binary_operators	    :	BINARY_OPERATOR 
                        |   COMPARISON_OPERATOR 
                        |   BINARY_LOGICAL_OPERATOR
unary_operators	        :	UNARY_OPERATOR
                        |   UNARY_LOGICAL_OPERATOR
assignment_operators	:	EQUAL_TO
                        |   ASSIGNMENT_OPERATOR
                        
conditional_block       :   yield_block 
                        |   block
conditional_argument    :   special_function COMPARISON_OPERATOR expression
                        |   expression
conditional_statement	:	GIVEN OPEN_PARENTHESIS conditional_argument CLOSE_PARENTHESIS conditional_block other_block otherwise_block
other_block	            :	OTHER OPEN_PARENTHESIS conditional_argument CLOSE_PARENTHESIS conditional_block other_block
                        |   epsilon 
otherwise_block	        :	OTHERWISE conditional_block
                        |   epsilon
skip_stop               :   SKIP
                        |   STOP

loop_statement	        :	ITER OPEN_PARENTHESIS statement expression END_OF_LINE expression CLOSE_PARENTHESIS block
                        |   WHILE OPEN_PARENTHESIS conditional_argument CLOSE_PARENTHESIS block
                        |   REPEAT block WHILE OPEN_PARENTHESIS conditional_argument CLOSE_PARENTHESIS END_OF_LINE

pop_statement           :   POP OPEN_PARENTHESIS string CLOSE_PARENTHESIS

try_catch_statement	    :	TEST block ARREST OPEN_PARENTHESIS string CLOSE_PARENTHESIS block

yield_block             :   OPEN_BRACES statements YIELD expression END_OF_LINE CLOSE_BRACES

function_call	        :	IDENTIFIER OPEN_PARENTHESIS argument_list CLOSE_PARENTHESIS

argument_list	        :	expression expressions

let_in_braces           :   let_in CLOSE_BRACES
let_in                  :   let_in_statement | expression
let_in_statement	    :   LET data_type IDENTIFIER EQUAL_TO OPEN_BRACES let_in_braces
                        |   LET data_type IDENTIFIER EQUAL_TO term IN OPEN_BRACES let_in_braces
                        |   LET data_type IDENTIFIER EQUAL_TO term IN let_in

statement	            :	block
                        |   variable_declaration END_OF_LINE
                        |   assignment_statement END_OF_LINE
                        |   show_statement END_OF_LINE
                        |   conditional_statement
                        |   loop_statement
                        |   skip_stop END_OF_LINE
                        |   value_change_array END_OF_LINE
                        |   pop_statement END_OF_LINE
                        |   try_catch_statement
                        |   function_call END_OF_LINE
                        |   unary_operators IDENTIFIER END_OF_LINE
                        |   IDENTIFIER UNARY_OPERATOR END_OF_LINE
                        |   func_def

epsilon :
NUM: "NUM"
STR: "STR"
FLAG: "FLAG"
FIX: "FIX"
SHOW: "SHOW"
ITER: "ITER"
LIST: "LIST"
TUP: "TUP"
ENTER: "ENTER"
YIELD: "YIELD"
LET: "LET"
IN: "IN"
VOID: "VOID"
WHILE: "WHILE"
REPEAT: "REPEAT"
GIVEN: "GIVEN"
OTHER: "OTHER"
OTHERWISE: "OTHERWISE"
DEFINE: "DEFINE"
TEST: "TEST"
POP: "POP"
ARREST: "ARREST"
LENGTH: "LENGTH"
HEAD: "HEAD"
TAIL: "TAIL"
ISEMPTY: "ISEMPTY"
APPEND: "APPEND"
SKIP: "SKIP"
STOP: "STOP"
YAY: "YAY"
NAY: "NAY"
MAIN: "MAIN"
IDENTIFIER: "IDENTIFIER"
OPEN_PARENTHESIS: "OPEN_PARENTHESIS"
CLOSE_PARENTHESIS: "CLOSE_PARENTHESIS"
OPEN_BRACES: "OPEN_BRACES"
CLOSE_BRACES: "CLOSE_BRACES"
OPEN_BRACKET: "OPEN_BRACKET"
CLOSE_BRACKET: "CLOSE_BRACKET"
NUM_LITERAL: "NUM_LITERAL"
STRING_LITERAL: "STRING_LITERAL"
END_OF_LINE: "END_OF_LINE"
SLICING_COLON: "SLICING_COLON"
ELEMENT_SEPERATOR: "ELEMENT_SEPERATOR"
COMPARISON_OPERATOR: "COMPARISON_OPERATOR"
ASSIGNMENT_OPERATOR: "ASSIGNMENT_OPERATOR"
UNARY_OPERATOR: "UNARY_OPERATOR"
BINARY_OPERATOR: "BINARY_OPERATOR"
BINARY_LOGICAL_OPERATOR: "BINARY_LOGICAL_OPERATOR"
UNARY_LOGICAL_OPERATOR: "UNARY_LOGICAL_OPERATOR"
TILDE: "TILDE"
EQUAL_TO: "EQUAL_TO"

%import common.NUMBER
%import common.WS
%ignore WS"""

#----------------------------------------------------------------------------------------------------------------------------

# Create the Lark parser
parser = Lark(grammar, start='start', parser = 'lalr')#, lexer = lexer_lark)

code = """
define num main() {
    num a = 7;
    yield 0;
}"""
#--------------------------



# ----------------------------------------------------------------------------------------------------------------------------

parser_lark_dir = os.path.dirname(__file__)
tokens = lexer_lark.lexer(code)

# ----------------------------------------------------------------------------------------------------------------------------

tokenised_code = ""

for token in tokens:
    # print(type(token[0]))
    tokenised_code += token[0] + " "

#---------------------------------------

tree = parser.parse(tokenised_code)

# ast_builder = ASTBuilder()
# ast = ast_builder.transform(tree)
# print(ast)


graph_of_tree = lark.tree.pydot__tree_to_graph(tree)

#---------------------------------------

graph = pydot.graph_from_dot_data(lark.tree.pydot__tree_to_graph(tree).to_string())
# function toh chal gaya
print(type(graph[0]))

#----------------------------------------------------------------------------------------------------------------------------

png_name = "abstract_syntax_tree.png"
# graph[0].write_png(png_name)

# graph bhi chal gaya!
#----------------------------------------------------------------------------------------------------------------------------

# leaf_nodes = []
# dfs(tree, leaf_nodes)

# ----------------------------------------------------------------------------------------------------------------------------

# Final function to be used: 
final_iteration(tree, tokens, graph=graph[0])
ast_builder = ASTBuilder()
ast = ast_builder.transform(tree)
# print(ast)

import rich
rich.print(ast)

# ----------------------------------------------------------------------------------------------------------------------------
# ast ke liye code: 
# printing the AST:

def print_ast(node, indent=0):
    print("  " * indent + str(node))
    if isinstance(node, list):
        for child in node:
            print_ast(child, indent + 1)
    elif isinstance(node, tuple) and len(node) > 1:
        for child in node[1:]:
            print_ast(child, indent + 1)
    elif isinstance(node, dict):
        for key, value in node.items():
            print("  " * (indent + 1) + str(key) + ":")
            print_ast(value, indent + 2)

# Assuming 'ast' is the variable holding the AST
# print_ast(ast, indent=2)

