from ast_final import *
from ast_classes import *
from sem_combine import *
import rich
# Code Generation
type_map = {
    'num': 'int',
    'str': 'str',  # Python doesn't have char*, strings are used instead
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
        print_tabs(ntabs, file)
        mut, dt = node.data_type.split()
        if mut == "fix":
            var_type = f"const {type_map[dt]}"
        else:
            var_type = f"{type_map[dt]}"
        file.write(f"{var_type} {node.variable_name} = ")
        if node.equal_to:
            for j in node.equal_to:
                if isinstance(j, Term):
                    write_term(j, file, symbol_table, ntabs)
                elif isinstance(j, Expression):
                    write_expression(j, file, symbol_table, ntabs)
        file.write(";\n")
    
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


    else:
        # Handling other nodes generically
        print_tabs(ntabs, file)
        file.write("int main() {\n")
        for child in node.statements:
            write_code_main(child, file, symbol_table, ntabs + 1)
        file.write("\treturn 0;\n}\n")



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
