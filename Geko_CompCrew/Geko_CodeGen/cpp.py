import sys
import os

# join ../Geko_AST to sys path variables
sys.path.append(os.path.abspath('./'))
sys.path.append(os.path.abspath("../Geko_AST"))
sys.path.append(os.path.abspath("../Geko_SemanticAnalysis"))

from ast_final import *
from ast_classes import *
from semantic_analyser import *
import rich
# Code Generation
type_map = {
    'num': 'int',
    'str': 'std::string',  # Python doesn't have char*, strings are used instead
    'list': 'std::vector',   # Python list for any list type
    'tup': 'std::tuple', # Python tuple for tuple types
    'flag': 'bool', # Python's bool for flag
    'fix': 'const',
    'void': 'void',
    'int': 'int'
}





def write_code_main(node, file, symbol_table, ntabs=0):
    if node is None:
        return
    if node.__class__.__name__ == "function":
        # Assuming the main function setup
        file.write("int main() {\n")
        for child in node.children:
            write_code_main(child, file, symbol_table, ntabs + 1)
        file.write("\treturn 0;\n}\n")

    elif node.__class__.__name__ == "FunctionDef":
        print("Function definition found")
        write_function_definition(node, file, symbol_table, ntabs)

    elif node.__class__.__name__ == "SpecialFunction":
        write_special_function(node, file, symbol_table, ntabs)


    elif node.__class__.__name__ == "VariableDeclaration":
        write_variable_declaration(node, file, symbol_table, ntabs)
    
    elif node.__class__.__name__ == "LoopStatement":
        write_loop_statement(node, file, symbol_table, ntabs=0)

    elif node.__class__.__name__ == "Expression":
        write_expression(node, file, symbol_table, ntabs)
    
    elif node.__class__.__name__ == "Term":
        write_term(node, file, symbol_table, ntabs)
        file.write(";\n")  # Assuming terms outside expressions need to be terminated with a semicolon
    elif node.__class__.__name__ == "FunctionCall":
        write_function_call(node, file, symbol_table, ntabs)

    elif node.__class__.__name__ == "ListAppendTail":
        write_list_append_tail(node, file, symbol_table, ntabs)

    elif node.__class__.__name__ == "Block":
        write_block(node, file, symbol_table, ntabs)

    elif node.__class__.__name__ == "OtherBlock":
        write_other_block(node, file, symbol_table, ntabs)

    elif node.__class__.__name__ == "ValueChangeArray":
        write_value_change_array(node, file, symbol_table, ntabs)

    elif node.__class__.__name__ == "ConditionalStatement":
        file.write("if (")
        write_conditional_argument(node.conditional_argument, file, symbol_table, ntabs)
        file.write(") {\n")
        write_block(node.conditional_block, file, symbol_table, ntabs + 1)
        file.write("}\n")
        if node.other_blocks:
            for other_block in node.other_blocks:
                write_other_block(other_block, file, symbol_table, ntabs)
        if node.otherwise_block:
            write_otherwise_block(node.otherwise_block, file, symbol_table, ntabs)

    elif node.__class__.__name__ == "Assignment":
        write_assignment(node, file, symbol_table, ntabs)

    elif node.__class__.__name__ == "LetInStatement":
        write_let_in_statement(node, file, symbol_table, ntabs)

    elif node.__class__.__name__ == "UnaryStatement":
        write_unary_statement(node, file, symbol_table, ntabs)

    elif node.__class__.__name__ == "LoopStatement":
        write_loop_statement(node, file, symbol_table, ntabs)

    elif node.__class__.__name__ == "ShowStatement":
        print_tabs(ntabs, file)
        file.write("std::cout << ")
        for i, expr in enumerate(node.expressions):
            write_expression(expr, file, symbol_table, ntabs)
            if i < len(node.expressions) - 1:
                file.write(" << ' ' << ")
        file.write(" << std::endl;\n")


    elif node.__class__.__name__ == "TryCatchStatement":
        print_tabs(ntabs, file)
        file.write("try {\n")
        write_code_main(node.try_block, file, symbol_table, ntabs + 1)
        print_tabs(ntabs, file)
        file.write(f"}} catch ({node.catch_string}) {{\n")
        write_code_main(node.catch_block, file, symbol_table, ntabs + 1)
        print_tabs(ntabs, file)
        file.write("}\n")


    elif node.__class__.__name__ == "ConditionalStatement":
        write_conditional_statement(node, file, symbol_table, ntabs)

    elif node.__class__.__name__ == "FunctionCall":
        file.write(node.function_name + "(")
        file.write(", ".join([write_expression(arg, symbol_table) for arg in node.arguments]))
        file.write(");\n")

    else:
        # Handling other nodes generically
        print_tabs(ntabs, file)
        file.write("int main() {\n")
        for child in node.statements:
            write_code_main(child, file, symbol_table, ntabs + 1)
        file.write("\treturn 0;\n}\n")


