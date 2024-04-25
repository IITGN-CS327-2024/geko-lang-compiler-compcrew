from lark import Lark
from lark.lexer import Lexer, Token
from lark.exceptions import UnexpectedToken
import ast_lexer_lark as lexer_lark
import sys
import os
import re
# ----------------------------------------------------------------------------------------------------------------------------
import lark
from lark import Visitor, Tree, Token
import pydot
from IPython.display import display
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
from typing import *
import rich
# ----------------------------------------------------------------------------------------------------------------------------
from ast_classes import *
# ----------------------------------------------------------------------------------------------------------------------------
# AST node classes (imported from the previous code)
# Add current directory to the system path
sys.path.append(os.path.abspath('./'))
from ast_grammar import grammar

class ASTBuilder(Visitor):
    def __default__(self, tree):
        children = [self.transform(child) for child in tree.children]
        # print("----------------------------------------------------------")
        # print(f"the tree data from __default__ is: {tree.data}, children are: {children}")
        return self.create_node(tree.data, children)

    def create_node(self, node_type, children):
        # print("----------------------------------------------------------")
        # print(f"node_type from create_node: {node_type}, children: {children}")
        # print("----------------------------------------------------------")
        if node_type == "start":
            # print(f"node_type: {node_type}, value: {children[0]}")
            return children[0]
        
        elif node_type == "program":
            if(len(children) == 1):
                main_function = children[0]
                function_defs = []
                # print(f"node_type:{node_type}, main_function: {main_function}")
                # print("**************************************************************************")
                return (Program(function_defs, main_function))
            else:
                function_defs = [children[0]]
                program = children[1]
                function_defs.extend(program.function_defs)
                main_function = program.main_function
                # print(f"node_type:{node_type}, function_defs: {function_defs}, main_function: {main_function}")
                return Program(function_defs, main_function)
        
        elif node_type == "main_func":
            statements = children[6]
            return MainFunc(statements)
        
        elif node_type == "func_def":
            # print("ye func_def bhi galat hai isko bhi change crow")
            function_type = str(children[1])
            function_name = str(children[2])
            parameters = [children[4][0]]
            parameters.extend(children[4][1]) if len(children[4]) > 1 else None
            function_block = children[6]
            # print(f"node_type:{node_type}, function_type: {function_type}, function_name: {function_name}, parameters: {parameters}, function_block: {function_block}")
            return FunctionDef(function_type, function_name, parameters, function_block)
        
        elif node_type == "function_block":
            statements = children[1]
            return_value = children[3]
            # print(f"node_type:{node_type}, statements: {statements}, return_value: {return_value}")
            return FunctionBlock(statements, return_value)
        
        elif node_type == "function_type":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        
        elif node_type == "parameter_list":
            parameters = children if children else []
            # print(f"node_type:{node_type}, parameters: {parameters}")
            return parameters
        
        elif node_type == "return_value":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return children[0]
        
        elif node_type == "parameters":
            if not children:
                return []
            elif len(children) == 1:
                # print(f"node_type:{node_type}, value: None")
                return []
            parameters = [children[1]]
            parameters.extend(children[2])
            # print(f"node_type:{node_type}, parameters: {parameters}")
            return parameters
        
        elif node_type == "parameter":
            if len(children) == 2:
                data_type = str(children[0])
                parameter_name = str(children[1])
                # print(f"node_type:{node_type}, parameter_name: {parameter_name}")
                return Parameter(data_type, parameter_name, None)
            else:
                data_type = str(children[0])
                parameter_name = str(children[1])
                array_size = children[2] if len(children) > 2 else None
                # print(f"node_type:{node_type}, data_type: {data_type}, parameter_name: {parameter_name}, array_size: {array_size}")
                return Parameter(data_type, parameter_name, array_size)

        elif node_type == "choose_array":
            if not children:
                # print(f"node_type:{node_type}, value: None")
                return None
            elif len(children) == 1:
                # print(f"node_type:{node_type}, value: None")
                return None
            else:
                # print(f"node_type:{node_type}, value: {children[1]}")
                return children[1]
        
        elif node_type == "statements":
            statements = [children[0]]
            if children[0] == None:
                # print(f"node_type:{node_type}, value: {children[0]}")
                return statements
            if children[1]!=None:
                statements.extend(children[1])
            # print(f"node_type:{node_type}, statements: {statements}")
            
            return statements
        
        elif node_type == "equal_to":
            if not children:
                # print(f"node_type:{node_type}, value: []")
                return []
            elif len(children) == 1:
                # print(f"node_type:{node_type}, value: {children[0]}")
                return children[0]
            # print(f"node_type:{node_type}, value: {children}")
            return children[1]

        elif node_type == "post_equal_to":
            if children[0] == "enter":
                string = str(children[2])[len("THIS_IS_A_STRING_SO_THAT_IT_DOES_NOT_CONFLICT_WITH_OTHER_TYPES"):]
                value = EnterStatement(string,None)
            else:
                value = children[0]
            # print(f"node_type:{node_type}, value: {value}")
            return value

        elif node_type == "special_function":
            if len(children) == 1:
                function_call = children[0]
                # print(f"node_type:{node_type}, function_call: {function_call}")
                return SpecialFunction(None, None, None, None, None, None, function_call)
            else:
                if children[0] == "length":
                    identifier = str(children[2])
                    # print(f"node_type:{node_type}, identifier: {identifier}")
                    return SpecialFunction(identifier, None, None, "length", None, None, None)
                elif children[0] == "head":
                    identifier = str(children[2])
                    # print(f"node_type:{node_type}, identifier: {identifier}")
                    return SpecialFunction(identifier, None, None, None, "head", None, None)
                elif children[0] == "isEmpty":
                    identifier = str(children[2])
                    isEmpty = "isEmpty"
                    # print(f"node_type:{node_type}, identifier: {identifier}")
                    return SpecialFunction(identifier, None, None, None, None,isEmpty, None)

                identifier = str(children[0])
                num_literal_start = int(children[2])
                num_literal_end = int(children[4])
                # print(f"node_type:{node_type}, identifier: {identifier}, num_literal_start: {num_literal_start}, num_literal_end: {num_literal_end}")
                return SpecialFunction(identifier, num_literal_start, num_literal_end, None, None, None, None)
        
        elif node_type == "data_type":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0]) if children else None
        
        elif node_type == "num_str_flag":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        
        elif node_type == "basic_data_type":
            fix_let = str(children[0])
            data_type = str(children[-1])
            # print(f"node_type:{node_type}, fix_let: {fix_let}, data_type: {data_type}")
            return f"{fix_let} {data_type}" if fix_let else data_type
        
        elif node_type == "fix_let":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0]) if children else None
        
        elif node_type == "compound_data_type":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        
        elif node_type == "string":
            # print(f"node_type:{node_type}, value: {children[1]}")
            string_value = "THIS_IS_A_STRING_SO_THAT_IT_DOES_NOT_CONFLICT_WITH_OTHER_TYPES" + str(children[1])
            return string_value

        elif node_type == "array":
            data_type = str(children[0])
            identifier = str(children[1])
            size = int(children[3])
            # print(f"node_type:{node_type}, data_type: {data_type}, identifier: {identifier}, size: {size}")
            return Array(data_type, identifier, size)
        
        elif node_type == "variable_declaration":
            if children[0].__class__.__name__ == "Array":
                data_type = children[0].data_type
                variable_name = children[0].identifier
                size_array = children[0].size
                if children[1]: 
                    equal_to = children[1][1]
                else:
                    equal_to = None
            elif children[0].__class__.__name__ == "LIST":
                size_array = None 
                data_type = children[0].data_type
                variable_name = children[0].identifier
                if children[1]:
                    equal_to = children[1][1]
                else:
                    equal_to = None
            elif children[0].__class__.__name__ == "TUP":
                data_type = children[0].data_type
                size_array = None
                variable_name = children[0].identifier
                equal_to = children[1][1] if len(children[1]) > 1 else children
            else:
                data_type = children[0]
                variable_name = str(children[1])
                equal_to = children
                size_array = None
                if len(children) > 2:
                    equal_to = children[2]           
                if equal_to:
                    equal_to = flatten_expression(equal_to)
            return VariableDeclaration(data_type, variable_name, size_array, equal_to)

        elif node_type == "compound_array":
            if len(children) == 1:
                return children[0]
            else:
                data_type = str(children[0])
                identifier = str(children[1])
                if data_type == "list":
                    # print(f"node_type:{node_type}, data_type: {data_type}, identifier: {identifier}")
                    return LIST(data_type, identifier, None)
                else:
                    # print(f"node_type:{node_type}, data_type: {data_type}, identifier: {identifier}")
                    return TUP(data_type, identifier)
        
        elif node_type == "compound_var":
            if len(children) == 1:
                return None
            elif len(children) == 2:
                if children[1].__class__.__name__ == "ListAppendTail":
                    return children
                else:
                    return children[0]
            elif len(children) == 4:
                if children[0] == "EQUAL_TO":
                    return BinaryOperator(children[2], children[1], children[3])
                else:
                    return children
            else:
                return children
        
        elif node_type == "list_append_tail":
            elements = None
            identifier = children
            tail = None
            append = None
            if children[1].__class__.__name__ == "Expression":
                elements =[ children[1] ]
                elements.extend(children[2]) if len(children) > 2 else None
                identifier = None
            elif children[0] == "tail":
                elements = None
                identifier = children[2]
                tail = str(children[0])
            elif children[0] == "append":
                elements = children[2].terms[0]
                identifier = children[4]
                append = str(children[0])
            # print(f"node_type:{node_type}, elements: {elements}, identifier: {identifier}")
            return ListAppendTail(elements, identifier, tail, append)
        
        elif node_type == "assignment_statement":
            variable_name = str(children[0])
            assignment_operators = children[1].operator
            value = children[2]
            # print(f"node_type:{node_type}, variable_name: {variable_name}, assignment_operators: {assignment_operators}, value: {value}")
            return Assignment(variable_name, assignment_operators, value)
        
        elif node_type == "show_statement":
            expressions = children[2]
            if children[3] != "CLOSE_PARENTHESIS":
                i = 3
                expressions = [expressions] 
                while isinstance(children[i],list):
                    expressions.extend(children[i])
                    i+=1
            # print(f"node_type:{node_type}, expressions: {expressions}")
            return ShowStatement(expressions)
        
        elif node_type == "block":
            statements = children[1]
            # print(f"node_type:{node_type}, statements: {statements}")
            return Block(statements)
        
        elif node_type == "value_change_array":
            identifier = str(children[0])
            index = children[2]
            assignment_operators = children[4]
            value = children[5]
            # print(f"node_type:{node_type}, identifier: {identifier}, index: {index}, assignment_operators: {assignment_operators}, value: {value}")
            return ValueChangeArray(identifier, index, assignment_operators, value)
        
        elif node_type == "expressions":
            if not children:
                # print(f"node_type:{node_type}, value: []")
                return []
            expressions = [children[1]] if len(children) > 1 else []
            expressions.extend(children[2]) if len(children) > 2 else None
            # print(f"node_type:{node_type}, expressions: {expressions}")
            return expressions
        
        elif node_type == "expression":
            if len(children) == 1:
                terms = children[0]
                operator_if_exists = None
            elif len(children) == 2:
                terms = [children[0], children[1] if children[1] is not None else None] if children else None
                # operator_if_exists = children if '=' in children else None
                operator_if_exists = None
            # elif len(children) == 3:
            #     terms = None
            #     # operator_if_exists = children if '=' in children else None
            #     operator_if_exists = None
            # else:
            #     terms = None
            #     # operator_if_exists = children if '=' in children else None
            #     operator_if_exists = None
            # print(f"node_type:{node_type}, terms: {terms}")
            return Expression(operator_if_exists, terms)
        
        elif node_type == "terms":
            if not children:
                # print(f"node_type:{node_type}, value: []")
                return []
            operator_if_exists = [children[0]]
            operator_if_exists = children[0]
            terms = children[1:] if len(children) > 1 else None
            # print(f"node_type:{node_type}, operators: {operator_if_exists}, terms: {terms}")
            if terms is None:
                return None
            return Expression(operator_if_exists=operator_if_exists, terms=terms)
        
        elif node_type == "term":
            identifier = None
            if len(children)==1:  
                if children[0].__class__.__name__ == "SpecialFunction":
                    expression = children[0]
                    value = None
                elif str(children[0]).startswith("THIS_IS_A_STRING_SO_THAT_IT_DOES_NOT_CONFLICT_WITH_OTHER_TYPES"):
                    value = str(children[0])[len("THIS_IS_A_STRING_SO_THAT_IT_DOES_NOT_CONFLICT_WITH_OTHER_TYPES"):]
                    identifier = None
                    expression = None
                elif type(children[0]) == int:
                    value = children[0]
                    identifier = None
                    expression = None
                elif type(children[0]) == bool:
                    value = children[0]
                    identifier = None
                    expression = None
                elif children[0].__class__.__name__ == "ListAppendTail":
                    expression = children[0]
                    value = None
                else:
                    value = None
                    identifier = children[0]
                    expression = None
                if children[0].__class__.__name__ == "Token":
                    identifier = children[0].__class__.__name__
                pre_unary_operator = None
                post_unary_operator = None
                
            elif len(children) == 2:
                if children[0].__class__.__name__ == "UnaryOperator":
                    pre_unary_operator = children[0].operator
                    identifier = str(children[1])
                    post_unary_operator = None
                else:
                    post_unary_operator = children[1]
                    identifier = str(children[0])
                    pre_unary_operator = None
                value = None
                expression = None
            elif len(children) == 3:
                pre_unary_operator = None
                post_unary_operator = None
                identifier = None
                expression = children[1]
                value = None
            else:
                pre_unary_operator = None
                post_unary_operator = None
                identifier = str(children[0])
                expression = children[2]
                value = None

            return Term(value, identifier, expression, pre_unary_operator, post_unary_operator)    

        
        elif node_type == "binary_operators":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        
        elif node_type == "unary_operators":
            operator = str(children[0])
            # print(f"node_type:{node_type}, value: {children[0]}")
            return UnaryOperator(operator)
        
        elif node_type == "assignment_operators":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return AssignmentOperator(str(children[0]))
        
        elif node_type == "conditional_block":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return children[0]
        
        elif node_type == "conditional_argument":
            if children[0].__class__.__name__ == "SpecialFunction":
                is_special = children[0]; 
                comparison_operator = str(children[1]) if len(children) > 1 else None
                expression = children[2] if len(children) > 1 else None
            else:
                expression = children[0]
                comparison_operator = None
                is_special = None
            # print(f"node_type:{node_type}, is_special: {is_special}, comparison_operator: {comparison_operator}, expression: {expression}")
            return ConditionalArgument(is_special, comparison_operator, expression)
        
        elif node_type == "conditional_statement":
            conditional_argument = children[2]
            conditional_block = children[4]
            other_blocks = children[5] if len(children) > 5 else []
            otherwise_block = children[6] if len(children) > 6 else None
            # print(f"node_type:{node_type}, conditional_argument: {conditional_argument}, conditional_block: {conditional_block}, other_blocks: {other_blocks}, otherwise_block: {otherwise_block}")
            return ConditionalStatement(conditional_argument, conditional_block, other_blocks, otherwise_block)    

        elif node_type == "other_block":
            if children == [None]:
                # print(f"node_type:{node_type}, value: []")
                return []
            condition = children[2]
            conditional_block = children[4]
            other_blocks = children[5] if len(children) > 5 else []
            # print(f"node_type:{node_type}, condition: {condition}, conditional_block: {conditional_block}, other_blocks: {other_blocks}")
            return [OtherBlock(condition, conditional_block)] + other_blocks
        
        elif node_type == "otherwise_block":
            # print(f"node_type:{node_type}, value: {children[0]}")
            # print(children[1])
            return OtherwiseBlock(children[1]) if children[0] else None
            return OtherwiseBlock(children[1:])
            # TODO FIX - current fix to not have list return in otherwise_block in AST
        
        elif node_type == "update_statement":
            if len(children) > 2:
                return Assignment(children[0], children[1], children[2])
            
            elif children[1] == "++" or children[1] == "--":
                value = str(children[0])
                post_unary_operator = str(children[1])
                pre_unary_operator = None
                # print(f"node_type:{node_type}, pre_unary_operator: {pre_unary_operator}, value: {value}, post_unary_operator: {post_unary_operator}")
                return UnaryStatement(pre_unary_operator, value, post_unary_operator)
            else: 
                value = str(children[1])
                pre_unary_operator = str(children[0])
                post_unary_operator = None
                # print(f"node_type:{node_type}, pre_unary_operator: {pre_unary_operator}, value: {value}, post_unary_operator: {post_unary_operator}")
                return UnaryStatement(pre_unary_operator, value, post_unary_operator)


        

        elif node_type == "loop_statement":
            loop_type = children[0]
            declaration = None
            condition = children[2]
            updation = None
            block = children[4]
            if children[0] == "iter":
                loop_type = "iter"
                declaration = children[2]
                condition = children[3]
                updation = children[5]
                block = children[7]
            elif children[0] == "while":
                loop_type = "while"
                condition = children[2]
                block = children[4]
            elif children[0] == "repeat":
                loop_type = "repeat_while"
                condition = children[-3]
                block = children[1]
            # print(f"node_type:{node_type}, loop_type: {loop_type}, condition: {condition}, block: {block}")
            return LoopStatement(loop_type, declaration,condition, updation, block)
        
        elif node_type == "pop_statement":
            string_value = children[2]
            # print(f"node_type:{node_type}, string_value: {string_value}")
            return PopStatement(string_value)
        
        elif node_type == "try_catch_statement":
            try_block = children[1]
            catch_string = children[4]
            catch_block = children[6]
            # print(f"node_type:{node_type}, try_block: {try_block}, catch_string: {catch_string}, catch_block: {catch_block}")
            return TryCatchStatement(try_block, catch_string, catch_block)
        
        elif node_type == "yield_block":
            statements = children[1]
            expression = children[3]
            # print(f"node_type:{node_type}, statements: {statements}, expression: {expression}")
            return YieldBlock(statements, expression)
        
        elif node_type == "function_call":
            function_name = str(children[0])
            arguments = children[2]
            # print(f"node_type:{node_type}, function_name: {function_name}, arguments: {arguments}")
            return FunctionCall(function_name, arguments)
        
        elif node_type == "argument_list":
            if not children:
                # print(f"node_type:{node_type}, value: []")
                return []
            arguments = [children[0]]
            arguments.extend(children[1])
            # print(f"node_type:{node_type}, arguments: {arguments}")
            return arguments
        
        elif node_type == "let_in_braces":
            let_in = children[0]
            # print(f"node_type:{node_type}, let_in: {let_in}")
            return children
        
        elif node_type == "let_in":
            if isinstance(children[0], LetInStatement):
                # print(f"node_type:{node_type}, value: {children[0]}")
                return children[0]
            else:
                # print(f"node_type:{node_type}, value: {children[0]}")
                return children
        elif node_type == "let_in_statement":
            data_type = children[1]
            variable_name = children[2]
            operation = None
            if children[4] == "OPEN_BRACES":
                value = children[5]
            else:
                value = children[4]
            if len(children) > 6:
                value = children[4]
                if children[6] == "{":
                    operation = children[7]
                else:
                    operation = children[6]
            # print(f"node_type:{node_type}, data_type: {data_type}, variable_name: {variable_name}, value: {value}, operation: {operation}")
            return LetInStatement(data_type=data_type, variable_name=variable_name, value_or_letin=value, operation=operation)

        elif node_type == "statement":
            
            if len(children) == 3:
                # if children[0] == "++" or children[0] == "--" or children[0]=="`" or children[0]=="!":
                if children[0].__class__.__name__ == "UnaryOperator":
                    pre_unary_operator = children[0].operator
                    value = children[1]
                    post_unary_operator = None
                    # print(f"node_type:{node_type}, pre_unary_operator: {pre_unary_operator}, value: {value}, post_unary_operator: {post_unary_operator}")
                    return UnaryStatement(pre_unary_operator, value, post_unary_operator)
                else:
                    pre_unary_operator = None
                    value = children[0]
                    post_unary_operator = children[1]
                    # print(f"node_type:{node_type}, pre_unary_operator: {pre_unary_operator}, value: {value},post_unary_operator: {post_unary_operator}")
                    return UnaryStatement(pre_unary_operator, value, post_unary_operator)
            
            statement_type = children[0].__class__.__name__
            if statement_type == "ConditionalStatement":
                return children[0]
            elif statement_type == "TryCatchStatement":
                return children[0]
            elif statement_type == "LoopStatement":
                return children[0]
            value = children[0]
            if statement_type == "Block":
                return children[0]
            if children[-1] == ";":
                children.pop()
                children = children[0] 
            # print(f"node_type:{node_type}, statement_type: {statement_type}, value: {value}")
            return children
        
        elif node_type == "special_function":
            function_type = children[0].data
            if function_type == "IDENTIFIER":
                if len(children) == 3:
                    arguments = [children[2]]
                else:
                    start = int(children[2].value)
                    end = int(children[4].value)
                    arguments = [start, end]
            else:
                arguments = [str(children[2])] if len(children) > 2 else []
            # print(f"node_type:{node_type}, function_type: {function_type}, arguments: {arguments}")
            return SpecialFunction(function_type, arguments)
        
        elif node_type == "data_type":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0]) if children else None
        
        elif node_type == "num_str_flag":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        
        elif node_type == "basic_data_type":
            fix_let = str(children[0]) if children else None
            data_type = str(children[1])
            # print(f"node_type:{node_type}, fix_let: {fix_let}, data_type: {data_type}")
            return f"{fix_let} {data_type}" if fix_let else data_type
        
        elif node_type == "fix_let":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0]) if children else None
        
        elif node_type == "compound_data_type":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        
        elif node_type == "skip_stop":
            # print(f"node_type:{node_type}, value: {children[0]}")
            return Skip(skip=children[0])

        
        elif node_type == "compound_element":
            # print(f"node_type:{node_type}, value: {children[0]}")
            terms = children if len(children) > 1 else None
            terms.extend(children[3]) if len(children) > 3 else None
            operator_if_exists = children[2] if len(children) > 2 else None
            return Expression(operator_if_exists, terms)

    def transform(self, tree):
        if isinstance(tree, Tree):
            # print("this is the start from a tree node i.e. transform...")
            # print()
            # print("tree.data from transform is:",tree.data)
            # print()
            return self.__default__(tree)
        elif isinstance(tree, Token):
            # print("value from transform is:",tree.value)
            # print()
            if tree.type == 'NUM_LITERAL':
                # Convert the string value of NUM_LITERAL to an integer
                return int(tree.value)
            if tree.type == 'YAY':
                return True
            if tree.type == 'NAY':
                return False

            return tree.value
        else:
            raise ValueError(f"Unexpected input: {tree}")

