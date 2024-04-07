from lark import Lark
from lark.lexer import Lexer, Token
from lark.exceptions import UnexpectedToken
import re
import ast_lexer_lark as lexer_lark
import sys
import os
# ----------------------------------------------------------------------------------------------------------------------------
import lark
import pydot
from IPython.display import display
# ----------------------------------------------------------------------------------------------------------------------------
from lark import Transformer, v_args
from dataclasses import dataclass
from typing import List, Optional, Union
# ----------------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass
from typing import *
import rich

# ----------------------------------------------------------------------------------------------------------------------------
# Dataclasses for the AST

@dataclass
class Program:
    function_defs: List['FunctionDef']
    main_function: 'MainFunc'

@dataclass
class MainFunc:
    statements: List[Union['Block', 'VariableDeclaration', 'AssignmentStatement', 'ShowStatement', 'ConditionalStatement', 'LoopStatement', 'ValueChangeArray', 'PopStatement', 'TryCatchStatement', 'FunctionCall', 'UnaryStatement', 'FunctionDef']]

@dataclass
class Block:
    statements: List[Union['Block', 'VariableDeclaration', 'AssignmentStatement', 'ShowStatement', 'ConditionalStatement', 'LoopStatement', 'ValueChangeArray', 'PopStatement', 'TryCatchStatement', 'FunctionCall', 'UnaryStatement', 'FunctionDef']]

@dataclass
class AssignmentStatement:
    variable_name: str
    assignment_operators: str
    value: Union['Expression', 'SpecialFunction', 'LetInStatement']

@dataclass
class EnterStatement:
    string: str

@dataclass
class UnaryStatement:
    unary_operator: str
    # value: Union['Expression', 'SpecialFunction', 'LetInStatement']
    value: str

@dataclass
class FunctionDef:
    function_type: str
    function_name: str
    parameters: List['Parameter']
    function_block: 'FunctionBlock'

@dataclass
class FunctionBlock:
    statements: List[Union['Block', 'VariableDeclaration', 'AssignmentStatement', 'ShowStatement', 'ConditionalStatement', 'LoopStatement', 'ValueChangeArray', 'PopStatement', 'TryCatchStatement', 'FunctionCall', 'UnaryStatement', 'FunctionDef']]
    return_value: Union['Expression', 'FunctionCall']

@dataclass
class Parameter:
    data_type: Optional[str]
    parameter_name: str
    array_size: Optional[int]

@dataclass
class VariableDeclaration:
    data_type: str
    variable_name: str
    initial_value: Optional[Union['Expression', 'ListAppendTail']]
    equal_to: Optional[str]

@dataclass
class Assignment:
    variable_name: str
    assignment_operators: str
    value: Union['Expression', 'SpecialFunction', 'LetInStatement']

@dataclass
class Array:
    data_type: str
    identifier: str
    size: Optional[int]

@dataclass
class LIST:
    data_type: str
    identifier: str
    size: Optional[int]

@dataclass
class TUP:
    data_type: str
    identifier: str

@dataclass
class UnaryOperator:
    operator: str

@dataclass
class AssignmentOperator:
    operator: str


@dataclass
class SpecialFunction:
    # identifier
    # num_literal_start and num_literal_end
    # OR
    # length/head/isempty
    # identifier
    # OR
    # function_call
    identifier: str
    num_literal_start: Optional[int]
    num_literal_end: Optional[int]
    length: Optional[str]
    head: Optional[str]
    isempty: Optional[str]
    function_call: Optional['FunctionCall']
    # is upar wale ko change karna hai

@dataclass
class Expression:
    terms: List['Term']
    operations: Optional[List['BinaryOperator']]

@dataclass
class Term:
    value: Union[str, int, bool]
    identifier: Optional[str]
    expression: Optional['Expression']
    unary_operator: Optional[str]

@dataclass
class BinaryOperator:
    operator: str

@dataclass
class ConditionalStatement:
    condition: Union['SpecialFunction', 'Expression']
    conditional_block: Union['YieldBlock', 'Block']
    other_blocks: List['OtherBlock']
    otherwise_block: Optional['OtherwiseBlock']

@dataclass
class OtherBlock:
    condition: Union['SpecialFunction', 'Expression']
    conditional_block: Union['YieldBlock', 'Block']

@dataclass
class OtherwiseBlock:
    conditional_block: Union['YieldBlock', 'Block']

@dataclass
class LoopStatement:
    loop_type: str
    condition: Optional[Union['Expression', 'ConditionalArgument']]
    block: 'Block'

@dataclass
class ConditionalArgument:
    condition: Union['SpecialFunction', 'Expression']
    comparison_operator: Optional[str]

@dataclass
class TryCatchStatement:
    try_block: 'Block'
    catch_string: str
    catch_block: 'Block'