def write_value_change_array(node, file, symbol_table, ntabs=0):
    # Helper function to print tabs
    def print_tabs(ntabs, file):
        file.write('\t' * ntabs)

    print_tabs(ntabs, file)
    # Writing the array element modification line
    file.write(f"{node.identifier}[{node.index}] {node.assignment_operators.operator} ")
    write_expression(node.value, file, symbol_table, 0)  # Write the expression to be assigned
    file.write(";\n")


def write_loop_statement(node, file, symbol_table, ntabs=0):

    print_tabs(ntabs, file)
    
    # Determine the type of loop and write the appropriate loop header
    if node.loop_type == "iter":
        # Start the for loop
        file.write("for (")
        if node.declaration:
            if isinstance(node.declaration, VariableDeclaration):
                write_variable_declaration(node.declaration, file, symbol_table, 0)  # Inline declaration, no newline
            elif isinstance(node.declaration, AssignmentStatement):
                write_assignment(node.declaration, file, symbol_table, 0)  # Inline assignment, no newline
        else:
            file.write("; ")
        
        if node.condition:
            if isinstance(node.condition, Expression):
                write_expression(node.condition, file, symbol_table, 0)  # Inline condition, no newline
            elif isinstance(node.condition, ConditionalArgument):
                write_conditional_argument(node.condition, file, symbol_table, 0)  # Inline conditional argument
        file.write("; ")
        
        if node.updation:
            if isinstance(node.updation, AssignmentStatement):
                write_assignment(node.updation, file, symbol_table, 0)  # Inline update, no newline
            elif isinstance(node.updation, UnaryStatement):
                write_unary_statement(node.updation, file, symbol_table, 0, inline=True)  # Inline unary update
        
        file.write(") {\n")

    elif node.loop_type == "while":
        # Start the while loop
        file.write("while (")
        if node.condition:
            if isinstance(node.condition, Expression):
                write_expression(node.condition, file, symbol_table, 0)  # Inline condition
            elif isinstance(node.condition, ConditionalArgument):
                write_conditional_argument(node.condition, file, symbol_table, 0)  # Inline conditional argument
        file.write(") {\n")

    # Write the loop body
    write_block(node.block, file, symbol_table, ntabs + 1)

    # Close the loop
    print_tabs(ntabs, file)
    file.write("}\n")


def write_list_append_tail(node, file, symbol_table, ntabs=0):

    # If identifier is given, use it to perform the append operations
    if node.identifier:
        # Iterate over each expression in the elements list
        for expr in node.elements:
            print_tabs(ntabs, file)
            # Assuming append uses a method like push_back for std::vector
            file.write(f"{node.identifier}.push_back(")
            write_expression(expr, file, symbol_table, 0)  # Write the expression for the element to be appended
            file.write(");\n")

        # If there's a tail operation to handle, add that code (assuming custom behavior)
        if node.tail:
            print_tabs(ntabs, file)
            file.write(f"{node.tail}({node.identifier});\n")  # Example: tail_operation(list_identifier);

        # If there's an additional custom append method specified
        if node.append:
            print_tabs(ntabs, file)
            # Handle the custom append, which could be something like a special function
            file.write(f"{node.identifier}.{node.append}();\n")  # Example: identifier.custom_append_method();
    else:
        file.write("{")
        for i in range(len(node.elements)):
            if (i != len(node.elements) - 1):
                write_expression(node.elements[i], file, symbol_table, ntabs)
                file.write(", ")
            else:
                write_expression(node.elements[i], file, symbol_table, ntabs)
        file.write("}")
