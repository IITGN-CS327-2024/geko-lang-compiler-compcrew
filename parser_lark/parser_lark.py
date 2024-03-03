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
grammar = """
start: statement+

statement: assignment
         | expression END_OF_LINE

assignment: IDENTIFIER ASSIGNMENT_OPERATOR expression

expression: primary_expression
          | expression BINARY_OPERATOR expression

primary_expression: IDENTIFIER
                   | NUM_LITERAL
                   | OPEN_PARENTHESIS expression CLOSE_PARENTHESIS

END_OF_LINE: "END_OF_LINE"
IDENTIFIER: "IDENTIFIER"
ASSIGNMENT_OPERATOR: "ASSIGNMENT_OPERATOR"
BINARY_OPERATOR: "BINARY_OPERATOR"
NUM_LITERAL: "NUM_LITERAL"
OPEN_PARENTHESIS: "OPEN_PARENTHESIS"
CLOSE_PARENTHESIS: "CLOSE_PARENTHESIS"

%import common.NUMBER
%import common.WS
%ignore WS"""

# Create the Lark parser
parser = Lark(grammar, start='start', parser = 'lalr')#, lexer = CustomLexer)
code = """a + b;"""

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