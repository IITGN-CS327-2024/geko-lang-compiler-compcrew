%{
from geko_lexer import lexer
%}

%token <STRING> STRING_LITERAL
%token <INTEGER> NUM_LITERAL
%token <IDENTIFIER> IDENTIFIER
%token DEFINE NUM MAIN OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_BRACES END_OF_LINE CLOSE_BRACES
%token YIELD

%%

program : function_definitions DEFINE NUM MAIN OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_BRACES statements YIELD NUM_LITERAL END_OF_LINE CLOSE_BRACES
        ;

function_definitions : function_definition function_definitions
                      | /* empty */
                      ;

function_definition : DEFINE function_type IDENTIFIER OPEN_PARENTHESIS parameter_list CLOSE_PARENTHESIS function_block
                    ;

function_block : OPEN_BRACES statements YIELD return_value CLOSE_BRACES
               ;

return_value : NUM_LITERAL
             | STRING_LITERAL
             | /* empty */
             ;

function_type : NUM
              | STR
              | FLAG
              | VOID
              ;

parameter_list : parameter_list ELEMENT_SEPERATOR parameter
               | parameter
               | /* empty */
               ;

parameter : data_type IDENTIFIER
          | array
          ;

array : data_type IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET
      ;

statements : statement statements
           | /* empty */
           ;

statement : variable_declaration END_OF_LINE
          | assignment_statement END_OF_LINE
          | block
          | show_statement END_OF_LINE
          | conditional_statement
          | loop_statement
          | return_statement END_OF_LINE
          | try_catch_statement
          | function_call END_OF_LINE
          | enter_statement END_OF_LINE
          | /* empty */
          ;

variable_declaration : data_type IDENTIFIER ASSIGNMENT_OPERATOR expression
                      | data_type IDENTIFIER
                      ;

assignment_statement : IDENTIFIER ASSIGNMENT_OPERATOR expression
                     ;

show_statement : SHOW OPEN_PARENTHESIS expression expression_list CLOSE_PARENTHESIS
               ;

expression_list : ELEMENT_SEPERATOR expression expression_list
                 | /* empty */
                 ;

conditional_statement : GIVEN OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block
                       (OTHER OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block)*
                       (OTHERWISE block | /* empty */)
                       ;

loop_statement : ITER OPEN_PARENTHESIS expression END_OF_LINE expression END_OF_LINE expression CLOSE_PARENTHESIS block
               | WHILE OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block
               | REPEAT block WHILE OPEN_PARENTHESIS expression CLOSE_PARENTHESIS END_OF_LINE
               ;

return_statement : YIELD expression
                 ;

try_catch_statement : TEST block POP STRING_LITERAL ARREST OPEN_PARENTHESIS STRING_LITERAL CLOSE_PARENTHESIS block
                    ;

function_call : IDENTIFIER OPEN_PARENTHESIS argument_list CLOSE_PARENTHESIS
              ;

argument_list : expression expression_list
              | /* empty */
              ;

enter_statement : data_type IDENTIFIER ASSIGNMENT_OPERATOR ENTER OPEN_PARENTHESIS STRING_LITERAL CLOSE_PARENTHESIS
                ;

expression : term ((BINARY_OPERATOR | COMPARISON_OPERATOR) term)*
           ;

term : factor ((BINARY_OPERATOR | COMPARISON_OPERATOR) factor)*
     ;

factor : IDENTIFIER
       | NUM_LITERAL
       | STRING_LITERAL
       | BOOLEAN
       | OPEN_PARENTHESIS expression CLOSE_PARENTHESIS
       | UNARY_OPERATOR expression
       ;

string : TILDE STRING_LITERAL TILDE
       | /* empty */
       ;

data_type : FIX data_type
          | STR
          | FLAG
          | LIST
          | TUP
          | VOID
          | /* empty */
          ;
