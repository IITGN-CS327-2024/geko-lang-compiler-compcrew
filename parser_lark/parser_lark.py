from lark import Lark
from lark.lexer import Lexer, Token
from lark.exceptions import UnexpectedToken
import re
    
grammar = """
start                   :   program
program	                :	DEFINE NUM MAIN OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_BRACES statements YIELD NUM_LITERAL END_OF_LINE CLOSE_BRACES
                        |   DEFINE function_type IDENTIFIER OPEN_PARENTHESIS parameter_list CLOSE_PARENTHESIS function_block program

# --------------------------------------

function_block	        :	OPEN_BRACES statements YIELD return_value END_OF_LINE CLOSE_BRACES
function_type	        :	NUM | STR | FLAG | VOID
parameter_list	        :	parameter parameters | epsilon
return_value	        :	NUM_LITERAL | string | YAY | NAY | epsilon
parameters	            :	ELEMENT_SEPERATOR parameter parameters 
                        |   epsilon
parameter	            :	compound_data_type IDENTIFIER | basic_data_type IDENTIFIER choose_array
choose_array            :   OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET | epsilon                        
# --------------------------------------
statements	            :	statement statements
                        |   epsilon
equal_to                :   EQUAL_TO post_equal_to | epsilon
post_equal_to           :   ENTER OPEN_PARENTHESIS string CLOSE_PARENTHESIS 
                        |   IDENTIFIER OPEN_BRACKET NUM_LITERAL SLICING_COLON NUM_LITERAL CLOSE_BRACKET
                        |   LENGTH OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS
                        |   IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET
                        |   HEAD OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS
                        |   ISEMPTY OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS
                        |   function_call
                        |   let_in_statement 
                        |   expression


data_type	            :  	basic_data_type 
                        |   compound_data_type 
                        |   epsilon
num_str_flag	        :	NUM | STR | FLAG
basic_data_type	        :	fix_let num_str_flag
fix_let	                :	FIX | LET | epsilon
compound_data_type	    :	LIST | TUP


string	                :	TILDE STRING_LITERAL TILDE
array	                :	basic_data_type IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET

# --------------------------------------

variable_declaration	:	basic_data_type IDENTIFIER equal_to
                        |   compound_array compound_var

compound_array          :   compound_data_type IDENTIFIER
                        |   array 

compound_var            :   EQUAL_TO list_append_tail 
                        |   epsilon

list_append_tail        :   OPEN_BRACKET expression expressions CLOSE_BRACKET
                        |   TAIL OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS
                        |   APPEND OPEN_PARENTHESIS expression ELEMENT_SEPERATOR IDENTIFIER CLOSE_PARENTHESIS

assignment_statement	:	IDENTIFIER assignment_operators post_equal_to
show_statement	        :	SHOW OPEN_PARENTHESIS expression expressions CLOSE_PARENTHESIS
block	                :	OPEN_BRACES statements CLOSE_BRACES
value_change_array	    :	IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET assignment_operators expression
#---------------------------------------

expressions             :   ELEMENT_SEPERATOR expression expressions
                        |   epsilon
expression	            :   term terms | epsilon
terms	                :	binary_operators term terms 
                        |   epsilon
#---------------------------------------
term	                :   IDENTIFIER
                        |   NUM_LITERAL
                        |   string
                        |   YAY
                        |   NAY
                        |   OPEN_PARENTHESIS expression CLOSE_PARENTHESIS
                        |   unary_operators IDENTIFIER
                        |   IDENTIFIER UNARY_OPERATOR
                        |   IDENTIFIER OPEN_BRACKET expression CLOSE_BRACKET
#---------------------------------------
binary_operators	    :	BINARY_OPERATOR 
                        |   COMPARISON_OPERATOR 
                        |   BINARY_LOGICAL_OPERATOR
unary_operators	        :	UNARY_OPERATOR
                        |   UNARY_LOGICAL_OPERATOR
assignment_operators	:	EQUAL_TO
                        |   ASSIGNMENT_OPERATOR
#---------------------------------------
conditional_block       :   yield_block 
                        |   block
conditional_statement	:	GIVEN OPEN_PARENTHESIS expression CLOSE_PARENTHESIS conditional_block other_block otherwise_block
other_block	            :	OTHER OPEN_PARENTHESIS expression CLOSE_PARENTHESIS conditional_block other_block
                        |   epsilon 
otherwise_block	        :	OTHERWISE conditional_block
                        |   epsilon
skip_stop               :   SKIP
                        |   STOP
#---------------------------------------

loop_statement	        :	ITER OPEN_PARENTHESIS statement expression END_OF_LINE expression CLOSE_PARENTHESIS block
                        |   WHILE OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block
                        |   REPEAT block WHILE OPEN_PARENTHESIS expression CLOSE_PARENTHESIS END_OF_LINE

#---------------------------------------

pop_statement           :   POP OPEN_PARENTHESIS string CLOSE_PARENTHESIS

try_catch_statement	    :	TEST block ARREST OPEN_PARENTHESIS string CLOSE_PARENTHESIS block

yield_block             :   OPEN_BRACES statements YIELD expression END_OF_LINE CLOSE_BRACES

#---------------------------------------

function_call	        :	IDENTIFIER OPEN_PARENTHESIS argument_list CLOSE_PARENTHESIS

argument_list	        :	expression expressions

#---------------------------------------
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

"""
function_definitions	:	function_definiton function_definitions     
                        |   epsilon
