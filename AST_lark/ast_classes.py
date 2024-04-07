from lark import Visitor, Tree, Token
from dataclasses import dataclass
from typing import List, Optional, Union
from typing import *

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
    operator_if_exists: Optional[str]
    terms: List['Term']

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
    is_special: Optional['SpecialFunction']
    comparison_operator: Optional[str]
    expression: 'Expression'

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

@dataclass
class ConditionalStatement:
    conditional_argument: 'ConditionalArgument'
    conditional_block: Union['YieldBlock', 'Block']
    other_blocks: Optional[List['OtherBlock']]
    otherwise_block: Optional['OtherwiseBlock']