def write_assignment(node, file, symbol_table, ntabs=0):
    # Helper function to print tabs
    def print_tabs(ntabs, file):
        file.write('\t' * ntabs)

    print_tabs(ntabs, file)
    file.write(f"{node.variable_name} {node.assignment_operators} ")
    
    # Handle the value, which can be an Expression, SpecialFunction, or LetInStatement
    if isinstance(node.value, Expression):
        write_expression(node.value, file, symbol_table, 0)  # Inline expression
    elif isinstance(node.value, SpecialFunction):
        write_special_function(node.value, file, symbol_table, 0)  # Inline special function
    elif isinstance(node.value, LetInStatement):
        write_let_in_statement(node.value, file, symbol_table, 0)  # Inline let-in statement

    file.write(";\n")

def write_let_in_statement(node, file, symbol_table, ntabs=0):
    # Helper function to print tabs
    def print_tabs(ntabs, file):
        file.write('\t' * ntabs)

    print_tabs(ntabs, file)
    
    # Determine the type and write the variable declaration with initialization if present
    file.write(f"{type_map[node.data_type]} {node.variable_name}")
    
    if node.value_or_letin:
        file.write(" = ")
        if isinstance(node.value_or_letin, Term):
            write_term(node.value_or_letin, file, symbol_table, 0)  # Write the term directly
        elif isinstance(node.value_or_letin, Expression):
            write_expression(node.value_or_letin, file, symbol_table, 0)  # Write the expression
        elif isinstance(node.value_or_letin, LetInStatement):
            write_let_in_statement(node.value_or_letin, file, symbol_table, 0)  # Recursively handle nested let-in statements

    file.write(";\n")
    
    # If there's an additional operation to perform with the variable, write that expression
    if node.operation:
        print_tabs(ntabs, file)
        file.write(f"{node.variable_name} = ")  # Assuming the operation modifies the variable
        write_expression(node.operation, file, symbol_table, 0)
        file.write(";\n")


def write_unary_statement(node, file, symbol_table, ntabs=0,inline=False):
    # Helper function to print tabs

    print_tabs(ntabs, file)
    # Handling both pre and post unary operators
    if node.pre_unary_operator:
        file.write(f"{node.pre_unary_operator}")
    file.write(f"{node.value}")
    if node.post_unary_operator:
        file.write(f"{node.post_unary_operator}")
    if not inline:
        file.write(";\n")


def write_variable_declaration(declaration, file, symbol_table, ntabs=0):
    print_tabs(ntabs, file)
    
    # Splitting the data_type to extract mutability and actual type
    if declaration.data_type == "list" or declaration.data_type == "tup":
        dt = declaration.data_type
        mut = "None"
    else:
        mut, dt = declaration.data_type.split()
    if mut == "fix":
        var_type = f"const {type_map[dt]}"
    else:
        var_type = f"{type_map[dt]}"

    # Writing the variable declaration part
    if declaration.size_array:
        file.write(f"{var_type} {declaration.variable_name}[{declaration.size_array}]")  # Array type declaration
    else:
        file.write(f"{var_type} {declaration.variable_name}")  # Simple variable declaration

    # If there is an initialization expression
    if declaration.equal_to:
        file.write(" = ")
        if isinstance(declaration.equal_to, ListAppendTail):
            write_list_append_tail(declaration.equal_to, file, symbol_table, ntabs)
        
        else:
            for item in declaration.equal_to:
                if isinstance(item, Term):
                    write_term(item, file, symbol_table, ntabs)  # Direct writing of a term
                elif isinstance(item, BinaryOperator):
                    if item.operator:  # Check if operator is not None
                        file.write(f" {item.operator} ")
                elif isinstance(item, Expression):
                    write_expression(item, file, symbol_table, ntabs)  # Recursive handling of expressions
                elif item is None:
                    continue  # Ignore None items in the initialization list

    file.write(";\n")  # End the statement with a semicolon


def write_expression(expression, file, symbol_table, ntabs=0):
    if expression.__class__.__name__ == "SpecialFunction":
        write_special_function(expression, file, symbol_table, ntabs)
    else:
        if expression.operator_if_exists:
            file.write(f" {expression.operator_if_exists} ")
            # If there's an operator, it's a complex expression potentially with multiple terms
            for i, term in enumerate(expression.terms):
                if isinstance(term, Expression):
                    write_expression(term, file, symbol_table, ntabs)  # Recursively handle nested expressions
                elif isinstance(term, Term):
                    write_term(term, file, symbol_table, ntabs)  # Handle terms directly
                elif term and i < len(expression.terms) - 1:
                    file.write(f" {expression.operator_if_exists} ")  # Add operator between terms
        else:
            # Handle simple or unary expressions
            if expression.terms is not None:
                for term in expression.terms:
                    if isinstance(term, Expression):
                        write_expression(term, file, symbol_table, ntabs)  # Recursively handle nested expressions
                    elif isinstance(term, Term):
                        write_term(term, file, symbol_table, ntabs)  # Handle terms directly