function_definition	    :	DEFINE function_type IDENTIFIER OPEN_PARENTHESIS parameter_list CLOSE_PARENTHESIS function_block
function_block	        :	OPEN_BRACES statements YIELD return_value END_OF_LINE CLOSE_BRACES


statements	            :	statement statements 
                        |   epsilon

return_value	        :	NUM_LITERAL 
                        |   string 
                        |   YAY 
                        |   NAY                    
                        |   epsilon

function_type	        :	NUM 
                        |   STR 
                        |   FLAG 
                        |   VOID

parameter_list	        :	parameter parameters 
                        |   epsilon
parameters	            :	ELEMENT_SEPERATOR parameter parameters 
                        |   epsilon
parameter	            :	data_type IDENTIFIER 
                        | array
array	                :	data_type IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET
statement	            :	variable_declaration END_OF_LINE
                        |   assignment_statement END_OF_LINE
                        |   block
                        |   show_statement END_OF_LINE
                        |   conditional_statement
                        |   loop_statement
                        |   return_statement END_OF_LINE
                        |   try_catch_statement
                        |   function_call END_OF_LINE
                        |   enter_statement END_OF_LINE
                        |   pop_statement END_OF_LINE
                        |   let_in_statement
                        |   slice_string
                        |   length
                        |   element_access
                        |   value_change_array
                        |   list_head
                        |   list_tail
                        |   append_list
                        |   isEmpty_list
                        |   skip_stop END_OF_LINE
                        |   epsilon
string	            :	TILDE STRING_LITERAL TILDE 
                    |   epsilon
fix_let	            :	FIX 
                    |   LET
                    |   epsilon
num_str_flag	    :	NUM 
                    |   STR 
                    |   FLAG
basic_data_type	    :	fix_let num_str_flag
compound_data_type	:	LIST 
                    |   TUP
data_type	        :  	basic_data_type 
                    |   compound_data_type 
                    |   epsilon
expressions	        :	ELEMENT_SEPERATOR expression expressions | epsilon
expression	        :	term terms | epsilon
binary_operators	:	BINARY_OPERATOR | COMPARISON_OPERATOR | BINARY_LOGICAL_OPERATOR
unary_operators	    :	UNARY_OPERATOR | UNARY_LOGICAL_OPERATOR
terms	            :	binary_operators term terms | epsilon
term	            :   IDENTIFIER
                    |   NUM_LITERAL
                    |   string
                    |   FLAG
                    |   OPEN_PARENTHESIS expression CLOSE_PARENTHESIS
                    |   unary_operators IDENTIFIER
                    |   IDENTIFIER UNARY_OPERATOR
block	                :	OPEN_BRACES statements CLOSE_BRACES
assignment_operators	:	EQUAL_TO | ASSIGNMENT_OPERATOR
equal_to	            :  	EQUAL_TO expression | epsilon
variable_declaration	:	basic_data_type IDENTIFIER equal_to
                        |   compound_array compound_var
