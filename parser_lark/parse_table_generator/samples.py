from parsing.grammar import *

def get_sample_1():
    return Grammar([
        NonTerminal('start', [
            "program"
        ]),
        NonTerminal('program', [
            "DEFINE NUM MAIN OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_BRACES statements YIELD NUM_LITERAL END_OF_LINE CLOSE_BRACES",
            "DEFINE function_type IDENTIFIER OPEN_PARENTHESIS parameter_list CLOSE_PARENTHESIS function_block program"
        ]),
#-------------------------------------------------------
        NonTerminal('function_block', [
            "OPEN_BRACES statements YIELD return_value END_OF_LINE CLOSE_BRACES"
        ]),
        NonTerminal('function_type', [
            "NUM", "STR", "FLAG", "VOID"
        ]),
        NonTerminal('parameter_list', [
            "parameter parameters", "epsilon"
        ]),
        NonTerminal('return_value', [
            "NUM_LITERAL", "string", "YAY", "NAY", "epsilon"
        ]),
        NonTerminal('parameters', [
            "ELEMENT_SEPERATOR parameter parameters", "epsilon"
        ]),
        NonTerminal('parameter', [
            "compound_data_type IDENTIFIER", "basic_data_type IDENTIFIER choose_array"
        ]),
        NonTerminal('choose_array', [
            "OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET", "epsilon"
        ]),
        NonTerminal('statements', [
            "statement statements", "epsilon"
        ]),
        NonTerminal('equal_to', [
            "EQUAL_TO post_equal_to", "epsilon"
        ]),
        NonTerminal('post_equal_to', [
            "ENTER OPEN_PARENTHESIS string CLOSE_PARENTHESIS",
            "IDENTIFIER OPEN_BRACKET NUM_LITERAL SLICING_COLON NUM_LITERAL CLOSE_BRACKET",
            "LENGTH OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS",
            "IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET",
            "HEAD OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS",
            "ISEMPTY OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS",
            "function_call","let_in_statement", "expression"
        ]),
        NonTerminal('data_type', [
            "basic_data_type", "compound_data_type", "epsilon"
        ]),
        NonTerminal('num_str_flag', [
            "NUM", "STR", "FLAG"
        ]),
        NonTerminal('basic_data_type', [
            "fix_let num_str_flag"
        ]),
        NonTerminal('fix_let', [
            "FIX", "LET","epsilon"
        ]),
        NonTerminal('compound_data_type', [
            "LIST", "TUP"
        ]),
#-------------------------------------------------
        NonTerminal('string', [
            "TILDE STRING_LITERAL TILDE"
        ]),
        NonTerminal('array', [
            "basic_data_type IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET"
        ]),

#--------------------------------------------------------------------------------

        NonTerminal('variable_declaration', [
            "basic_data_type IDENTIFIER equal_to",
                    "compound_array compound_var"
        ]),
        NonTerminal('compound_array', [
            "compound_data_type IDENTIFIER",
                    "array"
        ]),
        NonTerminal('compound_var', [
            "EQUAL_TO list_append_tail",
                    "epsilon"
        ]),
        NonTerminal('list_append_tail', [
            "OPEN_BRACKET expression expressions CLOSE_BRACKET"
                        ,"TAIL OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS"
                        ,"APPEND OPEN_PARENTHESIS expression ELEMENT_SEPARATOR IDENTIFIER CLOSE_PARENTHESIS"
        ]),
        NonTerminal('assignment_statement', [
            "IDENTIFIER assignment_operators post_equal_to"
        ]),
        NonTerminal('show_statement', [
            "SHOW OPEN_PARENTHESIS expression expressions CLOSE_PARENTHESIS"
        ]),
        NonTerminal('block', [
            "OPEN_BRACES statements CLOSE_BRACES"
        ]),
        NonTerminal('value_change_array', [
            "IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET assignment_operators expression"
        ]),
#---------------------------------------
        NonTerminal('expressions', [
            " ELEMENT_SEPERATOR expression expressions"
                , "epsilon"
        ]),
        NonTerminal('expression', [
            "term terms" , "epsilon"
        ]),
        NonTerminal('terms', [
            "binary_operators term terms" 
                ,   "epsilon"
        ]),
#---------------------------------------
        NonTerminal('term', [
            "IDENTIFIER"
            ,"NUM_LITERAL"
            ,"string"
            ,"YAY"
            ,   "NAY"
            ,   "OPEN_PARENTHESIS expression CLOSE_PARENTHESIS"
            ,   "unary_operators IDENTIFIER"
            ,   "IDENTIFIER UNARY_OPERATOR"
            ,   "IDENTIFIER OPEN_BRACKET expression CLOSE_BRACKET"
        ]),
#-----------------------------------------------------------------------
        NonTerminal('binary_operators', [
            "BINARY_OPERATOR","COMPARISON_OPERATOR","BINARY_LOGICAL_OPERATOR"
        ]),
        NonTerminal('unary_operators',[
            "UNARY_OPERATOR", "UNARY_LOGICAL_OPERATOR"
        ]),
        NonTerminal('assignment_operators',[
            "EQUAL_TO", "ASSIGNMENT_OPERATOR"
        ]),
#-----------------------------------------------------
        NonTerminal('conditional_block',[
            "yield_block", "block"
        ]),
        NonTerminal('conditional_statement',[
            "GIVEN OPEN_PARENTHESIS expression CLOSE_PARENTHESIS conditional_block other_block otherwise_block"
        ]),
        NonTerminal('other_block',[
            "OTHER OPEN_PARENTHESIS expression CLOSE_PARENTHESIS conditional_block other_block","epsilon"
        ]),
        NonTerminal('otherwise_block',[
            "OTHERWISE conditional_block","epsilon"
        ]),
        NonTerminal('skip_stop',[
            "SKIP","STOP"
        ]),
#---------------------------------------------------------------
        NonTerminal('loop_statement',[
            "ITER OPEN_PARENTHESIS statement expression END_OF_LINE expression CLOSE_PARENTHESIS block",
            "WHILE OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block",
            "REPEAT block WHILE OPEN_PARENTHESIS expression CLOSE_PARENTHESIS END_OF_LINE"
        ]),
#-------------------------------------------------------------------
        NonTerminal('pop_statement',[
            "POP OPEN_PARENTHESIS string CLOSE_PARENTHESIS"
        ]),
        NonTerminal('try_catch_statement',[
            "TEST block ARREST OPEN_PARENTHESIS string CLOSE_PARENTHESIS block"
        ]),
        NonTerminal('yield_block', [
            "OPEN_BRACES statements YIELD expression END_OF_LINE CLOSE_BRACES"
        ]),
#-------------------------------------------------------------------
        NonTerminal('function_call',[
            "IDENTIFIER OPEN_PARENTHESIS argument_list CLOSE_PARENTHESIS"
        ]),
        NonTerminal('argument_list',[
            "expression expressions"
        ]),
#----------------------------------------------------------------------
        NonTerminal('let_in_braces',[
            "let_in CLOSE_BRACES"
        ]),
        NonTerminal('let_in',[
            "let_in_statement" , "expression"
        ]),
        NonTerminal('let_in_statement',[
            "LET data_type IDENTIFIER EQUAL_TO OPEN_BRACES let_in_braces"
            ,"LET data_type IDENTIFIER EQUAL_TO term IN OPEN_BRACES let_in_braces"
            ,"LET data_type IDENTIFIER EQUAL_TO term IN let_in"
        ]),

#---------------------------------------------------------
        NonTerminal('statement',[
            "block",
            "variable_declaration END_OF_LINE",
            "assignment_statement END_OF_LINE",
            "show_statement END_OF_LINE",
            "conditional_statement",
            "loop_statement",
            "skip_stop END_OF_LINE",
            "value_change_array END_OF_LINE",
            "pop_statement END_OF_LINE",
            "try_catch_statement",
            "function_call END_OF_LINE",
            "unary_operators IDENTIFIER END_OF_LINE",
            "IDENTIFIER UNARY_OPERATOR END_OF_LINE"
        ]),
#---------------------------------------------------------------
        NonTerminal('epsilon',['']),
        NonTerminal('NUM',[
            "'NUM'"
        ]),
        NonTerminal('STR',[
            "'STR'"
        ]),
        NonTerminal('FLAG',[
            "'FLAG'"
        ]),
        NonTerminal('FIX',[
            "'FIX'"
        ]),
        NonTerminal('SHOW',[
            "'SHOW'"
        ]),
        NonTerminal('ITER',[
            "'ITER'"
        ]),
        NonTerminal('LIST',[
            "'LIST'"
        ]),
        NonTerminal('TUP',[
            "'TUP'"
        ]),
        NonTerminal('ENTER',[
            "'ENTER'"
        ]),
        NonTerminal('YIELD',[
            "'YIELD'"
        ]),
        NonTerminal('LET',[
            "'LET'"
        ]),
        NonTerminal('IN',[
            "'IN'"
        ]),
        NonTerminal('VOID',[
            "'VOID'"
        ]),
        NonTerminal('WHILE',[
            "'WHILE'"
        ]),
        NonTerminal('REPEAT',[
            "'REPEAT'"
        ]),
        NonTerminal('GIVEN',[
            "'GIVEN'"
        ]),
        NonTerminal('OTHER',[
            "'OTHER'"
        ]),
        NonTerminal('OTHERWISE',[
            "'OTHERWISE'"
        ]),
        NonTerminal('DEFINE',[
            "'DEFINE'"
        ]),
        NonTerminal('TEST',[
            "'TEST'"
        ]),
        NonTerminal('POP',[
            "'POP'"
        ]),
        NonTerminal('ARREST',[
            "'ARREST'"
        ]),
        NonTerminal('LENGTH',[
            "'LENGTH'"
        ]),
        NonTerminal('HEAD',[
            "'HEAD'"
        ]),
        NonTerminal('TAIL',[
            "'TAIL'"
        ]),
        NonTerminal('ISEMPTY',[
            "'ISEMPTY'"
        ]),
        NonTerminal('APPEND',[
            "'APPEND'"
        ]),
        NonTerminal('SKIP',[
            "'SKIP'"
        ]),
        NonTerminal('STOP',[
            "'STOP'"
        ]),
        NonTerminal('YAY',[
            "'YAY'"
        ]),
        NonTerminal('NAY',[
            "'NAY'"
        ]),
        NonTerminal('MAIN',[
            "'MAIN'"
        ]),
        NonTerminal('IDENTIFIER',[
            "'IDENTIFIER'"
        ]),
        NonTerminal('OPEN_PARENTHESIS',[
            "'OPEN_PARENTHESIS'"
        ]),
        NonTerminal('CLOSE_PARENTHESIS',[
            "'CLOSE_PARENTHESIS'"
        ]),
        NonTerminal('OPEN_BRACES',[
            "'OPEN_BRACES'"
        ]),
        NonTerminal('CLOSE_BRACES',[
            "'CLOSE_BRACES'"
        ]),
        NonTerminal('OPEN_BRACKET',[
            "'OPEN_BRACKET'"
        ]),
        NonTerminal('CLOSE_BRACKET',[
            "'CLOSE_BRACKET'"
        ]),
        NonTerminal('NUM_LITERAL',[
            "'NUM_LITERAL'"
        ]),

        NonTerminal('STRING_LITERAL', [
            " 'STRING_LITERAL' "
        ]),
        NonTerminal('END_OF_LINE', [
            " 'END_OF_LINE' "
        ]),
        NonTerminal('SLICING_COLON', [
            " 'SLICING_COLON' "
        ]),
        NonTerminal('ELEMENT_SEPERATOR', [
            " 'ELEMENT_SEPERATOR' "
        ]),
        NonTerminal('COMPARISON_OPERATOR', [
            " 'COMPARISON_OPERATOR' "
        ]),
        NonTerminal('ASSIGNMENT_OPERATOR', [
            " 'ASSIGNMENT_OPERATOR' "
        ]),
        NonTerminal('UNARY_OPERATOR', [
            " 'UNARY_OPERATOR' "
        ]),
        NonTerminal('BINARY_OPERATOR', [
            " 'BINARY_OPERATOR' "
        ]),
        NonTerminal('BINARY_LOGICAL_OPERATOR', [
            " 'BINARY_LOGICAL_OPERATOR' "
        ]),
        NonTerminal('UNARY_LOGICAL_OPERATOR', [
            " 'UNARY_LOGICAL_OPERATOR' "
        ]),
        NonTerminal('TILDE', [
            " 'TILDE' "
        ]),
        NonTerminal('EQUAL_TO', [
            " 'EQUAL_TO' "
        ])
    ])