def write_term(term, file, symbol_table, ntabs=0):
    if term.value is not None:
        if type(term.value) == int:
            file.write(f"{term.value}")
        elif term.value == True:
            file.write("true")
        elif term.value == False:
            file.write("false")
        elif type(term.value) == str:
            file.write(f'"{term.value}"')
        else:
            print(term.value)
            file.write(f"{term.value}")
    elif term.pre_unary_operator:
        file.write(f"{term.pre_unary_operator}")
    elif term.identifier:
        file.write(f"{term.identifier}")
        if term.expression and term.expression.terms:
            file.write("[")
            write_expression(term.expression, file, symbol_table, ntabs)
            file.write("]")
    elif term.expression:
        write_expression(term.expression, file, symbol_table, ntabs)
    elif term.post_unary_operator:
        file.write(f"{term.post_unary_operator}")

def write_function_definition(node, file, symbol_table, ntabs=0):
    # Helper function to print tabs
    def print_tabs(ntabs, file):
        file.write('\t' * ntabs)

    print_tabs(ntabs, file)
    
    # Start by writing the function return type and name
    file.write(f"{type_map[node.function_type]} {node.function_name}(")
    
    # Write parameters
    if node.parameters:
        params = []
        for param in node.parameters:
            if(param.data_type == "list"):
                param_type = f"std::vector"
            else:
                param_mut, param_dt = param.data_type.split()
                if param_mut == "fix":
                    param_type = f"const {type_map[param_dt]}"
                else:
                    param_type = f"{type_map[param_dt]}"

            if param.array_size:
                params.append(f"{param_type} {param.parameter_name}[{param.array_size}]")
            else:
                params.append(f"{param_type} {param.parameter_name}")
        file.write(", ".join(params))
    file.write(") {\n")
    
    # Delegate the function body writing to the write_function_block
    write_function_block(node.function_block, file, symbol_table, ntabs + 1)
    
    # Close function
    print_tabs(ntabs, file)
    file.write("}\n")


def write_function_block(node, file, symbol_table, ntabs=0):
    # Helper function to print tabs

    # Write each statement in the function block
    for statement in node.statements:
        write_code_main(statement, file, symbol_table, ntabs)

    # Handle the return value if present
    if node.return_value:
        print_tabs(ntabs, file)
        file.write("return ")
        if isinstance(node.return_value, Expression):
            if node.return_value.operator_if_exists is None and node.return_value.terms is None:
                print_tabs(ntabs, file)
            else:
                write_expression(node.return_value, file, symbol_table, ntabs)
        elif isinstance(node.return_value, FunctionCall):
            write_function_call(node.return_value, file, symbol_table, ntabs)
        file.write(";\n")
    else:
        print_tabs(ntabs, file)
        file.write("return;\n")




def write_special_function(node, file, symbol_table, ntabs=0):
    # Helper function to print tabs
    def print_tabs(ntabs, file):
        file.write('\t' * ntabs)

    print_tabs(ntabs, file)

    # Handle different types of special function attributes
    if node.num_literal_start is not None and node.num_literal_end is not None:
        file.write(f"for (int {node.identifier} = {node.num_literal_start}; {node.identifier} <= {node.num_literal_end}; {node.identifier}++) {{\n")
        print_tabs(ntabs + 1, file)
        file.write("// Loop body (if applicable)\n")
        print_tabs(ntabs, file)
        file.write("}\n")
    elif node.length is not None:
        file.write(f"int {node.identifier}_length = sizeof({node.identifier}) / sizeof({node.identifier}[0]);\n")
    elif node.head is not None:
        file.write(f"auto {node.identifier}_head = {node.identifier}[0];\n")
    elif node.isempty is not None:
        file.write(f"bool {node.identifier}_isempty = ({node.identifier}.empty());\n")
    
    # Handle function call if it exists
    elif node.function_call:
        print("Function call found")
        write_function_call(node.function_call, file, symbol_table, ntabs)
 

