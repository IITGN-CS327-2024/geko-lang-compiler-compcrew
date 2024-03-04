References: https://github.com/alexpizarroj/lalr1-table-generator/tree/master

For generating the parse table for our LALR(1) we have used the pre-existing generator with our custom Context Free Grammar for our GEKO language.

# lalr1-table-generator
A tool that generates a LALR(1) parsing table given a formal grammar as input. 

### How to use?
* Run **generator.py**. This file contains a function called *get_grammar()*, which is responsible of returning a Grammar object from which the generator will do its work.
* We have our grammar rules listed in **CFG.py** under grammar_1, use that to generate respective parse tree.
* After running the generator, two new files will be created:
  * **parsing-table.txt**. It contains a summary of the input grammar and a LALR(1) parsing table.
  * **parsing-table.csv**. It contains a LARL(1) parsing table for the input grammar, written in an Excel-style CSV file format. 
