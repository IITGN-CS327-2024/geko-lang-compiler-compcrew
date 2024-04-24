from ast_final import *
from ast_classes import *
# from sem_combine import *
from sem_shreya_copy import *
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
    
    elif node.__class__.__name__ == "Expression":
        write_expression(node, file, symbol_table, ntabs)
    
    elif node.__class__.__name__ == "Term":
        write_term(node, file, symbol_table, ntabs)
        file.write(";\n")  # Assuming terms outside expressions need to be terminated with a semicolon
    
    elif node.__class__.__name__ == "Assignment":
        print_tabs(ntabs, file)
        file.write(f"{node.variable_name} {node.assignment_operators} ")
        if isinstance(node.value, (Term, Expression)):
            write_code_main(node.value, file, symbol_table, ntabs)  # This should handle both Term and Expression cases
        file.write(";\n")



    elif node.__class__.__name__ == "ShowStatement":
        print_tabs(ntabs, file)
        file.write("std::cout << ")
        for i, expr in enumerate(node.expressions):
            write_expression(expr, file, symbol_table, ntabs)
            if i < len(node.expressions) - 1:
                file.write(" << ' ' << ")
        file.write(" << std::endl;\n")

    elif node.__class__.__name__ == "LoopStatement":
        print_tabs(ntabs, file)
        loop_header = f"for ({write_variable_declaration(node.declaration, symbol_table)}; {write_expression(node.condition, symbol_table)}; {write_assignment(node.updation, symbol_table)})"
        file.write(loop_header + " {\n")
        write_code_main(node.block, file, symbol_table, ntabs + 1)
        print_tabs(ntabs, file)
        file.write("}\n")

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
        print_tabs(ntabs, file)
        file.write("if (")
        file.write(write_expression(node.conditional_argument.expression, symbol_table))
        file.write(") {\n")
        write_code_main(node.conditional_block, file, symbol_table, ntabs + 1)
        for other in node.other_blocks:
            print_tabs(ntabs, file)
            file.write("else if (")
            file.write(write_expression(other.condition, symbol_table))
            file.write(") {\n")
            write_code_main(other.conditional_block, file, symbol_table, ntabs + 1)
        if node.otherwise_block:
            print_tabs(ntabs, file)
            file.write("else {\n")
            write_code_main(node.otherwise_block.conditional_block, file, symbol_table, ntabs + 1)
        print_tabs(ntabs, file)
        file.write("}\n")

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


def write_variable_declaration(declaration, file, symbol_table, ntabs=0):
    print_tabs(ntabs, file)
    
    # Splitting the data_type to extract mutability and actual type
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
            for term in expression.terms:
                if isinstance(term, Expression):
                    write_expression(term, file, symbol_table, ntabs)  # Recursively handle nested expressions
                elif isinstance(term, Term):
                    write_term(term, file, symbol_table, ntabs)  # Handle terms directly



def write_term(term, file, symbol_table, ntabs=0):
    if term.value is not None:
        if term.value == True:
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
    elif term.expression:
        write_expression(term.expression, file, symbol_table, ntabs)
    elif term.post_unary_operator:
        file.write(f"{term.post_unary_operator}")

def write_function_definition(node, file, symbol_table, ntabs=0):

    print_tabs(ntabs, file)
    
    # Start by writing the function return type and name
    file.write(f"{type_map[node.function_type]} {node.function_name}(")
    
    # Write parameters
    if node.parameters:
        params = []
        for param in node.parameters:
            param_mut, param_dt = param.data_type.split()
            if param_mut == "fix":
                param_type = f"const {type_map[param_dt]}"
            else:
                param_type = f"{type_map[param_dt]}"

            if param.array_size:
                params.append(f"{type_map[param_type]} {param.parameter_name}[{param.array_size}]")
            else:
                params.append(f"{type_map[param_type]} {param.parameter_name}")
        file.write(", ".join(params))
    file.write(") {\n")
    
    # Write function body
    for statement in node.function_block.statements:
        write_code_main(statement, file, symbol_table, ntabs + 1)
    
    # Handle return value
    if node.function_block.return_value:
        print_tabs(ntabs + 1, file)
        if isinstance(node.function_block.return_value, Expression):
            file.write("return ")
            write_expression(node.function_block.return_value, file, symbol_table, ntabs + 1)
            file.write(";\n")
        elif isinstance(node.function_block.return_value, FunctionCall):
            file.write("return ")
            write_function_call(node.function_block.return_value, file, symbol_table, ntabs + 1)
            file.write(";\n")
    
    # Close function
    print_tabs(ntabs, file)
    file.write("}\n")



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
        # file.write(f"{node.function_call.function_name}(")
        # for i, arg in enumerate(node.function_call.arguments):
        #     write_expression(arg, file, symbol_table, ntabs)
        #     if i < len(node.function_call.arguments) - 1:
        #         file.write(", ")
        # file.write(");\n")

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

    file.write(");\n")  # Close the function call with a parenthesis and semicolon


def print_tabs(ntabs, file):
    file.write('\t' * ntabs)

def generate_cpp_code(ast):
    rich.print(ast)
    output_filename = "generated_code.cpp"
    symbol_table = SymTable
    print("Generating code in C++")
    print(symbol_table)
    with open(output_filename, 'w') as file:
        file.write("#include <iostream>\n\n")
        file.write("using namespace std;\n\n")
         # First, write all function definitions from the AST
        if hasattr(ast, 'function_defs') and ast.function_defs:
            for func_def in ast.function_defs:
                write_code_main(func_def, file, symbol_table, 0)
                file.write("\n")  # Add a newline for better separation between function definitions

        # Then, write the main function
        if hasattr(ast, 'main_function'):
            write_code_main(ast.main_function, file, symbol_table, 0)

        print("C++ code generation complete. Code written to:", output_filename)

import subprocess

semantic_analyzer = SemanticAnalyzer()
ast, message = semantic_analyzer.analyze(ast)
# Assuming 'ast' is your Abstract Syntax Tree instance
if __name__ == '__main__':
    if (message == "Semantic analysis completed successfully.") :
        print("AST is semantically correct. Generating code.")
        generate_cpp_code(ast)
    else:
        print("AST is not semantically correct. Skipping code generation.")
    # subprocess.run(["g++", "generated_code.cpp", "-o", "gp"])
    # subprocess.run(["./gp"])
