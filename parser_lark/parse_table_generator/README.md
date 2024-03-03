References: https://github.com/alexpizarroj/lalr1-table-generator/tree/master

For generating the parse table for our LALR(1) we have used the pre-existing generator with our custom Context Free Grammar for our GEKO language.

# lalr1-table-generator
A tool that generates a LALR(1) parsing table given a formal grammar as input. 

### How to use?
* Run **generator.py**. This file contains a function called *get_grammar()*, which is responsible of returning a Grammar object from which the generator will do its work. By default, it returns a sample Grammar object from **samples.py**.
* Several samples of grammar definitions can be found in **samples.py**. To define your own, just follow the syntax from the examples.
* After running the generator, two new files will be created:
  * **parsing-table.txt**. It contains a summary of the input grammar and a human-readable LALR(1) parsing table.
  * **parsing-table.csv**. It contains just a LARL(1) parsing table for the input grammar, written in an Excel-style CSV file format. It should be read along with parsing-table.txt.