@dataclass
class YieldBlock:
    statements: List[Union['Block', 'VariableDeclaration', 'AssignmentStatement', 'ShowStatement', 'ConditionalStatement', 'LoopStatement', 'ValueChangeArray', 'PopStatement', 'TryCatchStatement', 'FunctionCall', 'UnaryStatement', 'FunctionDef']]
    expression: 'Expression'

@dataclass
class FunctionCall:
    function_name: str
    arguments: List['Expression']

@dataclass
class LetInStatement:
    data_type: str
    variable_name: str
    value: Union['Term', 'Expression', 'LetInBraces']

@dataclass
class LetInBraces:
    let_in: Union['LetInStatement', 'Expression']

@dataclass
class ListAppendTail:
    elements: List['Expression']
    identifier: Optional[str]

# @dataclass
# class CompoundVar:
#     value: Optional[Union['ListAppendTail', 'Expression']]

@dataclass
class ShowStatement:
    expressions: List['Expression']

# @dataclass
# class Statement:
#     statement_type: str
#     value: Optional[Union[
#         'Block', 'VariableDeclaration', 'Assignment', 'ShowStatement',
#         'ConditionalStatement', 'LoopStatement', 'ValueChangeArray',
#         'PopStatement', 'TryCatchStatement', 'FunctionCall', 'FunctionDef'
#     ]]

@dataclass
class ValueChangeArray:
    identifier: str
    index: int
    assignment_operators: str
    value: 'Expression'

@dataclass
class PopStatement:
    string_value: str

@dataclass
class EqualTo:
    value: list

#================================
from lark import Visitor, Tree, Token
from dataclasses import dataclass
from typing import List, Optional, Union

# AST node classes (imported from the previous code)

