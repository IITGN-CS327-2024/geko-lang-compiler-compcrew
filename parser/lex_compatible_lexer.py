import re

class MyLexer:
    def __init__(self):
        # Define token patterns using regular expressions
        self.patterns = [
            ('NUM', r'\bnum\b'),
            ('STR', r'\bstr\b'),
            ('FLAG', r'\bflag\b'),
            # Add more token definitions as needed
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
