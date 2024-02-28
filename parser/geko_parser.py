# geko_parser.py

# Tokens
tokens = [
    'DEFINE', 'NUM', 'STR', 'FLAG', 'VOID', 'MAIN', 'OPEN_PARENTHESIS', 'CLOSE_PARENTHESIS', 'OPEN_BRACES', 'CLOSE_BRACES',
    'YIELD', 'SEMICOLON', 'ELEMENT_SEPERATOR', 'ASSIGNMENT_OPERATOR', 'SHOW', 'STRING_LITERAL',
    'GIVEN', 'OTHER', 'OTHERWISE', 'ITER', 'SLICING_COLON', 'WHILE', 'REPEAT', 'TEST', 'POP',
    'ARREST', 'ENTER', 'IDENTIFIER', 'NUM_LITERAL', 'BINARY_OPERATOR', 'COMPARISON_OPERATOR', 'UNARY_OPERATOR',
    'LIST', 'TUP', 'VOID', 'FLAG', 'BOOLEAN', 'STR'
]

# Tokens
t_ignore = ' \t\n'

# Tokens
t_DEFINE = r'DEFINE'
t_NUM = r'NUM'
t_MAIN = r'MAIN'
t_OPEN_PARENTHESIS = r'\('
t_CLOSE_PARENTHESIS = r'\)'
t_OPEN_BRACES = r'{'
t_CLOSE_BRACES = r'}'
t_YIELD = r'YIELD'
t_SEMICOLON = r';'
t_ELEMENT_SEPERATOR = r','
t_ASSIGNMENT_OPERATOR = r'='
t_SHOW = r'SHOW'
t_STRING_LITERAL = r'"([^"])*"'
t_GIVEN = r'GIVEN'
t_OTHER = r'OTHER'
t_OTHERWISE = r'OTHERWISE'
t_ITER = r'ITER'
t_SLICING_COLON = r':'
t_WHILE = r'WHILE'
t_REPEAT = r'REPEAT'
t_TEST = r'TEST'
t_POP = r'POP'
t_ARREST = r'ARREST'
t_ENTER = r'ENTER'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUM_LITERAL = r'\d+'
t_BINARY_OPERATOR = r'\*\*|\*|\/|\+|-|%|\&|\|'
t_COMPARISON_OPERATOR = r'<|>|<=|>=|==|!='
t_UNARY_OPERATOR = r'\+|-|!|\+\+|--'
t_LIST = r'LIST'
t_TUP = r'TUP'
t_VOID = r'VOID'
t_FLAG = r'FLAG'

# Parsing rules
def p_program(p):
    '''program : function_definition_list DEFINE NUM MAIN OPEN_PARENTHESIS CLOSE_PARENTHESIS block YIELD NUM_LITERAL SEMICOLON'''
    p[0] = ('program', p[1], p[7], p[10])

def p_function_definition_list(p):
    '''function_definition_list : function_definition function_definition_list
                                 | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_function_definition(p):
    '''function_definition : DEFINE function_type IDENTIFIER OPEN_PARENTHESIS parameter_list CLOSE_PARENTHESIS block'''
    p[0] = ('function_definition', p[2], p[3], p[5], p[7])

def p_function_type(p):
    '''function_type : NUM
                     | STR
                     | FLAG
                     | VOID'''
    p[0] = p[1]

def p_parameter_list(p):
    '''parameter_list : parameter ELEMENT_SEPERATOR parameter_list
                      | parameter
                      | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_parameter(p):
    '''parameter : data_type IDENTIFIER'''
    p[0] = ('parameter', p[1], p[2])

def p_block(p):
    '''block : OPEN_BRACES statement_list CLOSE_BRACES'''
    p[0] = ('block', p[2])