class ASTBuilder(Visitor):
    def __default__(self, tree):
        children = [self.transform(child) for child in tree.children]
        print("----------------------------------------------------------")
        print(f"the tree data from __default__ is: {tree.data}, children are: {children}")
        return self.create_node(tree.data, children)

    def create_node(self, node_type, children):
        print("----------------------------------------------------------")
        print(f"node_type from create_node: {node_type}, children: {children}")
        print("----------------------------------------------------------")
        if node_type == "start":
            print(f"node_type: {node_type}, value: {children[0]}")
            return children[0]
        elif node_type == "program":
            function_defs = [child for child in children[:-1] if isinstance(child, FunctionDef)]
            main_function = children[-1] # if children[-1].__class__.__name__ == "MainFunc" else None
            # if isinstance(children[-1], FunctionDef) else None
            print(f"node_type:{node_type}, function_defs: {function_defs}, main_function: {main_function}")
            return Program(function_defs, main_function)
        elif node_type == "main_func":
            statements = children[6]
            return MainFunc(statements)
        elif node_type == "func_def":
            print("ye func_def bhi galat hai isko bhi change crow")
            function_type = str(children[1])
            function_name = str(children[2])
            parameters = children[3]
            function_block = children[5]
            print(f"node_type:{node_type}, function_type: {function_type}, function_name: {function_name}, parameters: {parameters}, function_block: {function_block}")
            return FunctionDef(function_type, function_name, parameters, function_block)
        elif node_type == "function_block":
            statements = children[1]
            return_value = children[3]
            print(f"node_type:{node_type}, statements: {statements}, return_value: {return_value}")
            return FunctionBlock(statements, return_value)
        elif node_type == "function_type":
            print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        elif node_type == "parameter_list":
            parameters = children[0] if children else []
            print(f"node_type:{node_type}, parameters: {parameters}")
            return parameters
        elif node_type == "return_value":
            print(f"node_type:{node_type}, value: {children[0]}")
            return children[0]
        elif node_type == "parameters":
            if not children:
                return []
            parameters = [children[1]]
            parameters.extend(children[2])
            print(f"node_type:{node_type}, parameters: {parameters}")
            return parameters
        elif node_type == "parameter":
            if len(children) == 2:
                data_type = str(children[0])
                parameter_name = str(children[1])
                print(f"node_type:{node_type}, parameter_name: {parameter_name}")
                return Parameter(None, parameter_name, None)
            else:
                data_type = str(children[0])
                parameter_name = str(children[1])
                array_size = int(children[2].value) if len(children) > 2 else None
                print(f"node_type:{node_type}, data_type: {data_type}, parameter_name: {parameter_name}, array_size: {array_size}")
                return Parameter(data_type, parameter_name, array_size)
        elif node_type == "choose_array":
            if not children:
                print(f"node_type:{node_type}, value: None")
                return None
            print(f"node_type:{node_type}, value: {children[1]}")
            return children[1]
        elif node_type == "statements":
            # if not children:
            #     print(f"node_type:{node_type}, value: []")
            #     return []
            statements = [children[0]]
            if children[0] == None:
                print(f"node_type:{node_type}, value: {children[0]}")
                return statements
            if children[1]!=None:
                statements.extend(children[1])
            print(f"node_type:{node_type}, statements: {statements}")
            return statements
        elif node_type == "equal_to":
            if not children:
                print(f"node_type:{node_type}, value: []")
                return []
            print(f"node_type:{node_type}, value: {children[1]}")
            return children[1]
        elif node_type == "post_equal_to":
            # TODO - handle ENTER or enter
            # children[0].value/data ??
            if children[0] == "enter":
                value = str(children[2])
            else:
                value = children[0]
            print(f"node_type:{node_type}, value: {value}")
            return value
        
        # elif node_type == "post_equal_to":
        #     if len(children) == 1:
        #         value = children[0]
        #         print(f"node_type:{node_type}, value: {value}")
        #         return value
        #     elif len(children) == 4 and children[0] == "ENTER":
        #         string_value = str(children[2])
        #         print(f"node_type:{node_type}, value: {string_value}")
        #         return string_value
        #     else:
        #         raise ValueError("Unexpected structure for 'post_equal_to' node")


        elif node_type == "special_function":
            if len(children) == 1:
                function_call = children[0]
                print(f"node_type:{node_type}, function_call: {function_call}")
                return SpecialFunction(None, None, None, None, None, None, function_call)
            else:
                if children[0] == "length":
                    identifier = str(children[2])
                    print(f"node_type:{node_type}, identifier: {identifier}")
                    return SpecialFunction(identifier, None, None, "length", None, None, None)
                elif children[0] == "head":
                    identifier = str(children[2])
                    print(f"node_type:{node_type}, identifier: {identifier}")
                    return SpecialFunction(identifier, None, None, None, "head", None, None)
                elif children[0] == "isempty":
                    identifier = str(children[2])
                    print(f"node_type:{node_type}, identifier: {identifier}")
                    return SpecialFunction(identifier, None, None, None, None, "isempty", None)

                identifier = str(children[0])
                # .value?? .data?? ya phir children[2][0]???
                num_literal_start = int(children[2].value)
                num_literal_end = int(children[4].value)
                print(f"node_type:{node_type}, identifier: {identifier}, num_literal_start: {num_literal_start}, num_literal_end: {num_literal_end}")
                return SpecialFunction(identifier, num_literal_start, num_literal_end, None, None, None, None)
        elif node_type == "data_type":
            print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0]) if children else None
        elif node_type == "num_str_flag":
            print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        elif node_type == "basic_data_type":
            fix_let = str(children[0])
            data_type = str(children[-1])
            print(f"node_type:{node_type}, fix_let: {fix_let}, data_type: {data_type}")
            return f"{fix_let} {data_type}" if fix_let else data_type
        elif node_type == "fix_let":
            print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0]) if children else None
        elif node_type == "compound_data_type":
            print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        # elif node_type == "string":
        #     print(f"node_type:{node_type}, value: {children[1]}")
        #     # TODO vapis value???
        #     return children[1].value
        elif node_type == "string":
            # The string is wrapped with tildes (~), so we need to remove them
            # and return the string value.
            print(f"node_type:{node_type}, value: {children[1]}")
            string_value = str(children[1])
            return string_value

        elif node_type == "array":
            data_type = str(children[0])
            identifier = str(children[1])
            # TODO vapis value???
            size = int(children[3])
            print(f"node_type:{node_type}, data_type: {data_type}, identifier: {identifier}, size: {size}")
            return Array(data_type, identifier, size)
        # elif node_type == "variable_declaration":
        #     data_type = str(children[0])
        #     variable_name = str(children[1])
        #     equal_to = children[2] if len(children) > 2 else None
        #     # pending work
        #     print(f"node_type:{node_type}, data_type: {data_type}, variable_name: {variable_name}, initial_value: {initial_value}, equal_to: {equal_to}")
        #     return VariableDeclaration(data_type, variable_name, initial_value, equal_to)
        elif node_type == "variable_declaration":
            if children[0].__class__.__name__ == "Array":
                data_type = "Array " + children[0].data_type
                variable_name = children[0].identifier
                initial_value = children[0].size
                equal_to = None
            else:
                data_type = children[0]
                variable_name = str(children[1])
                equal_to = None
                initial_value = None

                if len(children) > 2:
                    equal_to = children[2]
                    if isinstance(equal_to, list):
                        if isinstance(equal_to[1], Expression) or isinstance(equal_to[1], SpecialFunction) or isinstance(equal_to[1], LetInStatement):
                            initial_value = equal_to[1]
                        elif isinstance(equal_to[1], str):
                            equal_to = equal_to[1]
                    else:
                        initial_value = equal_to
                        equal_to = None
                    # elif isinstance(equal_to, Expression) or isinstance(equal_to, SpecialFunction) or isinstance(equal_to, LetInStatement):
                    #     initial_value = equal_to
                    #     equal_to = None
            print(f"node_type:{node_type}, data_type: {data_type}, variable_name: {variable_name}, initial_value: {initial_value}, equal_to: {equal_to}")
            return VariableDeclaration(data_type, variable_name, initial_value, equal_to)
        
        elif node_type == "post_equal_to":
            if len(children) == 4 and children[0] == "ENTER":
                string_value = str(children[2])
                return string_value
            elif len(children) == 1:
                return children[0]
            else:
                raise ValueError("Unexpected structure for 'post_equal_to' node")

        elif node_type == "compound_array":
            if len(children) == 1:
                return children[0]
            else:
                data_type = str(children[0])
                identifier = str(children[1])
                if data_type == "list":
                    print(f"node_type:{node_type}, data_type: {data_type}, identifier: {identifier}")
                    return LIST(data_type, identifier, None)
                else:
                    print(f"node_type:{node_type}, data_type: {data_type}, identifier: {identifier}")
                    return TUP(data_type, identifier)
        
        # elif node_type == "variable_declaration":
        #     data_type = str(children[0])
        #     variable_name = str(children[1])
        #     equal_to = children[2] if len(children) > 2 else None
        #     print(f"abhi variable declaration mai hai, kuch dikkat aa rahi hai. Ye rahe children: {children}")
        #     initial_value = children[3] if len(children) > 3 else None
        #     print(f"node_type:{node_type}, data_type: {data_type}, variable_name: {variable_name}, initial_value: {initial_value}")
        #     return VariableDeclaration(data_type, variable_name, initial_value, equal_to)
        elif node_type == "compound_var":

            if len(children) == 1:
                return None
            elif len(children) == 2:
                if children[0] == "EQUAL_TO":
                    return 
                else:
                    return children[0]
            elif len(children) == 4:
                if children[0] == "EQUAL_TO":
                    return BinaryOperator(children[2], children[1], children[3])
                else:
                    return children[0]
            else:
                return None
        
        elif node_type == "list_append_tail":
            elements = None
            identifier = None
            if children[0] == "expressions":
                elements = children[1]
                identifier = None
            elif children[0] == "TAIL":
                elements = None
                identifier = str(children[2])
            elif children[0] == "APPEND":
                elements = [children[2]]
                identifier = str(children[4])
            print(f"node_type:{node_type}, elements: {elements}, identifier: {identifier}")
            return ListAppendTail(elements, identifier)
        elif node_type == "assignment_statement":
            variable_name = str(children[0])
            assignment_operators = str(children[1])
            value = children[2]
            print(f"node_type:{node_type}, variable_name: {variable_name}, assignment_operators: {assignment_operators}, value: {value}")
            return Assignment(variable_name, assignment_operators, value)
        elif node_type == "show_statement":
            expressions = children[2]
            print(f"node_type:{node_type}, expressions: {expressions}")
            return ShowStatement(expressions)
        elif node_type == "block":
            statements = children[1]
            print(f"node_type:{node_type}, statements: {statements}")
            return Block(statements)
        elif node_type == "value_change_array":
            identifier = str(children[0])
            index = int(children[2].value)
            assignment_operators = str(children[3])
            value = children[4]
            print(f"node_type:{node_type}, identifier: {identifier}, index: {index}, assignment_operators: {assignment_operators}, value: {value}")
            return ValueChangeArray(identifier, index, assignment_operators, value)
        elif node_type == "expressions":
            if not children:
                print(f"node_type:{node_type}, value: []")
                return []
            expressions = [children[1]] if len(children) > 1 else []
            expressions.extend(children[2]) if len(children) > 2 else None
            print(f"node_type:{node_type}, expressions: {expressions}")
            return expressions
        elif node_type == "expression":
            terms = children[0] if children else []
            operations = children[1] if len(children) > 1 else None
            print(f"node_type:{node_type}, terms: {terms}, operations: {operations}")
            return Expression(terms, operations)
        elif node_type == "terms":
            print(f"the children of terms are as follows: {[child for child in children]}")
            if not children:
                print(f"node_type:{node_type}, value: []")
                return []
            operators = [children[0]]
            terms = [children[1]] if len(children) > 1 else None
            terms.extend(children[2]) if len(children) > 2 else None
            print(f"node_type:{node_type}, operators: {operators}, terms: {terms}")
            if terms is None:
                return None, None
            return [operator for operator in operators for _ in terms], terms
        elif node_type == "term":
            value = children[0]
            identifier = None
            expression = None
            unary_operator = None
            if isinstance(children[0], Token):
                value = "garbaaj"
                # print("children[0]:", children[0])
                # print("fdaffavra:", children[0].value)
                value = children[0].value
                value = children[0][0]
                if children[0].type == "IDENTIFIER":
                    identifier = value
                    # value = None
                    value = "garbaaj identifier"
                elif children[0].type in ["NUM_LITERAL", "YAY", "NAY"]:
                    identifier = None
                else:
                    raise ValueError(f"Unexpected token type: {children[0].type}")
                expression = None
                unary_operator = None
            elif children[0] == "string":
                # value = children[0].children[0].value
                value = "garbaaj string"
                identifier = None
                expression = None
                unary_operator = None
            elif children[0] == "expression":
                # value = None
                value = "garbaaj expression"
                identifier = None
                expression = children[0]
                unary_operator = None
            elif children[0] == "unary_operators":
                # value = None
                value = "garbaaj unary_operators"
                identifier = str(children[1])
                expression = None
                unary_operator = str(children[0])
            elif children[0] == "IDENTIFIER":
                # value = None
                value = "garbaaj identifier"
                identifier = str(children[0])
                expression = children[2] if len(children) > 2 else None
                unary_operator = str(children[1]) if len(children) > 1 else None
            print(f"node_type:{node_type}, value: {value}, identifier: {identifier}, expression: {expression}, unary_operator: {unary_operator}")
            return Term(value, identifier, expression, unary_operator)
        elif node_type == "binary_operators":
            print(f"node_type:{node_type}, value: {children[0]}")
            return BinaryOperator(str(children[0]))
        elif node_type == "unary_operators":
            print(f"node_type:{node_type}, value: {children[0]}")
            return UnaryOperator(str(children[0]))
        elif node_type == "assignment_operators":
            print(f"node_type:{node_type}, value: {children[0]}")
            return AssignmentOperator(str(children[0]))
        elif node_type == "conditional_block":
            print(f"node_type:{node_type}, value: {children[0]}")
            return children[0]
        elif node_type == "conditional_argument":
            # if children[0].data == "special_function":
            if children[0] == "special_function":
                condition = children[0]
                comparison_operator = str(children[1]) if len(children) > 1 else None
            else:
                condition = children[0]
                comparison_operator = None
            print(f"node_type:{node_type}, condition: {condition}, comparison_operator: {comparison_operator}")
            return ConditionalArgument(condition, comparison_operator)
        elif node_type == "conditional_statement":
            condition = children[2]
            conditional_block = children[4]
            other_blocks = children[5]
            otherwise_block = children[6] if len(children) > 6 else None
            print(f"node_type:{node_type}, condition: {condition}, conditional_block: {conditional_block}, other_blocks: {other_blocks}, otherwise_block: {otherwise_block}")
            return ConditionalStatement(condition, conditional_block, other_blocks, otherwise_block)
        elif node_type == "other_block":
            if children == [None]:
                print(f"node_type:{node_type}, value: []")
                return []
            condition = children[2]
            conditional_block = children[4]
            other_blocks = children[5] if len(children) > 5 else []
            print(f"node_type:{node_type}, condition: {condition}, conditional_block: {conditional_block}, other_blocks: {other_blocks}")
            return [OtherBlock(condition, conditional_block)] + other_blocks
        elif node_type == "otherwise_block":
            print(f"node_type:{node_type}, value: {children[0]}")
            return OtherwiseBlock(children[0])
        elif node_type == "loop_statement":
            if children[0].data == "ITER":
                loop_type = "iter"
                condition = [children[2], children[4]]
                block = children[6]
            elif children[0].data == "WHILE":
                loop_type = "while"
                condition = children[2]
                block = children[4]
            elif children[0].data == "REPEAT":
                loop_type = "repeat"
                condition = children[4]
                block = children[2]
            print(f"node_type:{node_type}, loop_type: {loop_type}, condition: {condition}, block: {block}")
            return LoopStatement(loop_type, condition, block)
        elif node_type == "pop_statement":
            string_value = children[2].children[0].value
            print(f"node_type:{node_type}, string_value: {string_value}")
            return PopStatement(string_value)
        elif node_type == "try_catch_statement":
            try_block = children[1]
            catch_string = children[4].children[0].value
            catch_block = children[6]
            print(f"node_type:{node_type}, try_block: {try_block}, catch_string: {catch_string}, catch_block: {catch_block}")
            return TryCatchStatement(try_block, catch_string, catch_block)
        elif node_type == "yield_block":
            statements = children[1]
            expression = children[3]
            print(f"node_type:{node_type}, statements: {statements}, expression: {expression}")
            return YieldBlock(statements, expression)
        elif node_type == "function_call":
            function_name = str(children[0])
            arguments = children[2]
            print(f"node_type:{node_type}, function_name: {function_name}, arguments: {arguments}")
            return FunctionCall(function_name, arguments)
        elif node_type == "argument_list":
            if not children:
                print(f"node_type:{node_type}, value: []")
                return []
            arguments = [children[0]]
            arguments.extend(children[1])
            print(f"node_type:{node_type}, arguments: {arguments}")
            return arguments
        elif node_type == "let_in_braces":
            let_in = children[0]
            print(f"node_type:{node_type}, let_in: {let_in}")
            return LetInBraces(let_in)
        elif node_type == "let_in":
            if isinstance(children[0], LetInStatement):
                print(f"node_type:{node_type}, value: {children[0]}")
                return children[0]
            else:
                print(f"node_type:{node_type}, value: {children[0]}")
                return children[0]
        elif node_type == "let_in_statement":
            data_type = str(children[1])
            variable_name = str(children[2])
            if children[4] == "OPEN_BRACES":
                value = children[5]
            else:
                value = children[4]
            if len(children) > 6:
                value = LetInBraces(value)
            print(f"node_type:{node_type}, data_type: {data_type}, variable_name: {variable_name}, value: {value}")
            return LetInStatement(data_type, variable_name, value)
        elif node_type == "statement":
            # statement_type = children[0].data
            # statement_type = children[0] # ye galat hai i know, isko change karna padenga
            statement_type = children[0].__class__.__name__
            value = children[0]
            print(f"node_type:{node_type}, statement_type: {statement_type}, value: {value}")
            return children[:-1] if children[-1] == "END_OF_LINE" else children
            # return Statement(statement_type, value)
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
            print(f"node_type:{node_type}, function_type: {function_type}, arguments: {arguments}")
            return SpecialFunction(function_type, arguments)
        elif node_type == "data_type":
            print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0]) if children else None
        elif node_type == "num_str_flag":
            print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        elif node_type == "basic_data_type":
            fix_let = str(children[0]) if children else None
            data_type = str(children[1])
            print(f"node_type:{node_type}, fix_let: {fix_let}, data_type: {data_type}")
            return f"{fix_let} {data_type}" if fix_let else data_type
        elif node_type == "fix_let":
            print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0]) if children else None
        elif node_type == "compound_data_type":
            print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])
        elif node_type == "string":
            print(f"node_type:{node_type}, value: {children[1]}")
            return children[1].value
        elif node_type == "skip_stop":
            print(f"node_type:{node_type}, value: {children[0]}")
            return str(children[0])

    def transform(self, tree):
        if isinstance(tree, Tree):
            print("this is the start from a tree node i.e. transform...")
            # print()
            print("tree.data from transform is:",tree.data)
            print()
            return self.__default__(tree)
        elif isinstance(tree, Token):
            print("value from transform is:",tree.value)
            print()
            return tree.value
        else:
            raise ValueError(f"Unexpected input: {tree}")

