# Lexer
The lexical analyzer plays a crucial role in processing the source code of a program. It identifies and categorizes tokens, such as keywords and identifiers, and stores them in a symbol table for reference. Additionally, it eliminates white spaces and comments to streamline the code. The analyzer helps in associating error messages with specific locations in the source code, aiding in debugging. It can also expand macros found in the source program and reads input characters to facilitate further processing during the compilation or interpretation of the program. Essentially, the lexical analyzer ensures the effective understanding and preparation of the program for subsequent stages of compilation or execution.
## Running Instructions
1. Download the 'lexer' folder and open it on terminal.
2. Run the command ```$python3 tokens.py <.geko file>``` on terminal to get the output (tokenised form of the code) on the terminal.
## List of All Regular Languages

 <span style="white-space: nowrap;">
  
|Class|Description|RegEx|Comment on RegEx|
| :-: | :-: | :-: | :-: |
|NUM|Represents the 'num' keyword.|`\bnum\b`|Matches the exact word 'num' as a whole word.|
|STR|Represents the 'str' keyword.|`\bstr\b`|Matches the exact word 'str' as a whole word.|
|FLAG|Represents the 'flag' keyword.|`\bflag\b`|Matches the exact word 'flag' as a whole word.|
|FIX|Represents the 'fix' keyword.|`\bfix\b`|Matches the exact word 'fix' as a whole word.|
|SHOW|Represents the 'show' keyword.|`\bshow\b`|Matches the exact word 'show' as a whole word.|
|ITER|Represents the 'iter' keyword.|`\biter\b`|Matches the exact word 'iter' as a whole word.|
|LIST|Represents the 'list' keyword.|`\blist\b`|Matches the exact word 'list' as a whole word.|
|TUP|Represents the 'tup' keyword.|`\btup\b`|Matches the exact word 'tup' as a whole word.|
|ENTER|Represents the 'enter' keyword.|`\benter\b`|Matches the exact word 'enter' as a whole word.|
|YIELD|Represents the 'yield' keyword.|`\byield\b`|Matches the exact word 'yield' as a whole word.|
|LET|Represents the 'let' keyword.|`\blet\b`|Matches the exact word 'let' as a whole word.|
|IN|Represents the 'in' keyword.|`\bin\b`|Matches the exact word 'in' as a whole word.|
|VOID|Represents the 'void' keyword.|`\bvoid\b`|Matches the exact word 'void' as a whole word.|
|WHILE|Represents the 'while' keyword.|`\bwhile\b`|Matches the exact word 'while' as a whole word.|
|REPEAT|Represents the 'repeat' keyword.|`\brepeat\b`|Matches the exact word 'repeat' as a whole word.|
|GIVEN|Represents the 'given' keyword.|`\bgiven\b`|Matches the exact word 'given' as a whole word.|
|OTHER|Represents the 'other' keyword.|`\bother\b`|Matches the exact word 'other' as a whole word.|
|OTHERWISE|Represents the 'otherwise' keyword.|`\botherwise\b`|Matches the exact word 'otherwise' as a whole word.|
|DEFINE|Represents the 'define' keyword.|`\bdefine\b`|Matches the exact word 'define' as a whole word.|
|TEST|Represents the 'test' keyword.|`\btest\b`|Matches the exact word 'test' as a whole word.|
|POP|Represents the 'pop' keyword.|`\bpop\b`|Matches the exact word 'pop' as a whole word.|
|ARREST|Represents the 'arrest' keyword.|`\barrest\b`|Matches the exact word 'arrest' as a whole word.|
|LENGTH|Represents the 'length' keyword.|`\blength\b`|Matches the exact word 'length' as a whole word.|
|HEAD|Represents the 'head' keyword.|`\bhead\b`|Matches the exact word 'head' as a whole word.|
|TAIL|Represents the 'tail' keyword.|`\btail\b`|Matches the exact word 'tail' as a whole word.|
|ISEMPTY|Represents the 'isEmpty' keyword.|`\bisEmpty\b`|Matches the exact word 'isEmpty' as a whole word.|
|APPEND|Represents the 'append' keyword.|`\bappend\b`|Matches the exact word 'append' as a whole word.|
|SKIP|Represents the 'skip' keyword.|`\bskip\b`|Matches the exact word 'skip' as a whole word.|
|STOP|Represents the 'stop' keyword.|`\bstop\b`|Matches the exact word 'stop' as a whole word.|
|YAY|Represents the 'yay' keyword.|`\byay\b`|Matches the exact word 'yay' as a whole word.|
|NAY|Represents the 'nay' keyword.|`\bnay\b`|Matches the exact word 'nay' as a whole word.|
|MAIN|Represents the 'main' keyword.|`\bmain\b`|Matches the exact word 'main' as a whole word.|
|IDENTIFIER|Represents names given to variables, functions, etc.|`[a-zA-Z_][a-zA-Z0-9_]*`  |Allows for alphanumeric characters and underscores, but does not allow numbers as the first character.|
|OPEN_PARENTHESIS|Represents the open parenthesis character '('.|`\(`|Matches the open parenthesis character '('.|
|CLOSE_PARENTHESIS|Represents the close parenthesis character ')'.|`\(`|Matches the close parenthesis character ')'.|
|OPEN_BRACES|Represents the open braces character '{'.|`\{`|Matches the open braces character '{'.|
|CLOSE_BRACES|Represents the close braces character '}'.|`\}`|Matches the close braces character '}'.|
|OPEN_BRACKET|Represents the open bracket character '['.|`\[`|Matches the open bracket character '['.|
|CLOSE_BRACKET|Represents the close bracket character ']'.|`\]`|Matches the close bracket character ']'.|
|NUM_LITERAL|Represents a numeric literal.|`-?\b\d+\b`|Matches sequences of digits, allowing for negative numbers with optional '-' sign.|
|COMMENT|Represents a comment.|`##.*`|Matches any sequence of characters following '##' until the end of the line.|
|STRING_LITERAL|Represents a string literal.|` ~(?:[^~\\]\|\\.)*~ `|Matches strings enclosed within tilde '~' characters while allowing for escaped characters.|
|END_OF_LINE|Represents the end of line character ';'.|`;`|Matches the end of line character ';'.|
|SLICING_COLON|Represents the slicing colon character ':'.|`:`|Matches the slicing colon character ':'.|
|ELEMENT_SEPERATOR|Represents the element separator character ','.|`,`|Matches the ',' character used to separate elements in a list or tuple.|
|COMPARISON_OPERATOR|Represents comparison operators such as equal to, not equal to, less than or equal to, greater than or equal to, greater than, and less than.|`== \| != \| <= \| >= \| > \| <`|Matches comparison operators used to compare values in expressions.|
|ASSIGNMENT_OPERATOR|Represents assignment operators used to assign values to variables, including conventional assignment, division-assignment, multiplication-assignment, addition-assignment, subtraction-assignment, and modulo-assignment.|`= \| /= \| \*= \| \+= \| -= \| %=`|Matches various assignment operators used to assign values to variables.|
|UNARY_OPERATOR|Represents unary operators that operate on a single operand, such as increment, decrement, and logical negation.|``` \+\+ \| -- \| \` ```|Matches unary operators used to perform operations on a single operand.|
|BINARY_OPERATOR|Represents binary operators used to perform arithmetic and logical operations on two operands, including exponentiation, division, multiplication, addition, subtraction, and modulo.|`\*\* \| / \| \* \| \+ \| - \| %`|Matches binary operators used to perform operations on two operands.|
|LOGICAL_OPERATOR|Represents logical operators used to perform logical operations on boolean values, including AND, OR, NOT, XOR, and bitwise operators.|`&& \| \|\| \| & \| \| \| ! \| \^ `|Matches logical operators used to combine or negate boolean values.|


</span>
