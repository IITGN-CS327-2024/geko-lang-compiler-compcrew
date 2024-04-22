import re
import sys

def read_geko_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if len(sys.argv) != 2:
    print("Usage: python3 lexer.py <geko_file>")
    sys.exit(1)

file_path = sys.argv[1]
geko_code = read_geko_file(file_path)

# LEXER
patterns = [
    ('NUM', r'\bnum\b'),
    ('STR', r'\bstr\b'),
    ('FLAG', r'\bflag\b'),
    ('FIX', r'\bfix\b'),
    ('SHOW', r'\bshow\b'),
    ('ITER', r'\biter\b'),
    ('LIST', r'\blist\b'),
    ('TUP', r'\btup\b'),
    ('ENTER', r'\benter\b'),
    ('YIELD', r'\byield\b'),
    ('LET', r'\blet\b'),
    ('IN', r'\bin\b'),
    ('VOID', r'\bvoid\b'),
    ('WHILE', r'\bwhile\b'),
    ('REPEAT', r'\brepeat\b'),
    ('GIVEN', r'\bgiven\b'),
    ('OTHER', r'\bother\b'),
    ('OTHERWISE', r'\botherwise\b'),
    ('DEFINE', r'\bdefine\b'),
    ('TEST', r'\btest\b'),
    ('POP', r'\bpop\b'),
    ('ARREST', r'\barrest\b'),
    ('LENGTH', r'\blength\b'),
    ('HEAD', r'\bhead\b'),
    ('TAIL', r'\btail\b'),
    ('ISEMPTY', r'\bisEmpty\b'),
    ('APPEND', r'\bappend\b'),
    ('SKIP', r'\bskip\b'),
    ('STOP', r'\bstop\b'),
    ('YAY', r'\byay\b'),
    ('NAY', r'\bnay\b'),
    ('MAIN' , r'\bmain\b'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('OPEN_PARENTHESIS', r'\('),
    ('CLOSE_PARENTHESIS', r'\)'),
    ('OPEN_BRACES', r'\{'),
    ('CLOSE_BRACES', r'\}'),
    ('OPEN_BRACKET', r'\['),
    ('CLOSE_BRACKET', r'\]'),
    ('NUM_LITERAL', r'-?\b\d+\b'),
    ('COMMENT', r'##.*'),
    ('STRING_LITERAL', r'~(?:[^~\\]|\\.)*~'),
    ('TILDE', r'~'),
    ('END_OF_LINE', r';'),
    ('SLICING_COLON', r':'),
    ('ELEMENT_SEPERATOR', r','),
    ('COMPARISON_OPERATOR', r'==|!=|<=|>=|>|<'),
    ('EQUAL_TO', r'='),
    ('ASSIGNMENT_OPERATOR', r'/=|\*=|\+=|-=|%='),
    ('UNARY_OPERATOR' , r'\+\+|--|`'),
    ('BINARY_OPERATOR', r'\*\*|/|\*|\+|-|%'),
    ('BINARY_LOGICAL_OPERATOR', r'&&|\|\||&|\||\^'),
    ('UNARY_LOGICAL_OPERATOR', r'!')
]

pattern = '|'.join('(?P<%s>%s)' % pair for pair in patterns)

stringVal = ''
def lexer(code):
    tokens = []
    for match in re.finditer(pattern, code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'STRING_LITERAL':
            string_val = value[1:-1]
            tokens.append(('TILDE', '~'))
            tokens.append((kind, string_val))
            tokens.append(('TILDE', '~'))
        elif kind == 'COMMENT':
            pass
        else:
            tokens.append((kind, value))
    return tokens

tokens = lexer(geko_code)
def print_table(nested_tuple):
    # Find the maximum length of each column
    max_len_col1 = max(len(item[0]) for item in nested_tuple)
    max_len_col2 = max(len(item[1]) for item in nested_tuple)

    # Print the table header
    print(f"{ 'TokenName':<{max_len_col1}} {'TokenValue':<{max_len_col2}}")
    print('-' * (max_len_col1 + max_len_col2 + 3))

    # Print the table content
    for token_name, token_value in nested_tuple:
        print(f"{token_name:<{max_len_col1}} {token_value:<{max_len_col2}}")
# print_table(tokens)

# PARSER
from lark import Lark
from lark.lexer import Lexer, Token
import re
import sys
import os
#----------------------------------------------------------------------------------------------------------------------------
import lark
import pydot

# --------------------------------------------------------------------------------------------
    
# we have to perform dfs on the tree to get the leaf nodes and then we can append the value
def dfs(tree_node, leaf_nodes):
    if isinstance(tree_node, Token):
        leaf_nodes.append(tree_node)
    else:
        for child in tree_node.children:
            dfs(child, leaf_nodes)

def final_iteration(tree_node, tokens,graph, parent_node=None):
    if isinstance(tree_node, lark.Tree):
        for child in tree_node.children:
            final_iteration(child, tokens,graph, parent_node=tree_node)
            # ye to ho gaya childs ka
    else:
        # Handle leaf nodes (tokens)
        if isinstance(tree_node, lark.Token):
            # print("Token type & value:",tree_node.type,' ', tree_node.value)
            new_token = tokens.pop(0)
            # print(new_token)
            # print(type(new_token))
            new_node = (new_token[0], new_token[1])
            tree_node.value = new_node[1]
            # print(type(new_node))
            # new_node = pydot.Node(type=new_token[0], label=new_token[1])
            # print(new_node)
            # print(type(new_node))
            # if parent_node:
            # edge = pydot.Edge(parent_node, new_node)
                # print(type(parent_node))
            # graph.add_edge(edge)
                
            # parent.children[index+1] = new_node
            
            # print("New token type and value:", tree_node.type, ' ', tree_node.value)

        else:
            print("Unknown leaf node type:", tree_node)
    # return graph
# --------------------------------------------------------------------------------------------
            
# Grammar for the parser
grammar = """
start                   :   program
program	                :	main_func
                        |   func_def program
main_func               :   DEFINE NUM MAIN OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_BRACES statements YIELD NUM_LITERAL END_OF_LINE CLOSE_BRACES
func_def                :   DEFINE function_type IDENTIFIER OPEN_PARENTHESIS parameter_list CLOSE_PARENTHESIS function_block

function_block	        :	OPEN_BRACES statements YIELD return_value END_OF_LINE CLOSE_BRACES
function_type	        :	NUM | STR | FLAG | VOID
parameter_list	        :	parameter parameters | epsilon
return_value	        :	expression
parameters	            :	ELEMENT_SEPERATOR parameter parameters 
                        |   epsilon
parameter	            :	compound_data_type IDENTIFIER | basic_data_type IDENTIFIER choose_array
choose_array            :   OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET | epsilon                        

statements	            :	statement statements
                        |   epsilon
equal_to                :   EQUAL_TO post_equal_to | epsilon
post_equal_to           :   ENTER OPEN_PARENTHESIS string CLOSE_PARENTHESIS 
                        |   expression
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
                        |   EQUAL_TO IDENTIFIER
                        |   epsilon

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
                        |   special_function
                        
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

loop_statement	        :	ITER OPEN_PARENTHESIS statement expression END_OF_LINE update_statement CLOSE_PARENTHESIS block
                        |   WHILE OPEN_PARENTHESIS conditional_argument CLOSE_PARENTHESIS block
                        |   REPEAT block WHILE OPEN_PARENTHESIS conditional_argument CLOSE_PARENTHESIS END_OF_LINE

update_statement        :   IDENTIFIER assignment_operators expression
                        |   IDENTIFIER UNARY_OPERATOR
                        |   unary_operators IDENTIFIER
                        
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
parser_lark_dir = os.path.dirname(__file__)

tokenised_code = ""

for token in tokens:
    # print(type(token[0]))
    tokenised_code += token[0] + " "

tree = parser.parse(tokenised_code)
graph_of_tree = lark.tree.pydot__tree_to_graph(tree)
graph = pydot.graph_from_dot_data(lark.tree.pydot__tree_to_graph(tree).to_string())
print(type(graph[0]))

png_name = "parse_tree.png"
graph[0].write_png(png_name)

leaf_nodes = []

dfs(tree, leaf_nodes)

# Final function to be used: 
final_iteration(tree, tokens, graph=graph[0])

# CLASSES

from lark import Visitor, Tree, Token
from dataclasses import dataclass
from typing import List, Optional, Union
from typing import *

@dataclass
class Program:
    function_defs: List['FunctionDef']
    main_function: 'MainFunc'

@dataclass
class MainFunc:
    statements: List[Union['Block', 'VariableDeclaration', 'AssignmentStatement', 'ShowStatement', 'ConditionalStatement', 'LoopStatement', 'ValueChangeArray', 'PopStatement', 'TryCatchStatement', 'FunctionCall', 'UnaryStatement', 'FunctionDef']]

@dataclass
class Block:
    statements: List[Union['Block', 'VariableDeclaration', 'AssignmentStatement', 'ShowStatement', 'ConditionalStatement', 'LoopStatement', 'ValueChangeArray', 'PopStatement', 'TryCatchStatement', 'FunctionCall', 'UnaryStatement', 'FunctionDef']]

@dataclass
class AssignmentStatement:
    variable_name: str
    assignment_operators: str
    value: Union['Expression', 'SpecialFunction', 'LetInStatement']

@dataclass
class EnterStatement:
    string: str
    enter_value: str

@dataclass
class UnaryStatement:
    pre_unary_operator: str
    # value: Union['Expression', 'SpecialFunction', 'LetInStatement']
    value: str
    post_unary_operator: str

@dataclass
class FunctionDef:
    function_type: str
    function_name: str
    parameters: List['Parameter']
    function_block: 'FunctionBlock'

@dataclass
class FunctionBlock:
    statements: List[Union['Block', 'VariableDeclaration', 'AssignmentStatement', 'ShowStatement', 'ConditionalStatement', 'LoopStatement', 'ValueChangeArray', 'PopStatement', 'TryCatchStatement', 'FunctionCall', 'UnaryStatement', 'FunctionDef']]
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
    size_array: Optional[int]
    equal_to: Optional[Union['Expression', 'ListAppendTail',str]]

@dataclass
class Assignment:
    variable_name: str
    assignment_operators: str
    value: Union['Expression', 'SpecialFunction', 'LetInStatement']

@dataclass
class Array:
    data_type: str
    identifier: str
    size: Optional[int]

@dataclass
class LIST:
    data_type: str
    identifier: str
    size: Optional[int]

@dataclass
class TUP:
    data_type: str
    identifier: str

@dataclass
class Skip:
    skip: str

@dataclass
class UnaryOperator:
    operator: str

@dataclass
class AssignmentOperator:
    operator: str

@dataclass
class SpecialFunction:
    identifier: str
    num_literal_start: Optional[int]
    num_literal_end: Optional[int]
    length: Optional[str]
    head: Optional[str]
    isempty: Optional[str]
    function_call: Optional['FunctionCall']
    # is upar wale ko change karna hai

@dataclass
class Expression:
    operator_if_exists: Optional[str]
    terms: List['Term']
    # terms: List[Union['Term', 'BinaryOperator', 'UnaryOperator', 'SpecialFunction', 'LetInStatement', 'FunctionCall']]

@dataclass
class Term:
    value: Union[str, int, bool]
    identifier: Optional[str]
    expression: Optional['Expression']
    pre_unary_operator: Optional[str]
    post_unary_operator: Optional[str]

@dataclass
class BinaryOperator:
    operator: str

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
    declaration: Optional[Union['VariableDeclaration', 'AssignmentStatement']]
    condition: Optional[Union['Expression', 'ConditionalArgument']]
    updation: Optional[Union['AssignmentStatement', 'UnaryStatement']]
    block: 'Block'

@dataclass
class ConditionalArgument:
    is_special: Optional['SpecialFunction']
    comparison_operator: Optional[str]
    expression: 'Expression'

@dataclass
class TryCatchStatement:
    try_block: 'Block'
    catch_string: str
    catch_block: 'Block'

@dataclass
class YieldBlock:
    statements: List[Union['Block', 'VariableDeclaration', 'AssignmentStatement', 'ShowStatement', 'ConditionalStatement', 'LoopStatement', 'ValueChangeArray', 'PopStatement', 'TryCatchStatement', 'FunctionCall', 'UnaryStatement', 'FunctionDef']]
    expression: 'Expression'

@dataclass
class FunctionCall:
    function_name: str
    arguments: List['Expression']

@dataclass
class LetInStatement:
    # let: str
    data_type: str
    variable_name: str
    # in_in = str
    value_or_letin: Optional[Union['Term', 'Expression', 'LetInStatement']]
    operation: Optional['Expression']

@dataclass
class ListAppendTail:
    elements: List['Expression']
    identifier: Optional[str]
    tail: Optional[str]
    append: Optional[str]

@dataclass
class ShowStatement:
    expressions: List['Expression']

@dataclass
class ValueChangeArray:
    identifier: str
    index: int
    assignment_operators: str
    value: 'Expression'

@dataclass
class PopStatement:
    string_value: str

@dataclass
class EqualTo:
    value: List[Union['Expression', 'SpecialFunction', 'LetInStatement', 'FunctionCall']]

@dataclass
class ConditionalStatement:
    conditional_argument: 'ConditionalArgument'
    conditional_block: Union['YieldBlock', 'Block']
    other_blocks: Optional[List['OtherBlock']]
    otherwise_block: Optional['OtherwiseBlock']

def flatten_list(list_of_lists):
    flat_list = []
    for sublist in list_of_lists:
        if isinstance(sublist, list):
            flat_list.extend(flatten_list(sublist))
        elif(sublist is not None):
            flat_list.append(sublist)
    return flat_list

def flatten_expression(expression: Union[Expression, Term, Any]) -> List[Union[Term, Any]]:
    flattened = []

    if isinstance(expression, Expression):
        flattened.append(BinaryOperator(operator=expression.operator_if_exists))
        for term in expression.terms:
            flattened.extend(flatten_expression(term))
    elif isinstance(expression, Term):
        flattened.append(expression)
    else:
        flattened.append(expression)

    return flattened

# AST

from lark import Lark
from lark.lexer import Token
import sys
import os
import re
# ----------------------------------------------------------------------------------------------------------------------------
import lark
from lark import Visitor, Tree, Token
import pydot
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
from typing import *
import rich

class ASTBuilder(Visitor):
    def __default__(self, tree):
        children = [self.transform(child) for child in tree.children]
        # print("----------------------------------------------------------")
        # print(f"the tree data from __default__ is: {tree.data}, children are: {children}")
        return self.create_node(tree.data, children)

    def create_node(self, node_type, children):
        # print("----------------------------------------------------------")
        # print(f"node_type from create_node: {node_type}, children: {children}")
        # print("----------------------------------------------------------")
        if node_type == "start":
            # print(f"node_type: {node_type}, value: {children[0]}")
            return children[0]
        
        elif node_type == "program":
            if(len(children) == 1):
                main_function = children[0]
                function_defs = []
                # print(f"node_type:{node_type}, main_function: {main_function}")
                # print("**************************************************************************")
                return (Program(function_defs, main_function))
            else:
                function_defs = [children[0]]
                program = children[1]
                function_defs.extend(program.function_defs)
                main_function = program.main_function
                # print(f"node_type:{node_type}, function_defs: {function_defs}, main_function: {main_function}")
                return Program(function_defs, main_function)
        
        elif node_type == "main_func":
            statements = children[6]
            return MainFunc(statements)
        
        elif node_type == "func_def":
            # print("ye func_def bhi galat hai isko bhi change crow")
            function_type = str(children[1])
            function_name = str(children[2])
            parameters = [children[4][0]]
            parameters.extend(children[4][1]) if len(children[4]) > 1 else None
            function_block = children[6]
            # print(f"node_type:{node_type}, function_type: {function_type}, function_name: {function_name}, parameters: {parameters}, function_block: {function_block}")
            return FunctionDef(function_type, function_name, parameters, function_block)
        
        elif node_type == "function_block":
            statements = children[1]
            return_value = children[3]
            # print(f"node_type:{node_type}, statements: {statements}, return_value: {return_value}")
            return FunctionBlock(statements, return_value)
        
        elif node_type == "function_type":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        
        elif node_type == "parameter_list":
            parameters = children if children else []
            # print(f"node_type:{node_type}, parameters: {parameters}")
            return parameters
        
        elif node_type == "return_value":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return children[0]
        
        elif node_type == "parameters":
            if not children:
                return []
            elif len(children) == 1:
                # print(f"node_type:{node_type}, value: None")
                return []
            parameters = [children[1]]
            parameters.extend(children[2])
            # print(f"node_type:{node_type}, parameters: {parameters}")
            return parameters
        
        elif node_type == "parameter":
            if len(children) == 2:
                data_type = str(children[0])
                parameter_name = str(children[1])
                # print(f"node_type:{node_type}, parameter_name: {parameter_name}")
                return Parameter(None, parameter_name, None)
            else:
                data_type = str(children[0])
                parameter_name = str(children[1])
                array_size = children[2] if len(children) > 2 else None
                # print(f"node_type:{node_type}, data_type: {data_type}, parameter_name: {parameter_name}, array_size: {array_size}")
                return Parameter(data_type, parameter_name, array_size)

        elif node_type == "choose_array":
            if not children:
                # print(f"node_type:{node_type}, value: None")
                return None
            elif len(children) == 1:
                # print(f"node_type:{node_type}, value: None")
                return None
            else:
                # print(f"node_type:{node_type}, value: {children[1]}")
                return children[1]
        
        elif node_type == "statements":
            statements = [children[0]]
            if children[0] == None:
                # print(f"node_type:{node_type}, value: {children[0]}")
                return statements
            if children[1]!=None:
                statements.extend(children[1])
            # print(f"node_type:{node_type}, statements: {statements}")
            return statements
        
        elif node_type == "equal_to":
            if not children:
                # print(f"node_type:{node_type}, value: []")
                return []
            elif len(children) == 1:
                # print(f"node_type:{node_type}, value: {children[0]}")
                return children[0]
            # print(f"node_type:{node_type}, value: {children}")
            return children[1]

        elif node_type == "post_equal_to":
            if children[0] == "enter":
                string = str(children[2])[len("THIS_IS_A_STRING_SO_THAT_IT_DOES_NOT_CONFLICT_WITH_OTHER_TYPES"):]
                value = EnterStatement(string,None)
            else:
                value = children[0]
            # print(f"node_type:{node_type}, value: {value}")
            return value

        elif node_type == "special_function":
            if len(children) == 1:
                function_call = children[0]
                # print(f"node_type:{node_type}, function_call: {function_call}")
                return SpecialFunction(None, None, None, None, None, None, function_call)
            else:
                if children[0] == "length":
                    identifier = str(children[2])
                    # print(f"node_type:{node_type}, identifier: {identifier}")
                    return SpecialFunction(identifier, None, None, "length", None, None, None)
                elif children[0] == "head":
                    identifier = str(children[2])
                    # print(f"node_type:{node_type}, identifier: {identifier}")
                    return SpecialFunction(identifier, None, None, None, "head", None, None)
                elif children[0] == "isEmpty":
                    identifier = str(children[2])
                    isEmpty = "isEmpty"
                    # print(f"node_type:{node_type}, identifier: {identifier}")
                    return SpecialFunction(identifier, None, None, None, None,isEmpty, None)

                identifier = str(children[0])
                num_literal_start = int(children[2])
                num_literal_end = int(children[4])
                # print(f"node_type:{node_type}, identifier: {identifier}, num_literal_start: {num_literal_start}, num_literal_end: {num_literal_end}")
                return SpecialFunction(identifier, num_literal_start, num_literal_end, None, None, None, None)
        
        elif node_type == "data_type":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0]) if children else None
        
        elif node_type == "num_str_flag":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        
        elif node_type == "basic_data_type":
            fix_let = str(children[0])
            data_type = str(children[-1])
            # print(f"node_type:{node_type}, fix_let: {fix_let}, data_type: {data_type}")
            return f"{fix_let} {data_type}" if fix_let else data_type
        
        elif node_type == "fix_let":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0]) if children else None
        
        elif node_type == "compound_data_type":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        
        elif node_type == "string":
            # print(f"node_type:{node_type}, value: {children[1]}")
            string_value = "THIS_IS_A_STRING_SO_THAT_IT_DOES_NOT_CONFLICT_WITH_OTHER_TYPES" + str(children[1])
            return string_value

        elif node_type == "array":
            data_type = str(children[0])
            identifier = str(children[1])
            size = int(children[3])
            # print(f"node_type:{node_type}, data_type: {data_type}, identifier: {identifier}, size: {size}")
            return Array(data_type, identifier, size)
        
        elif node_type == "variable_declaration":
            if children[0].__class__.__name__ == "Array":
                data_type = children[0].data_type
                variable_name = children[0].identifier
                size_array = children[0].size
                if children[1]: 
                    equal_to = children[1][1]
                else:
                    equal_to = None
            elif children[0].__class__.__name__ == "LIST":
                size_array = None 
                data_type = children[0].data_type
                variable_name = children[0].identifier
                equal_to = children[1][1]
            elif children[0].__class__.__name__ == "TUP":
                data_type = children[0].data_type
                size_array = None
                variable_name = children[0].identifier
                equal_to = children[1][1] if len(children[1]) > 1 else children
            else:
                data_type = children[0]
                variable_name = str(children[1])
                equal_to = children
                size_array = None
                if len(children) > 2:
                    equal_to = children[2]           
                if equal_to:
                    equal_to = flatten_expression(equal_to)
            return VariableDeclaration(data_type, variable_name, size_array, equal_to)

        elif node_type == "compound_array":
            if len(children) == 1:
                return children[0]
            else:
                data_type = str(children[0])
                identifier = str(children[1])
                if data_type == "list":
                    # print(f"node_type:{node_type}, data_type: {data_type}, identifier: {identifier}")
                    return LIST(data_type, identifier, None)
                else:
                    # print(f"node_type:{node_type}, data_type: {data_type}, identifier: {identifier}")
                    return TUP(data_type, identifier)
        
        elif node_type == "compound_var":
            if len(children) == 1:
                return None
            elif len(children) == 2:
                if children[1].__class__.__name__ == "ListAppendTail":
                    return children
                else:
                    return children[0]
            elif len(children) == 4:
                if children[0] == "EQUAL_TO":
                    return BinaryOperator(children[2], children[1], children[3])
                else:
                    return children
            else:
                return children
        
        elif node_type == "list_append_tail":
            elements = None
            identifier = children
            tail = None
            append = None
            if children[1].__class__.__name__ == "Expression":
                elements =[ children[1] ]
                elements.extend(children[2]) if len(children) > 2 else None
                identifier = None
            elif children[0] == "tail":
                elements = None
                identifier = children[2]
                tail = str(children[0])
            elif children[0] == "append":
                elements = children[2].terms[0]
                identifier = children[4]
                append = str(children[0])
            # print(f"node_type:{node_type}, elements: {elements}, identifier: {identifier}")
            return ListAppendTail(elements, identifier, tail, append)
        
        elif node_type == "assignment_statement":
            variable_name = str(children[0])
            assignment_operators = children[1].operator
            value = children[2]
            # print(f"node_type:{node_type}, variable_name: {variable_name}, assignment_operators: {assignment_operators}, value: {value}")
            return Assignment(variable_name, assignment_operators, value)
        
        elif node_type == "show_statement":
            expressions = children[2]
            if children[3] != "CLOSE_PARENTHESIS":
                i = 3
                expressions = [expressions] 
                while isinstance(children[i],list):
                    expressions.extend(children[i])
                    i+=1
            # print(f"node_type:{node_type}, expressions: {expressions}")
            return ShowStatement(expressions)
        
        elif node_type == "block":
            statements = children[1]
            # print(f"node_type:{node_type}, statements: {statements}")
            return Block(statements)
        
        elif node_type == "value_change_array":
            identifier = str(children[0])
            index = int(children[2])
            assignment_operators = children[4]
            value = children[5]
            # print(f"node_type:{node_type}, identifier: {identifier}, index: {index}, assignment_operators: {assignment_operators}, value: {value}")
            return ValueChangeArray(identifier, index, assignment_operators, value)
        
        elif node_type == "expressions":
            if not children:
                # print(f"node_type:{node_type}, value: []")
                return []
            expressions = [children[1]] if len(children) > 1 else []
            expressions.extend(children[2]) if len(children) > 2 else None
            # print(f"node_type:{node_type}, expressions: {expressions}")
            return expressions
        
        elif node_type == "expression":
            if len(children) == 1:
                terms = children[0]
                operator_if_exists = None
            elif len(children) == 2:
                terms = [children[0], children[1] if children[1] is not None else None] if children else None
                # operator_if_exists = children if '=' in children else None
                operator_if_exists = None
            # elif len(children) == 3:
            #     terms = None
            #     # operator_if_exists = children if '=' in children else None
            #     operator_if_exists = None
            # else:
            #     terms = None
            #     # operator_if_exists = children if '=' in children else None
            #     operator_if_exists = None
            # print(f"node_type:{node_type}, terms: {terms}")
            return Expression(operator_if_exists, terms)
        
        elif node_type == "terms":
            if not children:
                # print(f"node_type:{node_type}, value: []")
                return []
            operator_if_exists = [children[0]]
            operator_if_exists = children[0]
            terms = children[1:] if len(children) > 1 else None
            # print(f"node_type:{node_type}, operators: {operator_if_exists}, terms: {terms}")
            if terms is None:
                return None
            return Expression(operator_if_exists=operator_if_exists, terms=terms)
        
        elif node_type == "term":
            identifier = None
            if len(children)==1:  
                if children[0].__class__.__name__ == "SpecialFunction":
                    expression = children[0]
                    value = None
                elif str(children[0]).startswith("THIS_IS_A_STRING_SO_THAT_IT_DOES_NOT_CONFLICT_WITH_OTHER_TYPES"):
                    value = str(children[0])[len("THIS_IS_A_STRING_SO_THAT_IT_DOES_NOT_CONFLICT_WITH_OTHER_TYPES"):]
                    identifier = None
                    expression = None
                elif type(children[0]) == int:
                    value = children[0]
                    identifier = None
                    expression = None
                elif type(children[0]) == bool:
                    value = children[0]
                    identifier = None
                    expression = None
                else:
                    value = None
                    identifier = children[0]
                    expression = None
                if children[0].__class__.__name__ == "Token":
                    identifier = children[0].__class__.__name__
                pre_unary_operator = None
                post_unary_operator = None
                
            elif len(children) == 2:
                if children[0].__class__.__name__ == "UnaryOperator":
                    pre_unary_operator = children[0].operator
                    identifier = str(children[1])
                    post_unary_operator = None
                else:
                    post_unary_operator = children[1]
                    identifier = str(children[0])
                    pre_unary_operator = None
                value = None
                expression = None
            elif len(children) == 3:
                pre_unary_operator = None
                post_unary_operator = None
                identifier = None
                expression = children[1]
                value = None
            else:
                pre_unary_operator = None
                post_unary_operator = None
                identifier = str(children[0])
                expression = children[2]
                value = None

            return Term(value, identifier, expression, pre_unary_operator, post_unary_operator)    

        
        elif node_type == "binary_operators":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        
        elif node_type == "unary_operators":
            operator = str(children[0])
            # print(f"node_type:{node_type}, value: {children[0]}")
            return UnaryOperator(operator)
        
        elif node_type == "assignment_operators":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return AssignmentOperator(str(children[0]))
        
        elif node_type == "conditional_block":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return children[0]
        
        elif node_type == "conditional_argument":
            if children[0].__class__.__name__ == "SpecialFunction":
                is_special = children[0]; 
                comparison_operator = str(children[1]) if len(children) > 1 else None
                expression = children[2] if len(children) > 1 else None
            else:
                expression = children[0]
                comparison_operator = None
                is_special = None
            # print(f"node_type:{node_type}, is_special: {is_special}, comparison_operator: {comparison_operator}, expression: {expression}")
            return ConditionalArgument(is_special, comparison_operator, expression)
        
        elif node_type == "conditional_statement":
            conditional_argument = children[2]
            conditional_block = children[4]
            other_blocks = children[5] if len(children) > 5 else []
            otherwise_block = children[6] if len(children) > 6 else None
            # print(f"node_type:{node_type}, conditional_argument: {conditional_argument}, conditional_block: {conditional_block}, other_blocks: {other_blocks}, otherwise_block: {otherwise_block}")
            return ConditionalStatement(conditional_argument, conditional_block, other_blocks, otherwise_block)    

        elif node_type == "other_block":
            if children == [None]:
                # print(f"node_type:{node_type}, value: []")
                return []
            condition = children[2]
            conditional_block = children[4]
            other_blocks = children[5] if len(children) > 5 else []
            # print(f"node_type:{node_type}, condition: {condition}, conditional_block: {conditional_block}, other_blocks: {other_blocks}")
            return [OtherBlock(condition, conditional_block)] + other_blocks
        
        elif node_type == "otherwise_block":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return OtherwiseBlock(children[1:])
        
        elif node_type == "update_statement":
            if len(children) > 2:
                return Assignment(children[0], children[1], children[2])
            
            elif children[1] == "++" or children[1] == "--":
                value = str(children[0])
                post_unary_operator = str(children[1])
                pre_unary_operator = None
                # print(f"node_type:{node_type}, pre_unary_operator: {pre_unary_operator}, value: {value}, post_unary_operator: {post_unary_operator}")
                return UnaryStatement(pre_unary_operator, value, post_unary_operator)
            else: 
                value = str(children[1])
                pre_unary_operator = str(children[0])
                post_unary_operator = None
                # print(f"node_type:{node_type}, pre_unary_operator: {pre_unary_operator}, value: {value}, post_unary_operator: {post_unary_operator}")
                return UnaryStatement(pre_unary_operator, value, post_unary_operator)


        

        elif node_type == "loop_statement":
            loop_type = children[0]
            declaration = None
            condition = children[2]
            updation = None
            block = children[4]
            if children[0] == "iter":
                loop_type = "iter"
                declaration = children[2]
                condition = children[3]
                updation = children[5]
                block = children[7]
            elif children[0] == "while":
                loop_type = "while"
                condition = children[2]
                block = children[4]
            elif children[0] == "repeat":
                loop_type = "repeat_while"
                condition = children[-3]
                block = children[1]
            # print(f"node_type:{node_type}, loop_type: {loop_type}, condition: {condition}, block: {block}")
            return LoopStatement(loop_type, declaration,condition, updation, block)
        
        elif node_type == "pop_statement":
            string_value = str(children[2])[len("THIS_IS_A_STRING_SO_THAT_IT_DOES_NOT_CONFLICT_WITH_OTHER_TYPES"):]
            # print(f"node_type:{node_type}, string_value: {string_value}")
            return PopStatement(string_value)
        
        elif node_type == "try_catch_statement":
            try_block = children[1]
            catch_string = str(children[4])[len("THIS_IS_A_STRING_SO_THAT_IT_DOES_NOT_CONFLICT_WITH_OTHER_TYPES"):]
            catch_block = children[6]
            # print(f"node_type:{node_type}, try_block: {try_block}, catch_string: {catch_string}, catch_block: {catch_block}")
            return TryCatchStatement(try_block, catch_string, catch_block)
        
        elif node_type == "yield_block":
            statements = children[1]
            expression = children[3]
            # print(f"node_type:{node_type}, statements: {statements}, expression: {expression}")
            return YieldBlock(statements, expression)
        
        elif node_type == "function_call":
            function_name = str(children[0])
            arguments = children[2]
            # print(f"node_type:{node_type}, function_name: {function_name}, arguments: {arguments}")
            return FunctionCall(function_name, arguments)
        
        elif node_type == "argument_list":
            if not children:
                # print(f"node_type:{node_type}, value: []")
                return []
            arguments = [children[0]]
            arguments.extend(children[1])
            # print(f"node_type:{node_type}, arguments: {arguments}")
            return arguments
        
        elif node_type == "let_in_braces":
            let_in = children[0]
            # print(f"node_type:{node_type}, let_in: {let_in}")
            return children
        
        elif node_type == "let_in":
            if isinstance(children[0], LetInStatement):
                # print(f"node_type:{node_type}, value: {children[0]}")
                return children[0]
            else:
                # print(f"node_type:{node_type}, value: {children[0]}")
                return children
        elif node_type == "let_in_statement":
            data_type = children[1]
            variable_name = children[2]
            operation = None
            if children[4] == "OPEN_BRACES":
                value = children[5]
            else:
                value = children[4]
            if len(children) > 6:
                value = children[4]
                if children[6] == "{":
                    operation = children[7]
                else:
                    operation = children[6]
            # print(f"node_type:{node_type}, data_type: {data_type}, variable_name: {variable_name}, value: {value}, operation: {operation}")
            return LetInStatement(data_type=data_type, variable_name=variable_name, value_or_letin=value, operation=operation)

        elif node_type == "statement":
            if len(children) == 3:
                if children[0] == "++" or children[0] == "--" or children[0]=="`" or children[0]=="!":
                    pre_unary_operator = children[0]
                    value = children[1]
                    post_unary_operator = None
                    # print(f"node_type:{node_type}, pre_unary_operator: {pre_unary_operator}, value: {value}, post_unary_operator: {post_unary_operator}")
                    return UnaryStatement(pre_unary_operator, value, post_unary_operator)
                else:
                    pre_unary_operator = None
                    value = children[0]
                    post_unary_operator = children[1]
                    # print(f"node_type:{node_type}, pre_unary_operator: {pre_unary_operator}, value: {value},post_unary_operator: {post_unary_operator}")
                    return UnaryStatement(pre_unary_operator, value, post_unary_operator)
            
            statement_type = children[0].__class__.__name__
            if statement_type == "ConditionalStatement":
                return children[0]
            value = children[0]
            if statement_type == "Block":
                return children[0]
            if children[-1] == ";":
                children.pop()
                children = children[0] 
            # print(f"node_type:{node_type}, statement_type: {statement_type}, value: {value}")
            return children
        
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
            # print(f"node_type:{node_type}, function_type: {function_type}, arguments: {arguments}")
            return SpecialFunction(function_type, arguments)
        
        elif node_type == "data_type":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0]) if children else None
        
        elif node_type == "num_str_flag":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        
        elif node_type == "basic_data_type":
            fix_let = str(children[0]) if children else None
            data_type = str(children[1])
            # print(f"node_type:{node_type}, fix_let: {fix_let}, data_type: {data_type}")
            return f"{fix_let} {data_type}" if fix_let else data_type
        
        elif node_type == "fix_let":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0]) if children else None
        
        elif node_type == "compound_data_type":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        
        elif node_type == "skip_stop":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return Skip(skip=children[0])

        
        elif node_type == "compound_element":
            # print(f"node_type:{node_type}, value: {children[0]}")
            terms = children if len(children) > 1 else None
            terms.extend(children[3]) if len(children) > 3 else None
            operator_if_exists = children[2] if len(children) > 2 else None
            return Expression(operator_if_exists, terms)

    def transform(self, tree):
        if isinstance(tree, Tree):
            # print("this is the start from a tree node i.e. transform...")
            # print()
            # print("tree.data from transform is:",tree.data)
            # print()
            return self.__default__(tree)
        elif isinstance(tree, Token):
            # print("value from transform is:",tree.value)
            # print()
            if tree.type == 'NUM_LITERAL':
                # Convert the string value of NUM_LITERAL to an integer
                return int(tree.value)
            if tree.type == 'YAY':
                return True
            if tree.type == 'NAY':
                return False

            return tree.value
        else:
            raise ValueError(f"Unexpected input: {tree}")

# Final function to be used: 
# final_iteration(tree, tokens, graph=graph[0])
ast_builder = ASTBuilder()
rich.print(tree)
ast = ast_builder.transform(tree)
rich.print(ast)

# SEMANTIC ANALYSER

class SemanticError(Exception):
    pass

SymTable = {}

dict_of_types = { 
    'int':'num',
    'str':'str',
    'list':'list',
    'tuple':'tup',
    'bool':'flag'
}
dict_types = { 
    'num':'int',
    'str':'str',
    'list':'list',
    'tup':'tup',
    'flag':'bool'
}
                
class SemanticAnalyzer:
    def __init__(self):
        # Initializes the symbol table stack with a global scope
        self.symbol_table = {}
        self.scopes = []

    def enter_scope(self, scp):
        # Enter a new scope by adding a scope to the stack
        self.scopes.append(scp)
        self.symbol_table[scp] = {}

    def exit_scope(self):
        # Exit a scope by removing the most recently entered scope
        if len(self.symbol_table) >= 1:
            self.scopes.pop()
        else:
            raise SemanticError("Trying to exit the global scope")

    def declare_variable(self, name, data_type, mutability, size = None):
        print(self.symbol_table[self.scopes[-1]])
        print(self.scopes[-1])
        if name in self.symbol_table[self.scopes[-1]]:
            raise SemanticError(f"Variable '{name}' already declared in this scope")
        if size is not None:
            self.symbol_table[self.scopes[-1]][name] = {'type': data_type, 'mutability': mutability, 'size': size}
        else:  
            self.symbol_table[self.scopes[-1]][name] = {'type': data_type, 'mutability': mutability}
        print(self.scopes)

    def check_variable_declared(self, name):
        # Check if a variable is declared in any accessible scope
        # print(self.scopes[-1],"\nIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        if name in self.symbol_table[self.scopes[-1]]:
            print(self.scopes[-1])
            return self.symbol_table[self.scopes[-1]][name]
        elif self.scopes[-1] == 'Block':
            for i in range(len(self.scopes)-2,-1,-1):
                if name in self.symbol_table[self.scopes[i]]:
                    print(self.scopes[i])
                    return self.symbol_table[self.scopes[i]][name]
        elif 'parameters' in  self.symbol_table[self.scopes[-1]]:
            if name in self.symbol_table[self.scopes[-1]]['parameters']:
                print("found in parameters")
                print(name, self.symbol_table[self.scopes[-1]]['parameters'][name])
                return self.symbol_table[self.scopes[-1]]['parameters'][name]
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
                print("var_info:",var_info)
                if (type(var_info) is not dict) and (var_info in dict_types):
                    return dict_types[var_info]
                else:
                    return dict_types[var_info['type']]
            # else:
            #     return self.type_of_expression(expression.value)
        elif expression.__class__.__name__ == "Expression":
            expr_type_list = []
            for term in expression.terms:
                if term:
                    temp = self.type_of_expression(term)
                    expr_type_list.append(temp)
            exp_typ = expr_type_list[0]
            for i in expr_type_list:
                if (i != exp_typ):
                    exp_typ = "Undetermined"
                    break
            return exp_typ
        elif isinstance (expression, SpecialFunction):
            if expression.function_call:
                return self.visit(expression.function_call)
        elif isinstance(expression, BinaryOperator):
            # Handle binary operations like +, -, *, etc.
            # You need to determine the resulting type based on the operation
            # This is a simplified example and might need adjustment based on your language's rules
            left_type = self.type_of_expression(expression.left)
            right_type = self.type_of_expression(expression.right)
            # Assuming for simplicity that the result type is the same as the operand type
            return left_type if left_type == right_type else None
        elif isinstance(expression, (int, float)):
            return 'int'
    # Add more comprehensive handling here based on your expression AST node types

    # def visit_FunctionCall(self, node):
    #     if node.function_name not in 

    # You should add more comprehensive handling here based on your expression AST node types
    def visit_ListAppendTail(self, node):
        print('ListAppendTail')

        if node.tail is not None:
            var_info = self.check_variable_declared(node.identifier)
            print('var_info:',var_info)
            return (None,[])
        
        if node.append is not None:
            var_info = self.check_variable_declared(node.identifier)
            print('var_info:',var_info)
            return (None,[])

        else:        
            type_list = []
            length = len(node.elements)
            count = 0
            for i in node.elements:
                print("#########BLAHBLAHBLAH########################\n",i)
                if (isinstance(i, Expression)):
                        print(1)
                        if (isinstance(i.terms[1], Expression)):
                            print(2)
                            print(i)
                            ex_type = self.type_of_expression(i)
                            print()
                            print(ex_type)
                            if ex_type == "Undetermined":
                                raise SemanticError(f"Type mismatch in the index:{count+1}")
                            type_list.append(ex_type)
                        expr_type = self.type_of_expression(i.terms[0])
                        type_list.append(expr_type)
                        print(type_list)
                        count += 1
            return (length, type_list)

    def visit_VariableDeclaration(self, node):
        # node.data_type might contain "None num", "let num", or "fix num"
        if (node.data_type == 'list' or node.data_type == 'tup'):
            mutability =  None
            type_name = node.data_type
            print(mutability)
            print(type_name)
            (length_list, type_list_list) = self.visit(node.equal_to)
            if (length_list != None and len(type_list_list)!=0):
                print("Bhai yaha aaya")     
                size = length_list
                self.declare_variable(node.variable_name, type_name, mutability,size)

        elif node.size_array: #when the variable is an array
            print('array')
            if isinstance(node.size_array, int):
                if node.size_array < 0:
                    raise SemanticError(f"Array size must be a positive integer")
            else:
                raise SemanticError(f"Array size must be an integer")
            size = node.size_array
            
            # var_info = self.check_variable_declared(node.variable_name)

            print(node.equal_to)
            (length_arr, type_list_arr) = self.visit(node.equal_to)

            #pehle ye check karlo ki elements ki length ke size ke equal hai ya nahi
            if (length_arr != size):
                raise SemanticError(f"Size of array does not match the number of elements")

            #phir ek ek element ke type check karo
            for i in range(len(type_list_arr)):
                if type_list_arr[i] in dict_of_types.keys(): #like int to num conversion
                    type_list_arr[i] = dict_of_types[type_list_arr[i]]
                if type_list_arr[i] != type_name:
                    raise SemanticError(f"Type mismatch: variable '{node.variable_name}' declared as '{type_name}' but assigned '{type_list_arr[i]}'")
            # phir us variable ko symbol table me store karo 
            self.declare_variable(node.variable_name, type_name, mutability,size)
            
        else:
            mutability, type_name = node.data_type.split()
            print(mutability)
            print(type_name)
            test_lst = []
            if (node.equal_to):
                for i in node.equal_to[:-1]: #-1 is for epsilon
                    if (isinstance(i, Term)):
                        print(1)
                        expr_type = self.type_of_expression(i)
                        test_lst.append(expr_type)
                # change expr_type according to dict_of_types
                print('###################################')
                print(test_lst)
                test_lst = flatten_list(test_lst)
                print(test_lst)
                print('###################################')
                if  len(test_lst) > 0:
                    var_val_tp = test_lst[0]
                    for i in test_lst:
                        print("i is:", i)
                        if i != var_val_tp:
                            var_val_tp = "Undetermined"
                            break
                    if ((var_val_tp != "Undetermined") and (var_val_tp in dict_of_types.keys())):
                        var_val_tp = dict_of_types[var_val_tp]
                # for i in range(len(test_lst)):
                #     # print(j)
                #     print(dict_of_types['int'])
                #     print(2)
                #     # if j in dict_of_types:
                #     #     j = dict_of_types[j]
                #     # if test_lst[i] in dict_of_types.keys():
                #     #     test_lst[i] = dict_of_types[test_lst[i]]
                #     # if test_lst[i] != type_name:
                    if var_val_tp != type_name:
                        raise SemanticError(f"Type mismatch: variable '{node.variable_name}' declared as '{type_name}' but assigned '{var_val_tp}'")
                print(test_lst)
            self.declare_variable(node.variable_name, type_name, mutability)

    def visit_UnaryStatement(self, node):
        self.check_variable_declared(node.value)
    
    def visit_ShowStatement(self, node):
        for stmt in node.expressions:
            temp_type = self.type_of_expression(stmt)
            if temp_type == "Undetermined":
                raise SemanticError(f"Type mismatch in the expression in show statement")

    def visit_Assignment(self, node):
        var_info = self.check_variable_declared(node.variable_name)
        expr_type = self.type_of_expression(node.value)
        # print('before ka before:',expr_type)
        # expr_type = flatten_list(expr_type)
        # for i in range(len(expr_type)):
            # print('before ka before:',expr_type[i])
        if expr_type in dict_of_types.keys():
            print('before:', expr_type)
            expr_type = dict_of_types[expr_type]
        tp = expr_type
        print('expr_type:',expr_type)
        print('tp:',tp)
        if tp != var_info['type']:
            raise SemanticError(f"Type mismatch: variable '{node.variable_name}' expected '{var_info['type']}' but got '{tp}'")
        if var_info['mutability'] == 'fix':
            raise SemanticError(f"Cannot assign to constant variable '{node.variable_name}'")
        
    def visit_ConditionalStatement(self, node):
        # self.enter_scope("Conditional")n``1
        self.visit(node.conditional_argument)
        for statement in node.conditional_block.statements:
            self.type_of_expression(statement)
        if len(node.other_blocks) > 0:
            for other in node.other_blocks:
                self.visit(other)
        self.visit(node.otherwise_block)
        # self.exit_scope()
    
    def visit_Otherwise(self,node):
        self.visit(node.conditional_block)

    def visit_TryCatchStatement(self, node):
        self.enter_scope("Try")
        for stmt in node.try_block.statements:
            if stmt:
                self.visit(stmt)
        self.symbol_table['Try']['catch'] = node.catch_string
        self.enter_scope("Catch")
        for stmt in node.catch_block.statements:
            if stmt:
                self.visit(stmt)
        
        self.exit_scope()
        self.exit_scope()
    
    def visit_PopStatement(self,node):
        self.symbol_table[self.scopes[-1]]['pop'] = node.string_value

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
        if len(node.function_defs) > 0:
            for function_def in node.function_defs:
                self.visit(function_def)
        self.visit(node.main_function)
        # for func in node.function_defs:
        #     self.visit(func)

    def visit_MainFunc(self, node):
        self.enter_scope("main")
        for statement in node.statements:
            if statement:
                if type(statement) is list:
                    self.visit(statement[0])
                else:
                    self.visit(statement)
        rich.print(self.symbol_table)
        SymTable = self.symbol_table
        self.exit_scope()

    def visit_FunctionDef(self, node):
        self.enter_scope(node.function_name)
        self.symbol_table[node.function_name]['parameters'] = {
            'return_value': node.function_type
        }
        # self.symbol_table[node.function_name]['return_type'] = {'data_type': 'int'}
        for param in node.parameters:
            self.visit(param)
        for statement in node.function_block.statements:
            self.visit(statement)
        yield_type = self.type_of_expression(node.function_block.return_value)
        if (dict_of_types[yield_type] != node.function_type):
            raise SemanticError(f"return type must be {node.function_type} but was given {yield_type}")
        self.exit_scope()

    def visit_Parameter(self,node):
        fix_let, dt = node.data_type.split()
        # print(fix_let)
        param = node.parameter_name
        if fix_let != 'None':
            raise SemanticError(f"Parameter datatype in the function {self.scopes[-1]} can't have {fix_let} keyword.")
        else:
            self.symbol_table[self.scopes[-1]]['parameters'][param] = (dt,node.array_size) if node.array_size else dt
            self.symbol_table[self.scopes[-1]]['parameters'][param] = dt
            # if node.array_size:
            #     self.symbol_table[self.scopes[-1]][] =
        # print("\n\nvisited\n\n")
    
    # def visit_Expression(self, node):
    #     for term in node.terms:
    #         # print("now visiting in expression, terms: ", term)
    #         print(type(term))
    #         if term == "None":
    #             pass
    #         self.visit(term)
    
    def visit_Block(self, node):
        # enter scope for block
        self.enter_scope("Block")
        for statement in node.statements:
            # print("now visiting statement in block: ", statement)
            self.visit(statement)
        # exit scope for block
        self.exit_scope()

    def visit_LoopStatement(self, node):
        self.enter_scope("Loop")
        # print("node.loop_type:",node.loop_type)
        loop_type = node.loop_type
        if loop_type == 'while':
            # Visiting is_special
            # print("now visiting:",node.condition)
            self.type_of_expression(node.condition)
            # Visiting updation
            # print("now visiting:",node.updation)
            self.visit(node.updation)
            # Visiting block
            # print("now visiting:",node.block)
            self.visit(node.block)
        elif loop_type == 'iter':
            # Visiting declaration
            print("now visiting in iter declaraion:",node.declaration)
            self.visit(node.declaration)
            rich.print(self.symbol_table)
            # Visiting condition
            print("now visiting in iter condition:",node.condition)
            self.type_of_expression(node.condition)
            # Visiting updation
            print("now visiting in iter updation:",node.updation)
            self.visit(node.updation)
            # Visiting block
            print("now visiting in iter block:",node.block)
            self.visit(node.block)
        # TODO work is going on here. The above is giving an error
        self.exit_scope()
        # TODO elif for third type of loop ---> repeat-while

    def visit_ConditionalArgument(self, node):
        self.type_of_expression(node.expression)

    # Isko change karna padenga for loop
    def visit_Skip(self, node):
        # agar koi loop statement not found before this
        # then this is semantically incorrect
        # TODO : check if loop statement is present before this - PENDING 
        # Currently, Darshi is working on this part
        pass
    # def visit_Term(self, node):
    #     if node.identifier:
    #         self.check_variable_declared(node.identifier)

    def visit_NoneType(self, node):
        pass

analyzer = SemanticAnalyzer()
try:
    analyzer.visit(ast)
    print("Semantic analysis completed successfully.")
except SemanticError as e:
    print(f"Semantic error: {e}")

# Code Generation
type_map = {
    'num': 'int',
    'str': 'str',  # Python doesn't have char*, strings are used instead
    'list': 'list',   # Python list for any list type
    'tup': 'tuple', # Python tuple for tuple types
    'flag': 'bool', # Python's bool for flag
    'fix': 'const'
}

def write_code_main(node, file, symbol_table, ntabs=0):
    if node is None:
        return
    if node.__class__.__name__ == "function":
        # Assuming the main function setup
        file.write("int main() {\n")
        for child in node.children:
            write_code_main(child, file, symbol_table, ntabs + 1)
        file.write("\treturn 0;\n}\n")
    elif node.__class__.__name__ == "VariableDeclaration":
        print_tabs(ntabs, file)
        mut, dt = node.data_type.split()
        if mut == "fix":
            var_type = f"const {type_map[dt]}"
        else:
            var_type = f"{type_map[dt]}"
        # var_type = "int" if node.data_type == 'num' else "auto"
        file.write(f"{var_type} {node.variable_name}")
        if node.equal_to:
            for j in node.equal_to:
                if j is not None:
                    # Assuming the first term in equal_to contains the value for initialization
                    if j.__class__.__name__ == "Term":
                        value = j.value if j.value else (j.identifier if j.identifier else 0)
                        file.write(f" = {value}")
        file.write(";\n")
    elif node.__class__.__name__ == "Expression":
        if node.operator_if_exists:
            file.write(f" {node.operator_if_exists} ")
            for term in node.terms:
                write_code_main(term,file,symbol_table,ntabs)
        else:
            for term in node.terms:
                write_code_main(term,file,symbol_table,ntabs)
    elif node.__class__.__name__ == "Term":
        if node.value:
            file.write(f"{node.value}")
        elif node.identifier:
            file.write(f"{node.identifier}")
    elif node.__class__.__name__ == "Assignment":
        print_tabs(ntabs, file)
        file.write(f"{node.variable_name} {node.assignment_operators} ")
        write_code_main(node.value,file,symbol_table,ntabs)
        file.write(";\n")
    elif node.__class__.__name__ == "ShowStatement":
        file.write(f"std::cout << ")
        for expr in node.expressions:
            if expr.terms[0].value:
                print_tabs(ntabs, file)
                file.write(f"\"{expr.terms[0].value}\" << ' ' << ")
            elif expr.terms[0].identifier:
                print_tabs(ntabs, file)
                file.write(f"{expr.terms[0].identifier} ")
        file.write("<< std::endl;\n")
    else:
        file.write("int main() {\n")
        for child in node.statements:
            write_code_main(child, file, symbol_table, ntabs + 1)
        file.write("\treturn 0;\n}\n")

def write_expression(expression, file, symbol_table):
    if expression.operator_if_exists:
        left = expression.terms[0].identifier
        right = expression.terms[1].identifier if len(expression.terms) > 1 else ""
        operator = expression.operator_if_exists
        file.write(f"{left} {operator} {right}")
    else:
        file.write(expression.terms[0].identifier)

def print_tabs(ntabs, file):
    file.write('\t' * ntabs)

def generate_cpp_code(ast):
    output_filename = "generated_code.cpp"
    symbol_table = {
        'a': {'type': 'num', 'mutability': 'fix'},
        'b': {'type': 'num', 'mutability': 'fix'},
        'ans': {'type': 'num', 'mutability': 'None'}
    }
    with open(output_filename, 'w') as file:
        file.write("#include <iostream>\n\n")
        write_code_main(ast.main_function, file, symbol_table, 0)

import subprocess
# Assuming 'ast' is your Abstract Syntax Tree instance
if __name__ == '__main__':
    generate_cpp_code(ast)
    subprocess.run(["g++", "generated_code.cpp", "-o", "gp"])
    subprocess.run(["./gp"])

