import ply.lex as lex
import ply.yacc as yacc

# Define tokens
tokens = (
    'NUM',
    'PLUS',
)

# Define token rules
t_NUM = r'\d+'
t_PLUS = r'\+'

# Ignored characters
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

from geko_lexer import GekoLexer

lexer = GekoLexer.lex()

# Define parser rules
def p_expression(p):
    '''expression : NUM PLUS NUM'''
    p[0] = int(p[1]) + int(p[3])

# Build the parser
parser = yacc.yacc()

# Parse input string
result = parser.parse('7 + 3')
print(result)  # Output: 5
