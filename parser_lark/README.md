### GENERAL POINTS
The file **parser_lark.py** has to be run to parse the original code after tokeninzing it. It will generate the parse tree (in the format of lark) if the code is parsed successfully and gives the respective error.

Here, you will also find two folders
* correct_testcases: This folder contains the codes with correct syntax. Hence, these codes will be successfully parsed by our geko parser.
* incorrect_testcases: This folder contains the codes with incorrect syntax. Hence, these codes will not be parsed by our geko parser.
### RUNNING INSTRUCTIONS
1. Download the whole repository.
2. Open the parser_lark folder on terminal.
3. In the terminal, write ```python parser_lark.py .\correct_testcases\<geko_file>``` to run the codes with correct syntax. Or run ```python parser_lark.py .\incorrect_testcases\<geko_file>``` to run the codes with wrong syntax.
