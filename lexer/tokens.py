from lexer import *
import sys

# Function to read the code from the .geko file
def read_geko_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if len(sys.argv) != 2:
    print("Usage: python3 lexer.py <geko_file>")
    sys.exit(1)

file_path = sys.argv[1]
geko_code = read_geko_file(file_path)

tokens = lexer(geko_code)
print_table(tokens)