def write_function_call(node, file, symbol_table, ntabs=0):
    print("Function call found")
    print_tabs(ntabs, file)
    file.write(f"{node.function_name}(")  # Write the function name and opening parenthesis

    # Iterate over each argument in the function call
    for i, arg in enumerate(node.arguments):
        if isinstance(arg, Expression):
            write_expression(arg, file, symbol_table, ntabs)  # Write the expression handling
        elif isinstance(arg, Term):
            write_term(arg, file, symbol_table, ntabs)  # Direct term handling

        if i < len(node.arguments) - 1:
            file.write(", ")  # Add a comma between arguments

    file.write(")")  # Close the function call with a parenthesis and semicolon

def write_conditional_statement(node, file, symbol_table, ntabs=0):

    print_tabs(1, file)
    file.write("if (")
    write_conditional_argument(node.conditional_argument, file, symbol_table, ntabs)  # Updated to use new function
    file.write(") {\n")
    write_block(node.conditional_block, file, symbol_table, ntabs + 1)  # Updated to use new function
    print_tabs(ntabs, file)
    file.write("}\n")

    # Handle additional else-if blocks using write_other_block function
    if node.other_blocks:
        for other in node.other_blocks:
            write_other_block(other, file, symbol_table, ntabs)  # Updated to use new function

    # Handle the optional else block using write_otherwise_block function
    if node.otherwise_block:
        write_otherwise_block(node.otherwise_block, file, symbol_table, ntabs)  # Updated to use new function

def write_conditional_argument(node, file, symbol_table, ntabs=0):

    if node.is_special:
        write_special_function(node.is_special, file, symbol_table, ntabs)
    if node.comparison_operator:
        file.write(f" {node.comparison_operator} ")
    write_expression(node.expression, file, symbol_table, ntabs)

def write_block(node, file, symbol_table, ntabs=0):
    for statement in node.statements:
        write_code_main(statement, file, symbol_table, ntabs)

def write_other_block(node, file, symbol_table, ntabs=0):

    print_tabs(ntabs, file)
    file.write("else if (")

    # Assume that node.condition is always a ConditionalArgument, use the existing function to handle it
    write_conditional_argument(node.condition, file, symbol_table, ntabs)

    file.write(") {\n")
    write_block(node.conditional_block, file, symbol_table, ntabs + 1)
    print_tabs(ntabs, file)
    file.write("}\n")


def write_otherwise_block(node, file, symbol_table, ntabs=0):

    print_tabs(ntabs, file)
    file.write("else {\n")
    write_block(node.conditional_block, file, symbol_table, ntabs + 1)
    print_tabs(ntabs, file)
    file.write("}\n")

input_filename = sys.argv[1]

def print_tabs(ntabs, file):
    file.write('\t' * ntabs)

def generate_cpp_code(ast):
    rich.print(ast)
    output_filename = os.path.splitext(os.path.basename(input_filename))[0] + ".cpp"
    symbol_table = SymTable
    print("Generating code in C++")
    print(symbol_table)
    with open(output_filename, 'w') as file:
        file.write("#include <iostream>\n\n")
        file.write("#include <vector>\n")
        file.write("using namespace std;\n\n")
  
        file.write("extern \"C\" {\n")
         # First, write all function definitions from the AST
        if hasattr(ast, 'function_defs') and ast.function_defs:
            for func_def in ast.function_defs:
                write_code_main(func_def, file, symbol_table, 0)
                file.write("\n")  # Add a newline for better separation between function definitions
        file.write("}\n")
        # Then, write the main function
        # if hasattr(ast, 'main_function'):
        #     write_code_main(ast.main_function, file, symbol_table, 0)

        print("C++ code generation complete. Code written to:", output_filename)

import subprocess

semantic_analyzer = SemanticAnalyzer()
ast, message = semantic_analyzer.analyze(ast)
# ast = semantic_analyzer.analyze(ast)
# Assuming 'ast' is your Abstract Syntax Tree instance

if __name__ == '__main__':
    if (message == "Semantic analysis completed successfully.") :
        print("AST is semantically correct. Generating code.")
        generate_cpp_code(ast)
    else:
        print(message)
        print("AST is not semantically correct. Skipping code generation.")