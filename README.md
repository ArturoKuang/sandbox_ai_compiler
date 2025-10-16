# SimpleLang Compiler

A complete language-to-language compiler that translates SimpleLang (a simple imperative language) to Python, built from scratch.

## Overview

This project demonstrates the full compiler pipeline:
- **Lexer** (Tokenizer): Breaks source code into tokens
- **Parser**: Builds an Abstract Syntax Tree (AST) from tokens
- **Semantic Analyzer**: Performs type checking and scope analysis
- **Code Generator**: Transforms AST into executable Python code

## Features

### SimpleLang Language Features (Phase 1)

- **Data Types**: Integer (`int`)
- **Variables**: Declaration and assignment
- **Operators**:
  - Arithmetic: `+`, `-`, `*`, `/`, `%`
  - Assignment: `=`
- **Statements**:
  - Variable declarations with type annotations
  - Variable assignments
  - Print statements
- **Expressions**:
  - Arithmetic expressions with proper precedence
  - Parenthesized expressions
  - Variable references

### Compiler Features

- **Comprehensive error reporting** with line and column numbers
- **Type checking** ensures type safety
- **Scope analysis** detects undefined variables
- **Operator precedence** correctly handled
- **Clean Python output** with type annotations
- **Command-line interface** with multiple options

## Installation

No external dependencies required! Uses only Python 3.8+ standard library.

```bash
git clone <repository-url>
cd sandbox
```

## Usage

### Basic Compilation

Compile a SimpleLang file to Python:

```bash
python simplelang.py examples/hello.sl
```

This generates `examples/hello.py`.

### Compile and Run

Compile and immediately execute the generated code:

```bash
python simplelang.py examples/hello.sl --run
```

### Specify Output File

```bash
python simplelang.py program.sl -o output.py
```

### Debug Options

View tokens (lexer output):
```bash
python simplelang.py program.sl --tokens
```

View AST (parser output):
```bash
python simplelang.py program.sl --ast
```

## SimpleLang Syntax

### Variable Declaration

```
int x = 42;
int result = 10 + 20;
```

### Variable Assignment

```
int x = 10;
x = 20;
x = x + 5;
```

### Arithmetic Expressions

```
int a = 5;
int b = 10;
int sum = a + b;
int product = a * b;
int quotient = b / a;
int remainder = b % a;
int complex = (a + b) * 2 - 5;
```

### Print Statement

```
print(42);
print(x);
print(x + y * 2);
```

## Examples

### Hello World

```
int x = 42;
print(x);
```

### Arithmetic Operations

```
int x = 10;
int y = 20;
int sum = x + y;
print(sum);
```

### Complex Expressions

```
int a = 5;
int b = 10;
int c = 15;
int result = (a + b) * c;
print(result);
```

More examples in the `examples/` directory.

## Project Structure

```
.
├── compiler/
│   ├── lexer/          # Tokenization
│   │   ├── token.py    # Token definitions
│   │   └── lexer.py    # Lexer implementation
│   ├── parser/         # Parsing
│   │   ├── ast_nodes.py # AST node definitions
│   │   └── parser.py   # Recursive descent parser
│   ├── semantic/       # Semantic analysis
│   │   └── analyzer.py # Type checking and scope analysis
│   └── codegen/        # Code generation
│       └── generator.py # Python code generator
├── tests/              # Test suite
│   ├── lexer/          # Lexer unit tests
│   ├── parser/         # Parser unit tests
│   ├── semantic/       # Semantic analyzer tests
│   ├── codegen/        # Code generator tests
│   ├── integration/    # Integration tests
│   └── e2e/            # End-to-end tests
├── examples/           # Example SimpleLang programs
├── .agent/             # Planning and design documents
├── simplelang.py       # Main compiler driver
└── README.md           # This file
```

## Grammar Specification

### Lexical Grammar

```
KEYWORD     : 'int' | 'print'
IDENTIFIER  : [a-zA-Z_][a-zA-Z0-9_]*
NUMBER      : [0-9]+
OPERATORS   : '+' | '-' | '*' | '/' | '%' | '='
DELIMITERS  : ';' | '(' | ')'
```

### Syntactic Grammar

```
program         : statement_list

statement       : declaration
                | assignment
                | print_stmt

declaration     : type IDENTIFIER '=' expression ';'

assignment      : IDENTIFIER '=' expression ';'

print_stmt      : 'print' '(' expression ')' ';'

expression      : term (('+' | '-') term)*

term            : factor (('*' | '/' | '%') factor)*

factor          : NUMBER
                | IDENTIFIER
                | '(' expression ')'
```

### Operator Precedence

1. Parentheses `()`
2. Multiplication, Division, Modulo `*`, `/`, `%`
3. Addition, Subtraction `+`, `-`

All operators are left-associative.

## Testing

The project includes 84 comprehensive tests covering all compiler phases.

### Run All Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Run Specific Test Suites

```bash
# Lexer tests (13 tests)
python -m unittest tests.lexer.test_lexer -v

# Parser tests (17 tests)
python -m unittest tests.parser.test_parser -v

# Semantic analyzer tests (18 tests)
python -m unittest tests.semantic.test_analyzer -v

# Code generator tests (17 tests)
python -m unittest tests.codegen.test_generator -v

# Integration tests (12 tests)
python -m unittest tests.integration.test_full_pipeline -v

# End-to-end tests (7 tests)
python -m unittest tests.e2e.test_examples -v
```

## Architecture

### Compilation Pipeline

1. **Lexical Analysis**: Source code → Tokens
2. **Parsing**: Tokens → Abstract Syntax Tree (AST)
3. **Semantic Analysis**: AST → Validated AST (type checking, scope analysis)
4. **Code Generation**: Validated AST → Python code

### Error Handling

Each phase provides detailed error messages with source location:

```
Lexer error at 1:15: Unexpected character '@'
Parser error at 2:10: Expected SEMICOLON, got EOF
Semantic error at 3:5: Undefined variable 'x'
```

### Type System

Phase 1 supports only integer types. The semantic analyzer:
- Ensures variables are declared before use
- Prevents variable redeclaration
- Verifies type compatibility in assignments
- Validates operator usage

## Development

### Adding New Features

The compiler is designed for easy extension:

1. **New operators**: Add to lexer and parser, update semantic analyzer
2. **New types**: Extend type system in semantic analyzer and code generator
3. **New statements**: Add AST nodes, parser rules, and code generation logic

### Code Quality

- Clean, maintainable code with meaningful names
- Comprehensive docstrings for all modules and functions
- Extensive test coverage (84 tests)
- Type hints throughout the codebase

## Future Extensions

Potential additions for Phase 2+:

- Boolean type and logical operators
- Comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`)
- Control flow (`if`/`else`, `while` loops)
- Functions (definition, calls, parameters, return values)
- Arrays and strings
- User-defined types/structs

## Implementation Details

### Integer Division

SimpleLang's `/` operator performs integer division. The code generator converts it to Python's `//` operator to maintain integer semantics.

### Operator Precedence

The parser implements operator precedence through the grammar structure:
- `expression` handles addition/subtraction
- `term` handles multiplication/division/modulo
- `factor` handles literals, identifiers, and parentheses

This ensures correct precedence without explicit precedence tables.

### Code Generation

The code generator produces clean, readable Python:
- Type annotations for variable declarations
- Preserved operator precedence through parenthesization
- Direct mapping of SimpleLang constructs to Python equivalents

## License

This is an educational project demonstrating compiler construction concepts.

## Author

Built with Claude Code - An AI-powered development assistant.