# ----------------------------------------------------------------------------------------------------------------------------

# def read_geko_file(file_path):
#     with open(file_path, 'r') as file:
#         return file.read()

# --------------------------------------------------------------------------------------------

# USE THIS FUNCTION, THIS WORKS:
def final_iteration(tree_node, tokens,graph, parent_node=None):
    if isinstance(tree_node, lark.Tree):
        for child in tree_node.children:
            final_iteration(child, tokens,graph, parent_node=tree_node)

    else:
        # Handle leaf nodes (tokens)
        if isinstance(tree_node, lark.Token):
            new_token = tokens.pop(0)
            new_node = (new_token[0], new_token[1])
            tree_node.value = new_node[1]

        else:
            print("Unknown leaf node type:", tree_node)
    # return graph

#----------------------------------------------------------------------------------------------------------------------------

# Create the Lark parser
parser = Lark(grammar, start='start', parser = 'lalr')#, lexer = lexer_lark)

code = """
define void caesarEncrypt(list plaintext, num key){
    iter(num i = 0; i < length(plaintext); i++){
        plaintext[i] = (plaintext[i] + key) % 26;
    }
    yield;
}

define void caesarDecrypt(list ciphertext, num key){
    iter (num i=0; i< length(ciphertext); i++){
        ciphertext[i] = (ciphertext[i] - key + 26) % 26;  ## Reverse the Caesar cipher shift
    }
    yield;
}

define num main(){
    list plaintext = [0, 1, 2, 3, 4, 5];  
    num key = 3;

    show(~Original text (as integers): ~);
    iter (num i = 0; i < length(plaintext); ++i) {
        show(plaintext[i],~ ~);
    }

    caesarEncrypt(plaintext, key);  ## Pass the array, size, and key to encrypt
    show(~Encrypted text (as integers): ~);
    iter (num i = 0; i < length(plaintext); ++i) {
        show(plaintext[i],~ ~);
    }

    caesarDecrypt(plaintext, key);  ##Pass the array, size, and key to decrypt
    show(~Decrypted text (as integers): ~);
    iter (num i = 0; i < length(plaintext); ++i) {
        show(plaintext[i], ~ ~);
    }

    yield 0; 
}

"""

