from lark import Lark
from lark.lexer import Lexer, Token
from lark.exceptions import UnexpectedToken
import re
import ast_lexer_lark as lexer_lark
import sys
import os
# ----------------------------------------------------------------------------------------------------------------------------
import lark
import pydot
from IPython.display import display
# ----------------------------------------------------------------------------------------------------------------------------
from lark import Transformer, v_args
from dataclasses import dataclass
# ----------------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass

# ----------------------------------------------------------------------------------------------------------------------------
# Dataclasses for the AST
@dataclass
class Program:
    statements: list

@dataclass
class FunctionDefinition:
    function_type: str
    identifier: str
    parameters: list
    function_block: list

@dataclass
class StatementBlock:
    statements: list

@dataclass
class Statement:
    statement: object

@dataclass
class Assignment:
    variable: str
    expression: object

@dataclass
class IfStatement:
    condition: object
    body: object

@dataclass
class FunctionCall:
    function_name: str
    arguments: list

@dataclass
class ShowStatement:
    expression: object

@dataclass
class ValueChangeArray:
    identifier: str
    index: int
    expression: object

@dataclass
class PopStatement:
    identifier: str

@dataclass
class TryCatchStatement:
    test_block: object
    exception_name: str
    arrest_block: object

@dataclass
class YieldBlock:
    statements: list
    expression: object

@dataclass
class ArgumentList:
    arguments: list

@dataclass
class LetInBraces:
    statement: object

@dataclass
class LetIn:
    data_type: str
    identifier: str
    expression: object

@dataclass
class LetInStatement:
    let_ins: list

@dataclass
class LoopStatement:
    loop_type: str
    statement: object
    condition: object

@dataclass
class SkipStop:
    command: str

# ----------------------------------------------------------------------------------------------------------------------------

# Transformer class
@v_args(inline=True)
# Transformer class
@v_args(inline=True)
class MyTransformer(Transformer):
    def start(self, *args):
        return Program(args[0])

    def func_def(self, *args):
        return FunctionDefinition(*args)

    def statements(self, *args):
        return StatementBlock(args)

    def statement(self, *args):
        return Statement(args[0])

    def assignment_statement(self, *args):
        return Assignment(*args)

    def if_statement(self, *args):
        return IfStatement(*args)

    def function_call(self, *args):
        return FunctionCall(*args)

    def show_statement(self, *args):
        return ShowStatement(*args)

    def value_change_array(self, *args):
        return ValueChangeArray(*args)

    def pop_statement(self, *args):
        return PopStatement(*args)

    def try_catch_statement(self, *args):
        return TryCatchStatement(*args)

    def yield_block(self, *args):
        return YieldBlock(*args)

    def argument_list(self, *args):
        return ArgumentList(args)

    def let_in_braces(self, *args):
        return LetInBraces(*args)

    def let_in(self, *args):
        return LetIn(*args)

    def let_in_statement(self, *args):
        return LetInStatement(*args)

    def loop_statement(self, *args):
        return LoopStatement(*args)

    def skip_stop(self, *args):
        return SkipStop(*args)

    # Other methods...
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
define num main(){
    given(meow){
        num x = 4;
    }
	yield 0;
}
"""

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

# parser = Lark(grammar)
tree = parser.parse(tokenised_code)
transformer = MyTransformer()
ast = transformer.transform(tree)
print(ast)
print(type(ast))

# --------------------------------------

# graph_of_tree = lark.tree.pydot__tree_to_graph(tree)

#---------------------------------------

# graph = pydot.graph_from_dot_data(lark.tree.pydot__tree_to_graph(tree).to_string())
# function toh chal gaya
# print(type(graph[0]))

#----------------------------------------------------------------------------------------------------------------------------

# png_name = "parse_tree.png"
# graph[0].write_png(png_name)

# graph bhi chal gaya!
#----------------------------------------------------------------------------------------------------------------------------

# leaf_nodes = []
# dfs(tree, leaf_nodes)

# ----------------------------------------------------------------------------------------------------------------------------

# Final function to be used: 
# final_iteration(tree, tokens, graph=graph[0])

# ----------------------------------------------------------------------------------------------------------------------------

# leaf_nodes_new = []
# dfs(tree, leaf_nodes_new)

# ----------------------------------------------------------------------------------------------------------------------------

# FINAL GRAPH:
# graph_of_tree_modified = pydot.graph_from_dot_data(lark.tree.pydot__tree_to_graph(tree).to_string())
# # Writing the graph to a PNG file
# png_name = "modified_parse_tree.png"
# graph_of_tree_modified[0].write_png(png_name)
# print("The modified parse tree has been written to", png_name, "inside ./correct_testcases")

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


# bas reference ke liye, abhi iska kuch nahi karna   
code = """
define void meow(num test_num, flag test_bool){
    given(test_num == 3){
        yield;
        }
    while(test_num > 0){
        show(test_num);
        test_num = test_num - 1;
        given(test_num == 2){
            yield;
            }
    }
    define num foo(num rand_int){
        yield rand_int;
    }
    num test_let = let test_num = 3 in { let test_num_2 = 4 in test_num + test_num_2};
    yield foo(3);
    } 
define num main() {
    fix num one = 3;
    num two = 4;
    num three;
    three = one + two;
    ## this is a comment
    str four = ~hello~;
    ## two = 5;
    list five = [1,2,Yay,~meow~,5];
    show(five[2+3]);
    flag test_empty = isEmpty(five);
    ## num test_declaration = foo(three, four);
    given(1==1){
        pop(~pop testing~);
        show(1);
    }
    other(three > four){
        show(2);
    }
    otherwise{
        show(2);
    }

    test{
        num a = 2;
        num b = 0;
        given(b == 0){
            pop(~pop testing~);
            }
    }
    arrest(~pop testing~){
        show(~error aayi hai!~);
    }

    add();

    num test_func = meow(3, Yay);
    list test_list_tail = tail(five);
    iter(num i = 0; i < three; i++){
        show(~meow~, i);
        skip;
    }

    while(three > 0){
        show(three);
        three = three - 1;
        stop;
        show(three);
    }

    repeat{
        show(three);
        three = three - 1;
    }while(three > 0);
    
    num a = 2;
    a += length(five);
    a %= five[1];
    five[1] = 5;
    num b = head(five);
    ## list c = tail(five);
    num test_enter = 9;
    num sum = a + test_enter;
    list test_append = append(~append test~, five);
    test_enter = enter(~hello~);
    str test_slice = four[1:2];
    num test_num_let_recurse = let test_num = 3 in { let test_num_2 = 4 in test_num + test_num_2};

    let num test_let_assgn = 5;
    num test_num = 0;
    test_num++;
    test_num--;
    ## --test_num++;
    given(three){
    }
    show(~);
    yield 0;
}
    """
