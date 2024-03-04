import re
import sys
# imported Regular Expressions(re) module

# Define token patterns using regular expressions
patterns = [
    # ('KEYWORD', r'\bnum\b|\bstr\b|\bflag\b|\bfix\b|\bshow\b|\biter\b|\blist\b|\btup\b|\benter\b|\byield\b|\blet\b|\bin\b|\bvoid\b|\bwhile\b|\brepeat\b|\bgiven\b|\bother\b|\botherwise\b|\bdefine\b|\btest\b|\bpop\b|\barrest\b|\bmain\b|\blength\b|\bhead\b|\btail\b|\bisEmpty\b|\bappend\b|\bskip\b|\bstop\b|\byay\b|\bnay\b'),
    #KEYWORD token class contains union of all keywords in Geko language
    #r signifies  raw string.It treats \ as literal character
    #here '\bnum\b' matches the exact word 'num' as a whole word not as part of a longer word
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
    # main token, kept separate for ease.

    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    # This is the concatenation of two expressions [a-zA-Z_] and [a-zA-Z0-9_]*.
    # [...] denotes a character set.
    # a-z : Denotes all lowercase letters
    # A-Z: Denotes all uppercase letters
    # _: Denotes an underscore
    # 0-9: Denotes digits from 0-9
    # [a-zA-Z_] matches any lowercase letter, uppercase letter or an underscore as a starting letter of the identifier.
    # [a-zA-Z0-9_]* matches any lowercase letter, uppercase letter,digit or  underscores

    # ('PARENTHESIS', r'[\[\]{}()]'),
    ('OPEN_PARENTHESIS', r'\('),
    ('CLOSE_PARENTHESIS', r'\)'),
    ('OPEN_BRACES', r'\{'),
    ('CLOSE_BRACES', r'\}'),
    ('OPEN_BRACKET', r'\['),
    ('CLOSE_BRACKET', r'\]'),
    #[\[\]{}()] denotes a character set. \[ and \[ ensures that ] and [ are treated as a literal character

    ('NUM_LITERAL', r'-?\b\d+\b'),
    #'-?' states zero or one occurence of -(negation). \d+ matches sequences of digits in a string

    ('COMMENT', r'##.*'),
    #.* matches any sequence of characters until the end of the line

    ('STRING_LITERAL', r'~(?:[^~\\]|\\.)*~'),
    ('TILDE', r'~'),
    #matches strings enclosed within tilde (~) characters while allowing for the presence of escaped tildes and other characters
    #[^~\\] matches any character that is not a tilde (~) or a backslash (\)
    #\\. matches an escaped character (any character preceded by a backslash)

    # ('SEPARATOR', r';|:|,'),
    ('END_OF_LINE', r';'),
    ('SLICING_COLON', r':'),
    ('ELEMENT_SEPERATOR', r','),

    ('COMPARISON_OPERATOR', r'==|!=|<=|>=|>|<'),
    ('EQUAL_TO', r'='),
    ('ASSIGNMENT_OPERATOR', r'/=|\*=|\+=|-=|%='),
    # due to precedence, assignment operator is kept above unary/binary (*,/,+,- versus *=, /=, += and -=), but below comparison (== versus =)
    ('UNARY_OPERATOR' , r'\+\+|--|`'),
    ('BINARY_OPERATOR', r'\*\*|/|\*|\+|-|%'),
    ('BINARY_LOGICAL_OPERATOR', r'&&|\|\||&|\||\^'),
    ('UNARY_LOGICAL_OPERATOR', r'!')
]
# Combine patterns into a single regular expression through join()
pattern = '|'.join('(?P<%s>%s)' % pair for pair in patterns)
#?P used for named capturing groups which allows to extract specific part of matched text
#%s placeholders are replaced with the actual values from the tuple.
# The entire statement combines all the individual regular expression patterns from the patterns list into a single regular expression.
# The resulting pattern will be used to match tokens in the input code.

stringVal = ''
# Tokenize input source code
def lexer(code):
    # Empty list to store tokens
    tokens = []

    # Loop over matches found in the code using the specified pattern
    for match in re.finditer(pattern, code):
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
        elif kind == 'COMMENT':
            # Ignore comments
            pass
        else:
            # For other token types, simply add the kind and value to the tokens list
            tokens.append((kind, value))

    # Return the list of tokens
    return tokens

# def read_geko_file(file_path):
#     with open(file_path, 'r') as file:
#         return file.read()

# file_path = r'C:/Users/Darshi Doshi/Desktop/Geko Lang/testcase1.geko'  # Replace the string with the actual path to  .geko file
# geko_code = read_geko_file(file_path)
# def read_geko_file(file_path):
#     with open(file_path, 'r') as file:
#         return file.read()

# if len(sys.argv) != 2:
#     print("Usage: python3 lexer.py <geko_file>")
#     sys.exit(1)

# file_path = sys.argv[1]
# geko_code = read_geko_file(file_path)

# tokens = lexer(geko_code)

example_code = '''
num main() {
    ## num x = 5;
    ## num y = 8;
    ## y = x + 5;
    x+=9;
    flag oneEx = yay;
    fix flag twoEx = nay;
    num testVar = 0;
    ##num tVar = 4;
    ##num tVarTwo;
    ##let tVar = 5 in tVarTwo = tVar**2;
    y +=++x++--;
    show(~mwoe mowe meow \~ heeh \~ \\ eememem ~)
    ##given(oneEx || twoEx){show(~oror_op.~);}
    ##given(oneEx && twoEx){show(~andand_op~);}
    ##given(oneEx  twoEx){show(~andand_op~);}
    ##given(oneEx && twoEx){show(~andand_op~);}
    ##given(++y >= x){show(~negate_op~);}
    ##given(oneEx < twoEx){show(~less_op~);}
    ##given(oneEx <= twoEx){show(~lesseq_op~);}
    ##testVar += y1;
    ##testVar -= y2;
    ##testVar *= y3;
    ##testVar /= y4;
    ##testVar %= y5;
    show(~ me \~ me ~)
    yield 0;

'''

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

# Call the function to print the table
# print_table(tokens)