# ----------------------------------------------------------------------------------------------------------------------------

parser_lark_dir = os.path.dirname(__file__)
def read_geko_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# testcase_folder_path = os.path.join(parser_lark_dir,"..", "testcases")
# sys.path.append(testcase_folder_path)

# if len(sys.argv) != 2:
#     print("Usage: python parser_lark.py <path to geko file>")
#     sys.exit(1)
# geko_file_path = sys.argv[-1]
# code = read_geko_file(geko_file_path)

tokens = lexer_lark.lexer(code)

# ----------------------------------------------------------------------------------------------------------------------------

tokenised_code = ""

for token in tokens:
    tokenised_code += token[0] + " "

#---------------------------------------

tree = parser.parse(tokenised_code)

graph_of_tree = lark.tree.pydot__tree_to_graph(tree)
graph = pydot.graph_from_dot_data(lark.tree.pydot__tree_to_graph(tree).to_string())

#----------------------------------------------------------------------------------------------------------------------------

png_name = "abstract_syntax_tree.png"

# ----------------------------------------------------------------------------------------------------------------------------

# Final function to be used: 
final_iteration(tree, tokens, graph=graph[0])
ast_builder = ASTBuilder()
rich.print(tree)
# print(tree)
ast = ast_builder.transform(tree)
# print(ast)


rich.print(ast)
# print("-----------------------------------------------------------------------------------------")
# a function to print the ast:
# print(type(ast))
# print("ast print kar rahe")
# print(ast)
# print_ast(ast)
# print("-----------------------------------------------------------------------------------------")
# rich.print(tree)

# ----------------------------------------------------------------------------------------------------------------------------