compound_var	        :	EQUAL_TO OPEN_BRACKET expression expressions CLOSE_BRACKET | epsilon
compound_array	        :	compound_data_type IDENTIFIER | array
assignment_statement	:	IDENTIFIER assignment_operators expression
show_statement	        :	SHOW OPEN_PARENTHESIS expression expressions CLOSE_PARENTHESIS
conditional_statement	:	GIVEN OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block other_block (OTHERWISE block | epsilon)
otherwise_block	    :	OTHERWISE block | epsilon
other_block	        :	OTHER OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block other_block | epsilon
loop_statement	    :	ITER OPEN_PARENTHESIS expression END_OF_LINE expression END_OF_LINE expression CLOSE_PARENTHESIS block
                    |   WHILE OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block
                    |   REPEAT block WHILE OPEN_PARENTHESIS expression CLOSE_PARENTHESIS END_OF_LINE
return_statement	:	YIELD expression | YIELD OPEN_PARENTHESIS expression CLOSE_PARENTHESIS
try_catch_statement	:	TEST block ARREST OPEN_PARENTHESIS string CLOSE_PARENTHESIS block
function_call	    :	IDENTIFIER OPEN_PARENTHESIS argument_list CLOSE_PARENTHESIS
argument_list	    :	expression expressions | epsilon
enter_statement	    :	basic_data_type IDENTIFIER EQUAL_TO ENTER OPEN_PARENTHESIS string CLOSE_PARENTHESIS
str	                :	STR | epsilon
slice_string	    :	str IDENTIFIER EQUAL_TO IDENTIFIER OPEN_BRACKET NUM_LITERAL SLICING_COLON NUM_LITERAL CLOSE_BRACKET
length	            :	NUM IDENTIFIER assignment_operators LENGTH OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS END_OF_LINE
element_access	    :	basic_data_type IDENTIFIER EQUAL_TO IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE BRACKET END_OF_LINE
value_change_array	:	IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET assignment_operators expression END_OF_LINE
list_head	        :	basic_data_type IDENTIFIER assignment_operators HEAD OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS END_OF_LINE
list_tail	        :	LIST IDENTIFIER EQUAL_TO TAIL OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS END_OF_LINE
append_list	        :	LIST IDENTIFIER EQUAL_TO APPEND OPEN_PARENTHESIS expression ELEMENT_SEPARATOR IDENTIFIER CLOSE_PARENTHESIS END_OF_LINE
let_in_statement	:	LET data_type IDENTIFIER ASSIGNMENT_OPERATOR term END_OF_LINE
                    |   OPEN_BRACES statements let_in_statement statements CLOSE BRACES
isEmpty_list	    :	FLAG IDENTIFIER EQUAL_TO ISEMPTY OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS END_OF_LINE
pop_statement	    :	POP OPEN_BRACKET string CLOSE_BRACKET
skip_stop       	:	SKIP | STOP
epsilon : ""
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
# Create the Lark parser
parser = Lark(grammar, start='start', parser = 'lalr')#, lexer = CustomLexer)
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
    yield;
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
    num test_enter;
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
    yield 0;
}
    """

import lexer_lark

tokens = lexer_lark.lexer(code)
# print(type(tokens))
# for token in tokens:
#     print(type(token), "-->", token)

# small_tokens = []
# small_code = "list five = [1,2,yay,~meow~,5];"
# small_tokens = lexer_lark.lexer(small_code)
# for token in small_tokens:
#     print(type(token), "-->", token)

for token in tokens:
    print(type(token), "-->", token)
tokenised_code = ""

for token in tokens:
    # print(type(token[0]))
    tokenised_code += token[0] + " "
# print(type(tokenised_code), "-->" , tokenised_code)
# tree = parser.parse(code)
tree = parser.parse(tokenised_code)
print("Parsed tree:\n", tree.pretty())
# try:
#     # Parse the input code
#     parser.parse(code)
#     # If parsing is successful, print success message
#     print("Parsing successful!")
# except UnexpectedToken as e:
#     # If parsing fails, print the error
#     print("Parsing error:", e)

# --------------------------------------
# IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
# ASSIGNMENT_OPERATOR: "="
# BINARY_OPERATOR: "+" | "-" | "*" | "/" 
# NUM_LITERAL: /-?\d+/
# OPEN_PARENTHESIS: "("
# CLOSE_PARENTHESIS: ")"
# END_OF_LINE: ";"
# --------------------------------------