# ----------------------------------------------------------------------------------------------------------------------------

# def read_geko_file(file_path):
#     with open(file_path, 'r') as file:
#         return file.read()
    
# --------------------------------------------------------------------------------------------
    
# we have to perform dfs on the tree to get the leaf nodes and then we can append the value
# def dfs(tree_node, leaf_nodes):
#     if isinstance(tree_node, Token):
#         leaf_nodes.append(tree_node)
#     else:
#         for child in tree_node.children:
#             dfs(child, leaf_nodes)

# --------------------------------------------------------------------------------------------

# USE THIS FUNCTION, THIS WORKS:
def final_iteration(tree_node, tokens,graph, parent_node=None):
    if isinstance(tree_node, lark.Tree):
        for child in tree_node.children:
            final_iteration(child, tokens,graph, parent_node=tree_node)
            # ye to ho gaya childs ka
    else:
        # Handle leaf nodes (tokens)
        if isinstance(tree_node, lark.Token):
            new_token = tokens.pop(0)
            new_node = (new_token[0], new_token[1])
            tree_node.value = new_node[1]

        else:
            print("Unknown leaf node type:", tree_node)
    # return graph
# --------------------------------------------------------------------------------------------
            
# Grammar for the parser
grammar = """
start                   :   program
program	                :	main_func
                        |   func_def program
main_func               :   DEFINE NUM MAIN OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_BRACES statements YIELD NUM_LITERAL END_OF_LINE CLOSE_BRACES
func_def                :   DEFINE function_type IDENTIFIER OPEN_PARENTHESIS parameter_list CLOSE_PARENTHESIS function_block

function_block	        :	OPEN_BRACES statements YIELD return_value END_OF_LINE CLOSE_BRACES
function_type	        :	NUM | STR | FLAG | VOID
parameter_list	        :	parameter parameters | epsilon
return_value	        :	expression | function_call
parameters	            :	ELEMENT_SEPERATOR parameter parameters 
                        |   epsilon
parameter	            :	compound_data_type IDENTIFIER | basic_data_type IDENTIFIER choose_array
choose_array            :   OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET | epsilon                        

statements	            :	statement statements
                        |   epsilon
equal_to                :   EQUAL_TO post_equal_to | epsilon
post_equal_to           :   ENTER OPEN_PARENTHESIS string CLOSE_PARENTHESIS 
                        |   expression
                        |   special_function
                        |   let_in_statement 
                        
special_function        :   IDENTIFIER OPEN_BRACKET NUM_LITERAL SLICING_COLON NUM_LITERAL CLOSE_BRACKET
                        |   LENGTH OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS
                        
                        |   HEAD OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS
                        |   ISEMPTY OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS
                        |   function_call

data_type	            :  	basic_data_type 
                        |   compound_data_type 
                        |   epsilon
num_str_flag	        :	NUM | STR | FLAG
basic_data_type	        :	fix_let num_str_flag
fix_let	                :	FIX | LET | epsilon
compound_data_type	    :	LIST | TUP


string	                :	TILDE STRING_LITERAL TILDE
array	                :	basic_data_type IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET

variable_declaration	:	basic_data_type IDENTIFIER equal_to
                        |   compound_array compound_var

compound_array          :   compound_data_type IDENTIFIER
                        |   array 

compound_var            :   EQUAL_TO list_append_tail
                        |   EQUAL_TO compound_element BINARY_OPERATOR compound_element
                        |   epsilon

compound_element        :   IDENTIFIER
                        |   OPEN_BRACKET expression expressions CLOSE_BRACKET

list_append_tail        :   OPEN_BRACKET expression expressions CLOSE_BRACKET
                        |   TAIL OPEN_PARENTHESIS IDENTIFIER CLOSE_PARENTHESIS
                        |   APPEND OPEN_PARENTHESIS expression ELEMENT_SEPERATOR IDENTIFIER CLOSE_PARENTHESIS

assignment_statement	:	IDENTIFIER assignment_operators post_equal_to
show_statement	        :	SHOW OPEN_PARENTHESIS expression expressions CLOSE_PARENTHESIS
block	                :	OPEN_BRACES statements CLOSE_BRACES
value_change_array	    :	IDENTIFIER OPEN_BRACKET NUM_LITERAL CLOSE_BRACKET assignment_operators expression

expressions             :   ELEMENT_SEPERATOR expression expressions
                        |   epsilon
expression	            :   term terms | epsilon
terms	                :	binary_operators term terms 
                        |   epsilon
                        
term	                :   IDENTIFIER
                        |   NUM_LITERAL
                        |   string
                        |   YAY
                        |   NAY
                        |   OPEN_PARENTHESIS expression CLOSE_PARENTHESIS
                        |   unary_operators IDENTIFIER
                        |   IDENTIFIER UNARY_OPERATOR
                        |   IDENTIFIER OPEN_BRACKET expression CLOSE_BRACKET
                        |   LENGTH
                        
binary_operators	    :	BINARY_OPERATOR 
                        |   COMPARISON_OPERATOR 
                        |   BINARY_LOGICAL_OPERATOR
unary_operators	        :	UNARY_OPERATOR
                        |   UNARY_LOGICAL_OPERATOR
assignment_operators	:	EQUAL_TO
                        |   ASSIGNMENT_OPERATOR
                        
conditional_block       :   yield_block 
                        |   block
conditional_argument    :   special_function COMPARISON_OPERATOR expression
                        |   expression
conditional_statement	:	GIVEN OPEN_PARENTHESIS conditional_argument CLOSE_PARENTHESIS conditional_block other_block otherwise_block
other_block	            :	OTHER OPEN_PARENTHESIS conditional_argument CLOSE_PARENTHESIS conditional_block other_block
                        |   epsilon 
otherwise_block	        :	OTHERWISE conditional_block
                        |   epsilon
skip_stop               :   SKIP
                        |   STOP

loop_statement	        :	ITER OPEN_PARENTHESIS statement expression END_OF_LINE expression CLOSE_PARENTHESIS block
                        |   WHILE OPEN_PARENTHESIS conditional_argument CLOSE_PARENTHESIS block
                        |   REPEAT block WHILE OPEN_PARENTHESIS conditional_argument CLOSE_PARENTHESIS END_OF_LINE

pop_statement           :   POP OPEN_PARENTHESIS string CLOSE_PARENTHESIS

try_catch_statement	    :	TEST block ARREST OPEN_PARENTHESIS string CLOSE_PARENTHESIS block

yield_block             :   OPEN_BRACES statements YIELD expression END_OF_LINE CLOSE_BRACES

function_call	        :	IDENTIFIER OPEN_PARENTHESIS argument_list CLOSE_PARENTHESIS

argument_list	        :	expression expressions

let_in_braces           :   let_in CLOSE_BRACES
let_in                  :   let_in_statement | expression
let_in_statement	    :   LET data_type IDENTIFIER EQUAL_TO OPEN_BRACES let_in_braces
                        |   LET data_type IDENTIFIER EQUAL_TO term IN OPEN_BRACES let_in_braces
                        |   LET data_type IDENTIFIER EQUAL_TO term IN let_in

statement	            :	block
                        |   variable_declaration END_OF_LINE
                        |   assignment_statement END_OF_LINE
                        |   show_statement END_OF_LINE
                        |   conditional_statement
                        |   loop_statement
                        |   skip_stop END_OF_LINE
                        |   value_change_array END_OF_LINE
                        |   pop_statement END_OF_LINE
                        |   try_catch_statement
                        |   function_call END_OF_LINE
                        |   unary_operators IDENTIFIER END_OF_LINE
                        |   IDENTIFIER UNARY_OPERATOR END_OF_LINE
                        |   func_def

epsilon :
NUM: "NUM"
STR: "STR"
FLAG: "FLAG"
FIX: "FIX"
SHOW: "SHOW"
ITER: "ITER"
LIST: "LIST"
TUP: "TUP"
ENTER: "ENTER"
YIELD: "YIELD"
LET: "LET"
IN: "IN"
VOID: "VOID"
WHILE: "WHILE"
REPEAT: "REPEAT"
GIVEN: "GIVEN"
OTHER: "OTHER"
OTHERWISE: "OTHERWISE"
DEFINE: "DEFINE"
TEST: "TEST"
POP: "POP"
ARREST: "ARREST"
LENGTH: "LENGTH"
HEAD: "HEAD"
TAIL: "TAIL"
ISEMPTY: "ISEMPTY"
APPEND: "APPEND"
SKIP: "SKIP"
STOP: "STOP"
YAY: "YAY"
NAY: "NAY"
MAIN: "MAIN"
IDENTIFIER: "IDENTIFIER"
OPEN_PARENTHESIS: "OPEN_PARENTHESIS"
CLOSE_PARENTHESIS: "CLOSE_PARENTHESIS"
OPEN_BRACES: "OPEN_BRACES"
CLOSE_BRACES: "CLOSE_BRACES"
OPEN_BRACKET: "OPEN_BRACKET"
CLOSE_BRACKET: "CLOSE_BRACKET"
NUM_LITERAL: "NUM_LITERAL"
STRING_LITERAL: "STRING_LITERAL"
END_OF_LINE: "END_OF_LINE"
SLICING_COLON: "SLICING_COLON"
ELEMENT_SEPERATOR: "ELEMENT_SEPERATOR"
COMPARISON_OPERATOR: "COMPARISON_OPERATOR"
ASSIGNMENT_OPERATOR: "ASSIGNMENT_OPERATOR"
UNARY_OPERATOR: "UNARY_OPERATOR"
BINARY_OPERATOR: "BINARY_OPERATOR"
BINARY_LOGICAL_OPERATOR: "BINARY_LOGICAL_OPERATOR"
UNARY_LOGICAL_OPERATOR: "UNARY_LOGICAL_OPERATOR"
TILDE: "TILDE"
EQUAL_TO: "EQUAL_TO"

%import common.NUMBER
%import common.WS
%ignore WS"""

#----------------------------------------------------------------------------------------------------------------------------

# Create the Lark parser
parser = Lark(grammar, start='start', parser = 'lalr')#, lexer = lexer_lark)

code = """
define num main() {
    ## add(1, 2);
    num a = 4;
    given(a == 4 && a == 5) {
        show(a);
    } otherwise {
        show(0);
    }
    yield 0;
}"""
# ----------------------------------------------------------------------------------------------------------------------------

parser_lark_dir = os.path.dirname(__file__)
tokens = lexer_lark.lexer(code)

# ----------------------------------------------------------------------------------------------------------------------------

tokenised_code = ""

for token in tokens:
    # print(type(token[0]))
    tokenised_code += token[0] + " "

#---------------------------------------

tree = parser.parse(tokenised_code)

graph_of_tree = lark.tree.pydot__tree_to_graph(tree)
graph = pydot.graph_from_dot_data(lark.tree.pydot__tree_to_graph(tree).to_string())
# function toh chal gaya

#----------------------------------------------------------------------------------------------------------------------------

png_name = "abstract_syntax_tree.png"
# graph bhi chal gaya!

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
