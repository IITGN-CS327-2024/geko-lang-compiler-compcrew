from ast_final import *
from ast_classes import *
from sem_combine import *
import rich
# Code Generation
type_map = {
    'num': 'int',
    'str': 'string',  # Python doesn't have char*, strings are used instead
    'list': 'list',   # Python list for any list type
    'tup': 'tuple', # Python tuple for tuple types
    'flag': 'bool', # Python's bool for flag
    'fix': 'const'
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
        write_code_main(ast.main_function, file, symbol_table, 0)

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
