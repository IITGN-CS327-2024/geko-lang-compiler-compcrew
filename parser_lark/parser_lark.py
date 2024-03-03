from lark import Lark
from lark.lexer import Lexer, Token
from lark.exceptions import UnexpectedToken
import re

class CustomLexer(Lexer):
    def __init__(self, lexer_conf):
        pass
    def lex(self, data):
        # Define token patterns using regular expressions
        patterns = [
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
            ('END_OF_LINE', r';'),
            ('SLICING_COLON', r':'),
            ('ELEMENT_SEPERATOR', r','),
            ('COMPARISON_OPERATOR', r'==|!=|<=|>=|>|<'),
            ('ASSIGNMENT_OPERATOR', r'=|/=|\*=|\+=|-=|%='),
            ('UNARY_OPERATOR' , r'\+\+|--|`'),
            ('BINARY_OPERATOR', r'\*\*|/|\*|\+|-|%'),
            ('BINARY_LOGICAL_OPERATOR', r'&&|\|\||&|\||\^'),
            ('UNARY_LOGICAL_OPERATOR', r'!')
        ]

        # Combine patterns into a single regular expression through join()
        pattern = '|'.join('(?P<%s>%s)' % pair for pair in patterns)

        # Empty list to store tokens
        tokens = []

        # Loop over matches found in the code using the specified pattern
        for match in re.finditer(pattern, data):
            # Extract the kind (token type) and value from the match
            kind = match.lastgroup
            value = match.group()

            # Handle special case for STRING_LITERAL where ~, <string>, ~ will be treated separately
            if kind == 'STRING_LITERAL':
                # String value without quotes
                string_val = value[1:-1]

                # Add tokens for string delimiters (~) and the string value
                tokens.append(('TILDE', '~'))
                tokens.append((kind, string_val))
                tokens.append(('TILDE', '~'))
            else:
                # For other token types, simply add the kind and value to the tokens list
                tokens.append((kind, value))

        # Return the list of tokens
        # return tokens
        lark_tokens = [Token(type_, value) for type_, value in tokens]

        return lark_tokens
    

# Define your custom grammar
# grammar = """
# start: statement+

# statement: assignment
#          | expression END_OF_LINE

# assignment: IDENTIFIER ASSIGNMENT_OPERATOR expression

# expression: primary_expression
#           | expression BINARY_OPERATOR expression

# primary_expression: IDENTIFIER
#                    | NUM_LITERAL
#                    | OPEN_PARENTHESIS expression CLOSE_PARENTHESIS

# END_OF_LINE: "END_OF_LINE"
# IDENTIFIER: "IDENTIFIER"
# ASSIGNMENT_OPERATOR: "ASSIGNMENT_OPERATOR"
# BINARY_OPERATOR: "BINARY_OPERATOR"
# NUM_LITERAL: "NUM_LITERAL"
# OPEN_PARENTHESIS: "OPEN_PARENTHESIS"
# CLOSE_PARENTHESIS: "CLOSE_PARENTHESIS"

# %import common.NUMBER
# %import common.WS
# %ignore WS"""
    

grammar = """
start                   :   program
program	                :	function_definitions DEFINE NUM MAIN OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_BRACES statements YIELD NUM_LITERAL END_OF_LINE CLOSE_BRACES
statements	            :	statement #statements
statement               :   epsilon
function_definitions    :   epsilon
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

"""
function_definitions	:	function_definiton function_definitions | epsilon
function_definition	    :	DEFINE function_type IDENTIFIER OPEN_PARENTHESIS parameter_list CLOSE_PARENTHESIS function_block
function_block	        :	OPEN_BRACES statements YIELD return_value END_OF_LINE CLOSE_BRACES


statements	            :	statement statements | epsilon
return_value	        :	NUM_LITERAL | string | YAY | NAY | epsilon
function_type	        :	NUM | STR | FLAG | VOID
parameter_list	        :	parameter parameters | epsilon
parameters	            :	ELEMENT_SEPERATOR parameter parameters | epsilon
parameter	            :	data_type IDENTIFIER | array
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
string	            :	TILDE STRING_LITERAL TILDE | epsilon
fix	                :	FIX | epsilon
num_str_flag	    :	NUM | STR | FLAG
basic_data_type	    :	fix num_str_flag
compound_data_type	:	LIST | TUP
data_type	        :  	basic_data_type | compound_data_type | epsilon
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
code = """define num main() {yield 0;}"""

import lexer_lark

tokens = lexer_lark.lexer(code)
# print(type(tokens))
# for token in tokens:
#     print(type(token), "-->", token)

tokenised_code = ""

for token in tokens:
    # print(type(token[0]))
    tokenised_code += token[0]
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
