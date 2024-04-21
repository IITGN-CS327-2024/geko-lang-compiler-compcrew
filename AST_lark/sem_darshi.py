from ast_final import *
from ast_classes import *
import rich
class SemanticError(Exception):
    pass

dict_of_types = { 
    'int':'num',
    'str':'str',
    'list':'list',
    'tuple':'tup',
    'bool':'flag'
}
dict_types = { 
    'num':'int',
    'str':'str',
    'list':'list',
    'tup':'tup',
    'flag':'bool'
}
                
class SemanticAnalyzer:
    def __init__(self):
        # Initializes the symbol table stack with a global scope
        self.symbol_table = {}
        self.scopes = []

    # def enter_scope(self):
    #     # Enter a new scope by adding a scope to the stack
    #     self.symbol_table.append({})
    def enter_scope(self, scp):
        # Enter a new scope by adding a scope to the stack
        self.scopes.append(scp)
        self.symbol_table[scp] = {}

    def exit_scope(self):
        # Exit a scope by removing the most recently entered scope
        if len(self.symbol_table) >= 1:
            self.scopes.pop()
        else:
            raise SemanticError("Trying to exit the global scope")

    def declare_variable(self, name, data_type, mutability, size = None):
        if name in self.scopes[-1]:
            raise SemanticError(f"Variable '{name}' already declared in this scope")
        if size is not None:
            self.symbol_table[self.scopes[-1]][name] = {'type': data_type, 'mutability': mutability, 'size': size}
        else:  
            self.symbol_table[self.scopes[-1]][name] = {'type': data_type, 'mutability': mutability}
        print(self.scopes)

    def check_variable_declared(self, name):
        # Check if a variable is declared in any accessible scope
        if name in self.symbol_table[self.scopes[-1]]:
            print(self.scopes[-1])
            return self.symbol_table[self.scopes[-1]][name]
        elif 'parameters' in  self.symbol_table[self.scopes[-1]]:
            if name in self.symbol_table[self.scopes[-1]]['parameters']:
                print("found in parameters")
                print(name, self.symbol_table[self.scopes[-1]]['parameters'][name])
                return self.symbol_table[self.scopes[-1]]['parameters'][name]
        raise SemanticError(f"Variable '{name}' not declared")

    def type_of_expression(self, expression):
        if isinstance(expression, str):
            if expression.startswith('~') and expression.endswith('~'):
                return 'string'
            else:
                # Handling direct variable name references
                var_info = self.check_variable_declared(expression)
                return var_info['type']
        elif isinstance(expression, UnaryOperator):
            operand_type = self.type_of_expression(expression.operand)
            return operand_type
        # elif isinstance(expression, Term):
        elif expression.__class__.__name__ == 'Term':
            if expression.value:
                print(type(expression.value))
                return type(expression.value).__name__
            if expression.expression:
                return self.type_of_expression(expression.expression)
            if expression.identifier:
                var_info = self.check_variable_declared(expression.identifier)
                print("var_info:",var_info)
                if (type(var_info) is not dict) and (var_info in dict_types):
                    return dict_types[var_info]
                else:
                    return dict_types[var_info['type']]
            # else:
            #     return self.type_of_expression(expression.value)
        elif expression.__class__.__name__ == "Expression":
            expr_type_list = []
            for term in expression.terms:
                if term:
                    temp = self.type_of_expression(term)
                    expr_type_list.append(temp)
            exp_typ = expr_type_list[0]
            for i in expr_type_list:
                if (i != exp_typ):
                    exp_typ = "Undetermined"
                    break
            return exp_typ
        elif isinstance(expression, BinaryOperator):
            # Handle binary operations like +, -, *, etc.
            # You need to determine the resulting type based on the operation
            # This is a simplified example and might need adjustment based on your language's rules
            left_type = self.type_of_expression(expression.left)
            right_type = self.type_of_expression(expression.right)
            # Assuming for simplicity that the result type is the same as the operand type
            return left_type if left_type == right_type else None
        elif isinstance(expression, (int, float)):
            return 'int'
    # Add more comprehensive handling here based on your expression AST node types

    # You should add more comprehensive handling here based on your expression AST node types
    def visit_ListAppendTail(self, node):
        print('ListAppendTail')

        if node.tail is not None:
            var_info = self.check_variable_declared(node.identifier)
            print('var_info:',var_info)
            return (None,[])
        
        if node.append is not None:
            var_info = self.check_variable_declared(node.identifier)
            print('var_info:',var_info)
            return (None,[])

        else:        
            type_list = []
            length = len(node.elements)
            count = 0
            for i in node.elements:
                print("#########BLAHBLAHBLAH########################\n",i)
                if (isinstance(i, Expression)):
                        print(1)
                        if (isinstance(i.terms[1], Expression)):
                            print(2)
                            print(i)
                            ex_type = self.type_of_expression(i)
                            print()
                            print(ex_type)
                            if ex_type == "Undetermined":
                                raise SemanticError(f"Type mismatch in the index:{count+1}")
                            type_list.append(ex_type)
                        expr_type = self.type_of_expression(i.terms[0])
                        type_list.append(expr_type)
                        print(type_list)
                        count += 1
            return (length, type_list)

    def visit_VariableDeclaration(self, node):
        # node.data_type might contain "None num", "let num", or "fix num"
        if (node.data_type == 'list' or node.data_type == 'tup'):
            mutability =  None
            type_name = node.data_type
            print(mutability)
            print(type_name)
            (length_list, type_list_list) = self.visit(node.equal_to)
            if (length_list != None and len(type_list_list)!=0):
                print("Bhai yaha aaya")     
                size = length_list
                self.declare_variable(node.variable_name, type_name, mutability,size)

        elif node.size_array: #when the variable is an array
            print('array')
            if isinstance(node.size_array, int):
                if node.size_array < 0:
                    raise SemanticError(f"Array size must be a positive integer")
            else:
                raise SemanticError(f"Array size must be an integer")
            size = node.size_array
            
            # var_info = self.check_variable_declared(node.variable_name)

            print(node.equal_to)
            (length_arr, type_list_arr) = self.visit(node.equal_to)

            #pehle ye check karlo ki elements ki length ke size ke equal hai ya nahi
            if (length_arr != size):
                raise SemanticError(f"Size of array does not match the number of elements")

            #phir ek ek element ke type check karo
            for i in range(len(type_list_arr)):
                if type_list_arr[i] in dict_of_types.keys(): #like int to num conversion
                    type_list_arr[i] = dict_of_types[type_list_arr[i]]
                if type_list_arr[i] != type_name:
                    raise SemanticError(f"Type mismatch: variable '{node.variable_name}' declared as '{type_name}' but assigned '{type_list_arr[i]}'")
            # phir us variable ko symbol table me store karo 
            self.declare_variable(node.variable_name, type_name, mutability,size)
            
        else:
            mutability, type_name = node.data_type.split()
            print(mutability)
            print(type_name)
            test_lst = []
            if (node.equal_to):
                for i in node.equal_to[:-1]: #-1 is for epsilon
                    if (isinstance(i, Term)):
                        print(1)
                        expr_type = self.type_of_expression(i)
                        test_lst.append(expr_type)
                # change expr_type according to dict_of_types
                print('###################################')
                print(test_lst)
                test_lst = flatten_list(test_lst)
                print(test_lst)
                print('###################################')
                if  len(test_lst) > 0:
                    var_val_tp = test_lst[0]
                    for i in test_lst:
                        print("i is:", i)
                        if i != var_val_tp:
                            var_val_tp = "Undetermined"
                            break
                    if ((var_val_tp != "Undetermined") and (var_val_tp in dict_of_types.keys())):
                        var_val_tp = dict_of_types[var_val_tp]
                # for i in range(len(test_lst)):
                #     # print(j)
                #     print(dict_of_types['int'])
                #     print(2)
                #     # if j in dict_of_types:
                #     #     j = dict_of_types[j]
                #     # if test_lst[i] in dict_of_types.keys():
                #     #     test_lst[i] = dict_of_types[test_lst[i]]
                #     # if test_lst[i] != type_name:
                    if var_val_tp != type_name:
                        raise SemanticError(f"Type mismatch: variable '{node.variable_name}' declared as '{type_name}' but assigned '{var_val_tp}'")
                print(test_lst)
            self.declare_variable(node.variable_name, type_name, mutability)

    def visit_UnaryStatement(self, node):
        self.check_variable_declared(node.value)
    
    def visit_ShowStatement(self, node):
        for stmt in node.expressions:
            temp_type = self.type_of_expression(stmt)
            if temp_type == "Undetermined":
                raise SemanticError(f"Type mismatch in the expression in show statement")

    def visit_Assignment(self, node):
        var_info = self.check_variable_declared(node.variable_name)
        expr_type = self.type_of_expression(node.value)
        # print('before ka before:',expr_type)
        # expr_type = flatten_list(expr_type)
        # for i in range(len(expr_type)):
            # print('before ka before:',expr_type[i])
        if expr_type in dict_of_types.keys():
            print('before:', expr_type)
            expr_type = dict_of_types[expr_type]
        tp = expr_type
        print('expr_type:',expr_type)
        print('tp:',tp)
        if tp != var_info['type']:
            raise SemanticError(f"Type mismatch: variable '{node.variable_name}' expected '{var_info['type']}' but got '{tp}'")
        if var_info['mutability'] == 'fix':
            raise SemanticError(f"Cannot assign to constant variable '{node.variable_name}'")
        
    def visit_ConditionalStatement(self, node):
        self.enter_scope()
        self.visit(node.conditional_argument.expression)
        for statement in node.conditional_block.statements:
            self.visit(statement)
        self.exit_scope()

    def visit(self, node):
        # General visit method that calls specific methods based on node type
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # Generic visit method for all unhandled node types
        raise NotImplementedError(f"No visit method defined for {type(node).__name__}")

    def visit_Program(self, node):
        # Visit the main function and any function definitions
        if len(node.function_defs) > 0:
            for function_def in node.function_defs:
                self.visit(function_def)
        self.visit(node.main_function)
        # for func in node.function_defs:
        #     self.visit(func)

    def visit_MainFunc(self, node):
        self.enter_scope("main")
        for statement in node.statements:
            if statement:
                self.visit(statement)
        rich.print(self.symbol_table)
        self.exit_scope()

    def visit_FunctionDef(self, node):
        self.enter_scope(node.function_name)
        self.symbol_table[node.function_name]['parameters'] = {
            'return_value': node.function_type
        }
        # self.symbol_table[node.function_name]['return_type'] = {'data_type': 'int'}
        for param in node.parameters:
            self.visit(param)
        for statement in node.function_block.statements:
            self.visit(statement)
        self.exit_scope()

    def visit_Parameter(self,node):
        fix_let, dt = node.data_type.split()
        # print(fix_let)
        param = node.parameter_name
        if fix_let != 'None':
            raise SemanticError(f"Parameter datatype in the function {self.scopes[-1]} can't have {fix_let} keyword.")
        else:
            self.symbol_table[self.scopes[-1]]['parameters'][param] = (dt,node.array_size) if node.array_size else dt
            self.symbol_table[self.scopes[-1]]['parameters'][param] = dt
            # if node.array_size:
            #     self.symbol_table[self.scopes[-1]][] =
        # print("\n\nvisited\n\n")
    
    def visit_Expression(self, node):
        for term in node.terms:
            self.visit(term)
    
    # Not used
    def visit_Term(self, node):
        if node.identifier:
            self.check_variable_declared(node.identifier)

    def visit_NoneType(self, node):
        pass

analyzer = SemanticAnalyzer()
try:
    analyzer.visit(ast)
    print("Semantic analysis completed successfully.")
except SemanticError as e:
    print(f"Semantic error: {e}")
