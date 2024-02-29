import re

class GekoLexer:
    def __init__(self):
        # Define token patterns using regular expressions
        self.patterns = [
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
            ('END_OF_LINE', r';'),
            ('SLICING_COLON', r':'),
            ('ELEMENT_SEPERATOR', r','),
            ('COMPARISON_OPERATOR', r'==|!=|<=|>=|>|<'),
            ('ASSIGNMENT_OPERATOR', r'=|/=|\*=|\+=|-=|%='),
            ('UNARY_OPERATOR' , r'\+\+|--|`'),
            ('BINARY_OPERATOR', r'\*\*|/|\*|\+|-|%'),
            ('LOGICAL_OPERATOR', r'&&|\|\||&|\||!|\^')
        ]
        # Combine patterns into a single regular expression through join()
        self.pattern = '|'.join('(?P<%s>%s)' % pair for pair in self.patterns)

    # Tokenize input source code
    def lexer(self, code):
        # Empty list to store tokens
        tokens = []

        # Loop over matches found in the code using the specified pattern
        for match in re.finditer(self.pattern, code):
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
        return tokens

