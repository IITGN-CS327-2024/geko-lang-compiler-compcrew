# GROUP NAME: CompCrew
### Our Programming Language: Geko
### Final Folder: Geko_CompCrew
#### MEMBERS:
|Name              |Roll Number      |
|:------------------|:-----------------|
|Darshi Doshi      |21110050|
|Saumya Jaiswal    |21110186|
|Shreya Patel      |21110155|
|Animesh Tumne     |21110227|

<p align="left"><img src="https://github.com/IITGN-CS327-2024/our-own-compiler-compcrew/assets/134190955/c304842e-fb75-4203-a09b-e26c32378bce" alt="geko" height="150"></p>

## LEXER:

- The lexer file is named lexer.py, and all the tescases are also nested under the testcases folder.
- Each test file has the .geko extension, unique to our Geko language.
- Peek into lexer.py for more information on how lexer.py works.

NOTE: For viewing the updated version, please go into the "lexer" folder, and have a look at the README file for instructions on how to run our lexer.

## PARSER:

- The final parser we are using is ./parser_lark/parser_lark.py
- All the test cases (correct and incorrect) are also nested under the respective testcases folder (inside ./parser_lark).
- To get the graph of our obtained parse tree, you need to have graphwiz installed in your system. Please do so by visiting [here](https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/10.0.1/windows_10_cmake_Release_graphviz-install-10.0.1-win64.exe)
- Similar to lexer.py, peek into ./parser_lark and have a read of the README.md file, to understand the workings of our parser.

NOTE: Similar to the lexer, the updated instructions on how to run our parser are posted under ./parser_lark inside the readme file.

## AST:
- Under the AST_lark folder
- The final AST file is named as ast_final.py, and all the correct tescases are also nested under the correct_testcases folder (inside ./AST_lark).
- The defined classes are in ast_classes.py file.
- Our grammar is stored in ast_grammar.py

NOTE: For viewing the updated version, please go into the "lexer" folder, and have a look at the README file for instructions on how to run our lexer.
