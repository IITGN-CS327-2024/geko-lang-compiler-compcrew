# Lexer
The lexical analyzer plays a crucial role in processing the source code of a program. It identifies and categorizes tokens, such as keywords and identifiers, and stores them in a symbol table for reference. Additionally, it eliminates white spaces and comments to streamline the code. The analyzer helps in associating error messages with specific locations in the source code, aiding in debugging. It can also expand macros found in the source program and reads input characters to facilitate further processing during the compilation or interpretation of the program. Essentially, the lexical analyzer ensures the effective understanding and preparation of the program for subsequent stages of compilation or execution.

|Class|Description|RegEx|Comment on RegEx|
| :-: | :-: | :-: | :-: |
|KEYWORD|This class stores reserved words in a programming language that have predefined meanings in the programming language.|num \| str \| flag \| fix \| show \| iter \| list \| tup \| enter \| yield \| let \| in \| void \| while \| repeat \| given \| other \| otherwise \| define \| test \| pop \| arrest \| main \| length \| head \| tail \| isEmpty \| append \| skip \| stop \| yay \| nay|-|
|MAIN|This token class stores the entry point of a program. Cannot be defined differently. Has to be preceded by keyword num.|main|-|
|IDENTIFIER|This class stores names given to variables, functions, etc.|[a-zA-Z_][a-zA-Z0-9_]*||
|PARENTHESIS|Used to demarcate scope, and define lists, arrays, and tuples.|[\[\]{}()]|-|
|NUM_LITERAL|Defined as any number in between -1023 and +1024 (tentative).|-?\b\d+\b|Also takes into account negative numbers with “-?”. “\d+” matches one or more digits.|
|COMMENT|A comment in our language, Geko, is defined by two simultaneous octothorpe (hashtag) symbols consecutively. This consists of a single line comment. Multi-line comments are not defined for Geko.|##.*|Checks for two ## at the beginning. Anything after these two symbols, until end-of-line character,  is considered as a comment and discarded by the compiler.|
|STRING_LITERAL||||
|SEPARATOR||||
|COMPARISON_OPERATOR||||
|ASSIGNMENT_OPERATOR||||
|UNARY_OPERATOR||||
|BINARY_OPERATOR||||
|LOGICAL_OPERATOR||||
