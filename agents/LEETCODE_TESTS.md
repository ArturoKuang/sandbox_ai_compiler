# LeetCode Tests for SimpleLang Compiler

## Overview

This document describes the enhancements made to the SimpleLang compiler to support algorithm testing similar to LeetCode problems.

## New Features Added

### 1. Boolean Type
- Added `bool` keyword for boolean type declarations
- Support for `true` and `false` literals
- Type checking ensures boolean operations are type-safe

### 2. Comparison Operators
- `==` (equality)
- `!=` (inequality)
- `<` (less than)
- `<=` (less than or equal)
- `>` (greater than)
- `>=` (greater than or equal)

All comparison operators:
- Accept `int` operands
- Return `bool` values
- Have proper operator precedence

### 3. Logical Operators
- `&&` (logical AND)
- `||` (logical OR)
- `!` (logical NOT / unary negation)

All logical operators:
- Accept `bool` operands
- Return `bool` values
- Follow standard precedence (NOT > AND > OR)

### 4. Control Flow

#### If Statements
```
if (condition) {
    statements
}

if (condition) {
    statements
} else {
    statements
}
```

#### While Loops
```
while (condition) {
    statements
}
```

## Test Program

The file `examples/leetcode_test.sl` demonstrates all new features:

1. **Finding Maximum**: Uses if statements and comparisons to find max of 3 numbers
2. **Countdown Loop**: Uses while loop with comparison operator
3. **Boolean Operations**: Tests boolean variables and comparison operators
4. **Fibonacci Sequence**: Implements fibonacci using while loops
5. **Logical Operators**: Tests AND, OR, and NOT operators

## Usage

Compile and run the test:
```bash
python simplelang.py examples/leetcode_test.sl --run
```

Expected output:
```
42          # max of (15, 42, 27)
10          # countdown from 10
9
8
7
6
5
4
3
2
1
True        # isPositive (counter >= 0)
False       # isNegative (counter < 0)
0           # Fibonacci sequence
1
1
2
3
5
8
13
21
34
True        # x < y && y > 0
True        # x == y || x < y
True        # !(x > y)
```

## Compiler Architecture Updates

### Lexer (`compiler/lexer/`)
- Added tokens for: `bool`, `if`, `else`, `while`, `true`, `false`
- Added tokens for comparison operators: `==`, `!=`, `<`, `<=`, `>`, `>=`
- Added tokens for logical operators: `&&`, `||`, `!`
- Added delimiters: `{`, `}`, `[`, `]`, `,`

### Parser (`compiler/parser/`)
- New AST nodes: `IfStatement`, `WhileStatement`, `Boolean`, `UnaryOp`
- Expression parsing hierarchy:
  - Logical OR (lowest precedence)
  - Logical AND
  - Comparison (`==`, `!=`, `<`, `<=`, `>`, `>=`)
  - Arithmetic (`+`, `-`, `*`, `/`, `%`)
  - Unary (`!`, `-`)
  - Factor (literals, identifiers, parentheses)

### Semantic Analyzer (`compiler/semantic/`)
- Type checking for boolean type
- Validation of comparison operators (require int operands, return bool)
- Validation of logical operators (require bool operands, return bool)
- Control flow condition validation (must be bool)

### Code Generator (`compiler/codegen/`)
- Python code generation for if/else statements
- Python code generation for while loops
- Operator mapping:
  - `!` → `not`
  - `&&` → `and`
  - `||` → `or`
  - `/` → `//` (integer division)

## Limitations

The compiler currently does NOT support:
- 2D arrays (needed for full Strange Printer II solution)
- Functions
- Return statements
- Arrays/lists
- String type
- For loops
- Break/continue statements
- Comments (use no comments in .sl files)

## Future Extensions

To support more complex LeetCode problems, the following features would be needed:

1. **Arrays**: 1D and 2D array support
2. **Functions**: Function definitions with parameters and return values
3. **More data types**: Strings, floats
4. **Advanced control flow**: For loops, break, continue
5. **Data structures**: Lists, dictionaries/maps
6. **Comments**: Single-line (`//`) and multi-line (`/* */`) comments

## Test Results

All 84 existing unit tests pass after the enhancements, ensuring backward compatibility.

The new test program (`leetcode_test.sl`) successfully:
- Compiles to valid Python code
- Executes correctly with expected output
- Demonstrates all new language features

## Example Generated Python Code

SimpleLang:
```
int a = 15;
int b = 42;
int max = a;
if (b > max) {
    max = b;
}
print(max);
```

Generated Python:
```python
a: int = 15
b: int = 42
max: int = a
if (b > max):
    max = b
print(max)
```

## Conclusion

The SimpleLang compiler has been successfully extended to support essential algorithm programming features. While it cannot yet handle the full Strange Printer II problem due to lack of 2D array support, it can now handle many simpler LeetCode-style problems involving:

- Conditional logic
- Loops
- Boolean algebra
- Comparison operations
- Basic algorithms (finding max/min, counting, simple sequences)

The compiler maintains full backward compatibility with all previous SimpleLang programs.
