# Instructions to run this code

1. Clone this repository and run the cpp.py from Geko_CodeGen folder via this command. This will generate teh cpp code for the given geko code.
```$ python cpp.py .\Geko-Codes\<geko_file>```

2. The Geko_CodeGen folder has the following files/folders:
   - `cpp.py`: This is a Python script that converts geko code to cpp code for code generation
   - wasm: folder that has the corresponding wasm files for the cpp codes. The wasm files can be used further to run the code.

# Instructions to install emsdk
1. Follow the steps from this link: [here](https://emscripten.org/docs/getting_started/downloads.html)
2. Also ensure that node.js is installed.
3. Add `.\emsdk\upstream\emscripten` to the path variable in the environmen variables present on your computer/PC
4. Restart your PC/computer/laptop before running to ensure smooth running

# Important Note:
1. Since in C++, `div` is a keyword, the name of the function we have kept is `divi`. So, change the name in the corresponding `arithmetic-test.js`
2. Also, the name in the `arithmetic-test.js` for wasm file is `arthimetic.wasm` instead of `arithmetic.wasm`. So, please correct that.

# Command to generate the wasm file from the .cpp file
To generate for:

`caesar.cpp`: `$emcc -Os -s STANDALONE_WASM -s EXPORTED_FUNCTIONS="['_caesarEncrypt','_caesarDecrypt']" --no-entry "caesar.cpp" -o "caesar.wasm"`

`sort.cpp`: `$emcc -Os -s STANDALONE_WASM -s EXPORTED_FUNCTIONS="['_sort']" --no-entry "sort.cpp" -o "sort.wasm"`

`arithmetic.cpp`: `$emcc -Os -s STANDALONE_WASM -s EXPORTED_FUNCTIONS="['_add','_sub','_divison','_mul','_mod']" --no-entry "arithmetic.cpp" -o "arithmetic.wasm"`
