from ast_final import *
from ast_classes import *
import rich
class SemanticError(Exception):
    pass

SymTable = {}

dict_of_types = { 
    'int':'num',
    'str':'str',
    'list':'list',
    'tuple':'tup',
    'bool':'flag',
    'void':'void'
}
dict_types = { 
    'num':'int',
    'str':'str',
    'list':'list',
    'tup':'tup',
    'flag':'bool',
    'void':'void'
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
        print(self.symbol_table[self.scopes[-1]])
        print(self.scopes[-1])
        if name in self.symbol_table[self.scopes[-1]]:
            raise SemanticError(f"Variable '{name}' already declared in this scope")
        if size is not None:
            self.symbol_table[self.scopes[-1]][name] = {'type': data_type, 'mutability': mutability, 'size': size}
        else:  
            self.symbol_table[self.scopes[-1]][name] = {'type': data_type, 'mutability': mutability}
        # print(self.scopes)

    def declare_list(self, name, data_type, mutability,size, list_for_elements):
        # Declare a variable in the current scope
        if name in self.symbol_table[self.scopes[-1]]:
            raise SemanticError(f"Variable '{name}' already declared in this scope")
        self.symbol_table[self.scopes[-1]][name] = {'type': data_type, 'mutability': mutability, 'size': size, 'elements_type': list_for_elements}
        # print(self.scopes)
    
    def declare_string(self, name, data_type, mutability, length):
        # Declare a variable in the current scope
        if name in self.symbol_table[self.scopes[-1]]:
            raise SemanticError(f"Variable '{name}' already declared in this scope")
        self.symbol_table[self.scopes[-1]][name] = {'type': data_type, 'mutability': mutability, 'length': length}
        # print(self.scopes)

    def check_variable_declared(self, name):
        # Check if a variable is declared in any accessible scope
        # print(self.scopes[-1],"\nIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        if name in self.symbol_table[self.scopes[-1]]:
            print(self.scopes[-1])
            # print(self.scopes[-1])
            return self.symbol_table[self.scopes[-1]][name]
        elif self.scopes[-1] == 'Block':
            for i in range(len(self.scopes)-2,-1,-1):
                if name in self.symbol_table[self.scopes[i]]:
                    print(self.scopes[i])
                    return self.symbol_table[self.scopes[i]][name]
        elif 'parameters' in  self.symbol_table[self.scopes[-1]]:
            if name in self.symbol_table[self.scopes[-1]]['parameters']:
                print("found in parameters")
                print(name, self.symbol_table[self.scopes[-1]]['parameters'][name])
                return self.symbol_table[self.scopes[-1]]['parameters'][name]
        raise SemanticError(f"Variable '{name}' not declared")

    def type_of_expression(self, expression):
        if isinstance(expression, str):
            if expression.startswith('~') and expression.endswith('~'):
                return 'str'
            else:
                # Handling direct variable name references
                var_info = self.check_variable_declared(expression)
                return var_info['type']
        elif isinstance(expression, UnaryOperator):
            operand_type = self.type_of_expression(expression.operand)
            return operand_type
        # elif isinstance(expression, Term):
        elif expression.__class__.__name__ == 'Term':
            #to handle b[2] on RHS
            if expression.identifier is not None and expression.expression is not None:
                var_info = self.check_variable_declared(expression.identifier)
                if len(var_info) == 2:
                    raise SemanticError(f"Variable '{expression.identifier}' is not an array/list/tuple")
                if var_info['size'] == 0:
                    raise SemanticError(f"Variable '{expression.identifier}' is an empty list/tuple")
                if expression.expression.terms[0].value >= var_info['size']:
                    raise SemanticError(f"Index out of bounds")
                return var_info['type']
            if expression.value is not None:
                print('value:',expression.value)
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
        elif isinstance (expression, SpecialFunction):
            return self.visit(expression)
            # if expression.function_call:
            #     return self.visit(expression.function_call)
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

    # def visit_FunctionCall(self, node):
    #     if node.function_name not in 

    # You should add more comprehensive handling here based on your expression AST node types

    def visit_SpecialFunction(self, node):
        print('SpecialFunction')
        #array, list, tup teeno ke liye ek saath handle karega
        typ = None
        if node.length and node.identifier:
            print('length')
            var_info = self.check_variable_declared(node.identifier)
            print('var_info',var_info)
            if len(var_info) == 2:
                raise SemanticError(f"Variable '{node.identifier}' is not an array/list/tuple")
            typ = 'int'
            return (typ,var_info['size'])
        
        elif node.head and node.identifier:
            print('head')
            var_info = self.check_variable_declared(node.identifier)
            if var_info['size'] == 0:
                raise SemanticError(f"Variable '{node.identifier}' is an empty list/tuple")
            print('var_info',var_info)
            if len(var_info) == 2:
                raise SemanticError(f"Variable '{node.identifier}' is not an array/list/tuple")
        
            typ = var_info['elements_type'][0]
            return (typ,var_info['size'])
        
        elif node.isempty and node.identifier:
            print('isempty')
            var_info = self.check_variable_declared(node.identifier)
            if len(var_info) == 2:
                raise SemanticError(f"Variable '{node.identifier}' is not an array/list/tuple")
            if var_info['size'] == 0:
                return ('flag',0)
            return ('flag',1)
        
        elif node.function_call:
            func_call_list = self.visit(node.function_call)
            return func_call_list
        
        else: #to handle slicing
            print('slicing')
            var_info = self.check_variable_declared(node.identifier)
            if var_info['type'] != 'str':
                raise SemanticError(f"Variable '{node.identifier}' is not a string")
            if node.num_literal_start >= node.num_literal_end:
                raise SemanticError(f"Invalid slicing range") 
            if node.num_literal_start < 0 or node.num_literal_end < 0:
                raise SemanticError(f"Negative slicing range")
            if node.num_literal_start >= var_info['length'] or node.num_literal_end > var_info['length']:
                raise SemanticError(f"Index out of bounds")
            return ('str',node.num_literal_end - node.num_literal_start)
    
    # 'add': {'parameters': {'return_value': 'num', 'x': 'num', 'y': 'num'}, 'sum': {'type': 'num', 'mutability': 'None'}}    
    def visit_FunctionCall(self,node):
        if node.function_name not in self.symbol_table:
            raise SemanticError("Undefined function '%s'" % node.function_name)
        else:
            param_list = self.symbol_table[node.function_name]['params'].values()
            return param_list
            

    def visit_ListAppendTail(self, node):
        print('ListAppendTail')

        if node.tail is not None:
            var_info = self.check_variable_declared(node.identifier)
            if (len(var_info) <= 3):
                raise SemanticError(f"Variable '{node.identifier}' is not a list")
            print('var_info:',var_info)
            return (None,[])
        
        if node.append is not None:
            var_info = self.check_variable_declared(node.identifier)
            if (len(var_info) <= 3):
                raise SemanticError(f"Variable '{node.identifier}' is not a list")
            print('var_info:',var_info)
            return (None,[])

        else:        
            type_list = []
            length = len(node.elements)
            count = 0
            for i in node.elements:
                print(i)
                if (isinstance(i, Expression)) and (i.terms is not None):
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
                elif (i.terms is None):
                    type_list = []
                    length = 0
            return (length, type_list)

    def visit_VariableDeclaration(self, node):
        # node.data_type might contain "None num", "let num", or "fix num"

        if (node.data_type == 'list' or node.data_type == 'tup'):
            mutability =  None
            type_name = node.data_type
            print(mutability)
            print(type_name)
            #when the equal_to goes to ListAppendTail
            if node.equal_to is None:
                print('None')
                self.declare_variable(node.variable_name, type_name, mutability)
                return 
            
            elif node.equal_to.__class__.__name__ == "ListAppendTail":
                print('ListAppendTail')
                if node.equal_to.tail is not None or node.equal_to.append is not None:
                    (length_list, type_list_list) = self.visit(node.equal_to)
                    self.declare_list(node.variable_name, type_name, mutability,length_list, type_list_list)
                    return
                
            #to handle empty list, tuple                
            elif node.equal_to.elements[0].terms == None:
                print('empty')
                self.declare_list(node.variable_name, type_name, mutability, 0, [])
                return
            (length_list, type_list_list) = self.visit(node.equal_to)
            self.declare_list(node.variable_name, type_name, mutability, length_list, type_list_list)
            return
        
        elif node.size_array is not None: #when the variable is an array
            print('array')
            mutability, type_name = node.data_type.split()

            if isinstance(node.size_array, int):
                if node.size_array < 0:
                    raise SemanticError(f"Array size must be a positive integer")
            else:
                raise SemanticError(f"Array size must be an integer")
            size = node.size_array
            
            # var_info = self.check_variable_declared(node.variable_name)

            print(node.equal_to)
            if node.equal_to is None:
                self.declare_variable(node.variable_name, type_name, mutability,size)
                return
            (length_arr, type_list_arr) = self.visit(node.equal_to)

            

            if type_list_arr == []:
                self.declare_variable(node.variable_name, type_name, mutability,size)
                return 

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

            #to handle num a = b[2];
            if (node.equal_to is None):
                self.declare_variable(node.variable_name, type_name, mutability)
                return
                # return
            # self.declare_variable(node.variable_name, type_name, mutability)

            #to handle string
            elif (node.equal_to):
                if (type_name == 'str'):
                    length = 0
                    for i in node.equal_to[:-1]:
                        if (isinstance(i, Term)):
                            expr_type = self.type_of_expression(i)
                            if type(expr_type) is tuple:
                                type_str,temp = expr_type
                                test_lst.append(expr_type[0])
                            else:
                                type_str= expr_type
                                test_lst.append(type_str)
                            print(f'expr_type: {expr_type}')
                            if (type_str != 'str'):   
                                raise SemanticError(f"Type mismatch: variable '{node.variable_name}' declared as '{type_name}' but assigned '{type_str}'!!!!")
                            
                            if (i.value is not None):
                                temp = len(i.value)
                            elif i.identifier is not None:
                                temp = self.check_variable_declared(i.identifier)['length']
                            # elif i.expression is not None: #for special function but only slicing
                            #     type_str,temp = expr_type
                            length += temp
                            print(f'value: {i.value}')
                            print(f'length: {length}')
                    
                    self.declare_string(node.variable_name, type_name, mutability,length)
                    return
                else:
                    for i in node.equal_to[:-1]: #-1 is for epsilon
                        print(i)
                        if (isinstance(i, Term)):
                            print(1)
                            if i.expression is not None:
                                if isinstance(i.expression, SpecialFunction) and i.expression.num_literal_start is not None:
                                    if type_name != 'str':
                                        raise SemanticError(f"Type mismatch: variable '{node.variable_name}' declared as '{type_name}' but assigned 'str'")
                            expr_type = self.type_of_expression(i)
                            if type(expr_type) is tuple:
                                type_str,temp = expr_type
                                if type_str in dict_of_types.keys():
                                    type_str = dict_of_types[expr_type[0]]
                                test_lst.append(type_str)
                            else:
                                if expr_type in dict_of_types.keys():
                                    expr_type = dict_of_types[expr_type]
                                test_lst.append(expr_type)
                    # change expr_type according to dict_of_types
                    print('###################################')
                    print(test_lst)
                    test_lst = flatten_list(test_lst)
                    print(test_lst)
                    print('###################################')
                    ################
                    # Darshi is handling special function here
                    ################
                    if  len(test_lst) > 0:
                        var_val_tp = test_lst[0]
                        for i in test_lst:
                            print("i is:", i)
                            if i != var_val_tp:
                                var_val_tp = "Undetermined"
                                break
                        if ((var_val_tp != "Undetermined") and (var_val_tp in dict_of_types.keys())):
                            var_val_tp = dict_of_types[var_val_tp]
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
        print('Assignment')
        print()
        var_info = self.check_variable_declared(node.variable_name) #for variable in LHS
        print('var_info:',var_info)

        if (var_info['type'] == 'tup'):
            raise SemanticError(f"Cannot assign to variable '{node.variable_name}' of type 'tuple'")

        #to handle list,append,tail
        if node.value.__class__.__name__ == "ListAppendTail":
            #to declare array
            if (var_info['type'] is not None):
                (len_arr, type_list_arr) = self.visit(node.value)
                if len_arr != var_info['size']:
                    raise SemanticError(f"Size of array does not match the number of elements")
                for i in range(len(type_list_arr)):
                    if type_list_arr[i] in dict_of_types.keys():
                        type_list_arr[i] = dict_of_types[type_list_arr[i]]
                    if type_list_arr[i] != var_info['type']:
                        raise SemanticError(f"Type mismatch: variable '{node.variable_name}' expected '{var_info['elements_type']}' but got '{type_list_arr[i]}'")
                
            #when declaring list, nothing to check only to store the types of elements in var info
            elif (var_info['type'] == 'list'):
                (len_list, type_list_list) = self.visit(node.value)
                var_info['elements_type'] = type_list_list

            #to handle tail
            elif node.value.tail is not None:
                if (var_info['type'] != 'list'):
                    raise SemanticError(f"Cannot assign to variable '{node.variable_name}'")
    
            #to handle append
            elif node.value.append is not None:
                if (var_info['type'] != 'list'):
                    raise SemanticError(f"Cannot assign to variable '{node.variable_name}'")
                
        else:
            expr_len = 0
            for i in node.value[:-1]:
                if (isinstance(i, Term)):
                    expr_type = self.type_of_expression(i)
                    #to handle cases of length, head, isempty
                    if type(expr_type) is tuple:
                        type_str,temp = expr_type
                        if (i.expression.length is not None):
                            if var_info['type'] != expr_type[0]:
                                raise SemanticError(f"Type mismatch: variable '{node.variable_name}' expected '{var_info['type']}' but got '{expr_type[0]}'")
                        elif (i.expression.head is not None):
                            if type_str in dict_of_types.keys():
                                type_str = dict_of_types[expr_type[0]]
                            if type_str != var_info['type']:
                                raise SemanticError(f"Type mismatch: variable '{node.variable_name}' expected '{var_info['type']}' but got '{expr_type[0]}'")
                        elif (i.expression.isempty is not None):
                            if var_info['type'] != type_str:
                                raise SemanticError(f"Type mismatch: variable '{node.variable_name}' expected '{var_info['type']}' but got '{expr_type[0]}'")
                        #in case of string, slicing is handled here
                        if (type_str == 'str'):
                            expr_len += temp
                    else:
                        type_str= expr_type
                        if (type_str == 'str'):
                            if (i.value is not None):
                                expr_len += len(i.value)
                            elif i.identifier is not None:
                                expr_len += self.check_variable_declared(i.identifier)['length']
                            
                    if type_str in dict_of_types.keys():
                        type_str = dict_of_types[type_str]
                    if type_str != var_info['type']:
                        raise SemanticError(f"Type mismatch: variable '{node.variable_name}' expected '{var_info['type']}' but got '{type_str}'")

                    var_info['length'] = expr_len






                
    def visit_ValueChangeArray(self, node):
    #to handle a[2] = 5 value change array;
        print('ValueChangeArray')
        var_info_lhs = self.check_variable_declared(node.identifier)
        if len(var_info_lhs) == 2:
            raise SemanticError(f"Variable '{node.identifier}' is not an array")
        if var_info_lhs['type'] == 'list':
            raise SemanticError(f"Cannot change element in variable '{node.identifier}' of type 'list'") 
        if var_info_lhs['size'] == 0:
            raise SemanticError(f"Variable '{node.identifier}' is an empty array")
        if var_info_lhs['size'] <= node.index:
            raise SemanticError(f"Index out of bounds")  
        if (node.value.terms[0].expression.__class__.__name__ == "SpecialFunction"):
            (typ,length) = self.visit(node.value.terms[0].expression)
            
            if (node.value.terms[0].expression.length is not None) and var_info_lhs['type'] != typ:
                raise SemanticError(f"Type mismatch: variable '{node.variable_name}' expected '{var_info_lhs['type']}' but got '{typ}'")
            elif (node.value.terms[0].expression.head is not None) and var_info_lhs['type'] != typ:
                if typ in dict_of_types.keys():
                    typ = dict_of_types[typ]
                if typ != var_info_lhs['type']:
                    raise SemanticError(f"Type mismatch: variable '{node.variable_name}' expected '{var_info_lhs['type']}' but got '{typ}'")
            elif (node.value.terms[0].expression.isempty is not None) and var_info_lhs['type'] != type:
                raise SemanticError(f"Type mismatch: variable '{node.variable_name}' expected '{var_info_lhs['type']}' but got '{typ}'")

        if (node.value.terms[0].expression is None):
            if var_info_lhs['type'] != dict_of_types[self.type_of_expression(node.value)]:
                    raise SemanticError(f"Type mismatch: variable '{node.identifier}' expected '{var_info_lhs['type']}' but got '{self.type_of_expression(node.value)}'")



    def visit_ConditionalStatement(self, node):
        # self.enter_scope("Conditional")n``1
        self.visit(node.conditional_argument)
        for statement in node.conditional_block.statements:
            self.type_of_expression(statement)
        if len(node.other_blocks) > 0:
            for other in node.other_blocks:
                self.visit(other)
        self.visit(node.otherwise_block)
        # self.exit_scope()
    
    def visit_OtherBlock(self, node):
        self.visit(node.condition)
        for statement in node.conditional_block.statements:
            self.type_of_expression(statement)
    
    def visit_OtherwiseBlock(self,node):
        for statement in node.conditional_block.statements:
            self.type_of_expression(statement)

    def visit_TryCatchStatement(self, node):
        self.enter_scope("Try")
        for stmt in node.try_block.statements:
            if stmt:
                self.visit(stmt)
        self.symbol_table['Try']['catch'] = node.catch_string
        self.enter_scope("Catch")
        for stmt in node.catch_block.statements:
            if stmt:
                self.visit(stmt)
        
        self.exit_scope()
        self.exit_scope()
    
    def visit_PopStatement(self,node):
        self.symbol_table[self.scopes[-1]]['pop'] = node.string_value

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
                if type(statement) is list:
                    self.visit(statement[0])
                else:
                    self.visit(statement)
        rich.print(self.symbol_table)
        SymTable = self.symbol_table
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
        yield_type = self.type_of_expression(node.function_block.return_value)
        if (dict_of_types[yield_type] != node.function_type):
            raise SemanticError(f"return type must be {node.function_type} but was given {yield_type}")
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
    
    # def visit_Expression(self, node):
    #     for term in node.terms:
    #         # print("now visiting in expression, terms: ", term)
    #         print(type(term))
    #         if term == "None":
    #             pass
    #         self.visit(term)
    
    def visit_Block(self, node):
        # enter scope for block
        self.enter_scope("Block")
        for statement in node.statements:
            # print("now visiting statement in block: ", statement)
            self.visit(statement)
        # exit scope for block
        self.exit_scope()

    def visit_LoopStatement(self, node):
        self.enter_scope("Loop")
        # print("node.loop_type:",node.loop_type)
        loop_type = node.loop_type
        if loop_type == 'while':
            # Visiting is_special
            # print("now visiting:",node.condition)
            self.type_of_expression(node.condition)
            # Visiting updation
            # print("now visiting:",node.updation)
            self.visit(node.updation)
            # Visiting block
            # print("now visiting:",node.block)
            self.visit(node.block)
        elif loop_type == 'iter':
            # Visiting declaration
            print("now visiting in iter declaraion:",node.declaration)
            self.visit(node.declaration)
            rich.print(self.symbol_table)
            # Visiting condition
            print("now visiting in iter condition:",node.condition)
            self.type_of_expression(node.condition)
            # Visiting updation
            print("now visiting in iter updation:",node.updation)
            self.visit(node.updation)
            # Visiting block
            print("now visiting in iter block:",node.block)
            self.visit(node.block)
        # TODO work is going on here. The above is giving an error
        self.exit_scope()
        # TODO elif for third type of loop ---> repeat-while

    def visit_ConditionalArgument(self, node):
        self.type_of_expression(node.expression)

    # Isko change karna padenga for loop
    def visit_Skip(self, node):
        # agar koi loop statement not found before this
        # then this is semantically incorrect
        # TODO : check if loop statement is present before this - PENDING 
        # Currently, Darshi is working on this part
        pass
    # def visit_Term(self, node):
    #     if node.identifier:
    #         self.check_variable_declared(node.identifier)

    def visit_NoneType(self, node):
        pass

    def analyze(self, ast):
        # Perform semantic analysis
        try:
            self.visit(ast)
            self.ast = ast
            return ast, "Semantic analysis completed successfully."
        except SemanticError as e:
            return None, f"Semantic error: {e}"

analyzer = SemanticAnalyzer()
try:
    analyzer.visit(ast)
    print("Semantic analysis completed successfully.")
except SemanticError as e:
    print(f"Semantic error: {e}")