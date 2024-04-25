### SOME CONSTRAINTS THAT GEKO LANGUAGE FOLLOWS
1. Geko does not have global variable declaration outside main function
2. For functions in Geko, they MUST return some value according to the data_type defined for a function
3. Geko does not return array, list, or tuple directly
4. By default, the outputs to the show statements will be shown in different lines
5. No default values can be given in the parameter_list in function

### GENERAL POINTS
The file **parser_lark.py** has to be run to parse the original code after tokeninzing it. It will generate the parse tree (in the format of lark) if the code is parsed successfully and gives the respective error.

Here, you will also find two folders
* correct_testcases: This folder contains the codes with correct syntax. Hence, these codes will be successfully parsed by our geko parser.
* incorrect_testcases: This folder contains the codes with incorrect syntax. Hence, these codes will not be parsed by our geko parser.
### RUNNING INSTRUCTIONS
1. Download the whole repository.
2. Open the parser_lark folder on terminal.
3. In the terminal, write ```python parser_lark.py .\correct_testcases\<geko_file>``` to run the codes with correct syntax. Or run ```python parser_lark.py .\incorrect_testcases\<geko_file>``` to run the codes with wrong syntax.

### TREE FORMATION: 
1. After completion of the aforementioned running instructions, we would get a display message indicating the formation of a visual representation of the parse tree, as a .png file.
2. If the test cases being run are correct, the parse tree is formed correctly, and the image is saved.
3. If the test cases being run are incorrect, the parse tree is not formed, and thus the image is also not saved. 
4. After each run, the tree is saved in the same .png file - parse_tree.png and modified_parse_tree.png (modified indicates that we have even added the values of tokens into the tree, successfully.)
