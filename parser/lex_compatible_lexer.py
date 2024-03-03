import re

class MyLexer:
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
            #matches strings enclosed within tilde (~) characters while allowing for the presence of escaped tildes and other characters
            #[^~\\] matches any character that is not a tilde (~) or a backslash (\)
            #\\. matches an escaped character (any character preceded by a backslash)

            # ('SEPARATOR', r';|:|,'),
            ('END_OF_LINE', r';'),
            ('SLICING_COLON', r':'),
            ('ELEMENT_SEPERATOR', r','),

            ('COMPARISON_OPERATOR', r'==|!=|<=|>=|>|<'),
            ('ASSIGNMENT_OPERATOR', r'=|/=|\*=|\+=|-=|%='),
            # due to precedence, assignment operator is kept above unary/binary (*,/,+,- versus *=, /=, += and -=), but below comparison (== versus =)
            ('UNARY_OPERATOR' , r'\+\+|--|`'),
            ('BINARY_OPERATOR', r'\*\*|/|\*|\+|-|%'),
            ('LOGICAL_OPERATOR', r'&&|\|\||&|\||!|\^')
        ]
        # Combine patterns into a single regular expression
        self.pattern = '|'.join('(?P<%s>%s)' % pair for pair in self.patterns)
        self.token_regexes = {name: re.compile(regex) for name, regex in self.patterns}

    def tokenize(self, code):
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
        return tokens

# Test the modified lexer with some input
example_code = '''
num main() {
    num x = 5;
    str message = "Hello, World!";
}
'''
lexer = MyLexer()
tokens = lexer.tokenize(example_code)
for token in tokens:
    print(token)