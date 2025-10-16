# SimpleLang to Python Compiler - Project Plan

## Overview

Building a compiler that translates SimpleLang (a simple imperative language) to Python.

## Language Specifications

### Source Language: SimpleLang
- Statically typed
- C-like syntax
- Imperative programming paradigm

### Target Language: Python
- Dynamic but we'll generate type-safe code
- Readable output for debugging

### Implementation Language: Python 3.8+

## Minimal Feature Set (Phase 1)

Starting with the smallest viable compiler:

1. **Literals**: Integer literals only
2. **Operators**: Basic arithmetic (+, -, *, /, %)
3. **Expressions**: Arithmetic expressions with precedence
4. **Variables**: Declaration and assignment (with type annotations)
5. **Print**: Single print statement for output

### Example SimpleLang Program (Phase 1)
```
int x = 10;
int y = 20;
int result = x + y * 2;
print(result);
```

### Expected Python Output (Phase 1)
```python
x: int = 10
y: int = 20
result: int = x + y * 2
print(result)
```

## Compiler Phases

### 1. Lexer (Tokenizer)
- Input: Source code string
- Output: List of tokens
- Tokens: INT, IDENTIFIER, NUMBER, OPERATORS, SEMICOLON, etc.

### 2. Parser
- Input: Token list
- Output: Abstract Syntax Tree (AST)
- Grammar: Context-free grammar for SimpleLang

### 3. Semantic Analyzer
- Input: AST
- Output: Validated/annotated AST
- Tasks: Type checking, scope analysis, undefined variable detection

### 4. Code Generator
- Input: Validated AST
- Output: Python source code
- Tasks: AST traversal and Python code emission

## Development Milestones

- [ ] Phase 1: Minimal compiler (integers, arithmetic, variables, print)
- [ ] Phase 2: Control flow (if/else, while loops)
- [ ] Phase 3: Functions (definition, calls, parameters, return)
- [ ] Phase 4: Advanced types (arrays, strings)
- [ ] Phase 5: Advanced features (structs, etc.)

## Current Status

Starting with Phase 1 implementation.