def p_statement_list(p):
    '''statement_list : statement SEMICOLON statement_list
                      | statement SEMICOLON
                      | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_statement(p):
    '''statement : variable_declaration
                 | assignment_statement
                 | block
                 | show_statement
                 | conditional_statement
                 | loop_statement
                 | return_statement
                 | try_catch_statement
                 | function_call
                 | enter_statement'''
    p[0] = p[1]

def p_variable_declaration(p):
    '''variable_declaration : data_type IDENTIFIER ASSIGNMENT_OPERATOR expression'''
    p[0] = ('variable_declaration', p[1], p[2], p[4])

def p_assignment_statement(p):
    '''assignment_statement : IDENTIFIER ASSIGNMENT_OPERATOR expression'''
    p[0] = ('assignment_statement', p[1], p[3])

def p_show_statement(p):
    '''show_statement : SHOW OPEN_PARENTHESIS expression expression_list CLOSE_PARENTHESIS'''
    p[0] = ('show_statement', p[3], p[4])

def p_expression_list(p):
    '''expression_list : ELEMENT_SEPERATOR expression expression_list
                       | empty'''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_conditional_statement(p):
    '''conditional_statement : GIVEN OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block
                             | GIVEN OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block OTHERWISE block
                             | GIVEN OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block OTHER OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block
                             | GIVEN OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block OTHERWISE block OTHER OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block'''
    if len(p) == 6:
        p[0] = ('conditional_statement', p[3], p[5], None, None)
    elif len(p) == 7:
        p[0] = ('conditional_statement', p[3], p[5], p[6], None)
    elif len(p) == 9:
        p[0] = ('conditional_statement', p[3], p[5], p[6], p[8])
    else:
        p[0] = ('conditional_statement', p[3], p[5], p[9], p[11])

def p_loop_statement(p):
    '''loop_statement : ITER OPEN_PARENTHESIS expression SLICING_COLON expression SLICING_COLON expression CLOSE_PARENTHESIS block
                      | WHILE OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block
                      | REPEAT block WHILE OPEN_PARENTHESIS expression CLOSE_PARENTHESIS'''
    if len(p) == 10:
        p[0] = ('iter_loop', p[3], p[5], p[7], p[9])
    elif len(p) == 6:
        p[0] = ('while_loop', p[3], p[5])
    else:
        p[0] = ('repeat_loop', p[2], p[5], p[7])

def p_return_statement(p):
    '''return_statement : YIELD expression'''
    p[0] = ('return_statement', p[2])

def p_try_catch_statement(p):
    '''try_catch_statement : TEST block POP STRING_LITERAL ARREST OPEN_PARENTHESIS STRING_LITERAL CLOSE_PARENTHESIS block'''
    p[0] = ('try_catch_statement', p[2], p[4], p[7], p[9])

def p_function_call(p):
    '''function_call : IDENTIFIER OPEN_PARENTHESIS argument_list CLOSE_PARENTHESIS'''
    p[0] = ('function_call', p[1], p[3])

def p_argument_list(p):
    '''argument_list : expression ELEMENT_SEPERATOR argument_list
                     | expression
                     | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_enter_statement(p):
    '''enter_statement : data_type IDENTIFIER ASSIGNMENT_OPERATOR ENTER OPEN_PARENTHESIS STRING_LITERAL CLOSE_PARENTHESIS'''
    p[0] = ('enter_statement', p[1], p[2], p[6])

def p_expression(p):
    '''expression : term
                  | term BINARY_OPERATOR expression
                  | term COMPARISON_OPERATOR term'''
    if len(p) == 2:
        p[0] = ('expression', p[1])
    else:
        p[0] = ('expression', p[2], p[1], p[3])

def p_term(p):
    '''term : factor
            | factor BINARY_OPERATOR term
            | factor COMPARISON_OPERATOR factor'''
    if len(p) == 2:
        p[0] = ('term', p[1])
    else:
        p[0] = ('term', p[2], p[1], p[3])

def p_factor(p):
    '''factor : IDENTIFIER
              | NUM_LITERAL
              | STRING_LITERAL
              | BOOLEAN
              | OPEN_PARENTHESIS expression CLOSE_PARENTHESIS
              | UNARY_OPERATOR expression'''
    if len(p) == 2:
        p[0] = ('factor', p[1])
    else:
        p[0] = ('factor', p[1], p[2])

def p_identifier(p):
    '''identifier : IDENTIFIER'''
    p[0] = ('identifier', p[1])

def p_number(p):
    '''number : NUM_LITERAL'''
    p[0] = ('number', p[1])

def p_string(p):
    '''string : STRING_LITERAL'''
    p[0] = ('string', p[1])

def p_boolean(p):
    '''boolean : FLAG'''
    p[0] = ('boolean', p[1])

def p_data_type(p):
    '''data_type : NUM
                 | STR
                 | FLAG
                 | LIST
                 | TUP
                 | VOID'''
    p[0] = ('data_type', p[1])

def p_empty(p):
    '''empty :'''
    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# Build the parser
# !pip install ply
import ply.yacc as yacc
parser = yacc.yacc()

# Test the parser
input_string = '''
define num main() {
    yield 0;
}
'''
result = parser.parse(input_string)
print(result)