# SimpleLang Compiler Architecture

This document provides a detailed overview of the compiler's architecture and design decisions.

## Overview

The SimpleLang compiler follows a traditional multi-phase compiler architecture:

```
Source Code → Lexer → Tokens → Parser → AST → Semantic Analyzer → Validated AST → Code Generator → Python Code
```

## Compiler Phases

### 1. Lexical Analysis (Lexer)

**Location**: `compiler/lexer/`

**Purpose**: Converts source code string into a stream of tokens.

**Components**:
- `Token`: Dataclass representing a single token with type, value, line, and column
- `TokenType`: Enum defining all token types
- `Lexer`: Main lexer class that performs tokenization

**Algorithm**:
1. Scan through source code character by character
2. Skip whitespace while tracking line and column numbers
3. Recognize patterns:
   - Numbers: Sequences of digits → NUMBER token
   - Identifiers: Letter/underscore followed by alphanumerics → IDENTIFIER or KEYWORD
   - Operators: Single characters → Operator tokens
   - Delimiters: Single characters → Delimiter tokens
4. Raise `LexerError` for invalid characters

**Design Decisions**:
- Uses a simple character-by-character scanner (no regex for clarity)
- Tracks line and column for error reporting
- Keywords are recognized during identifier scanning (lookup table)
- All whitespace is ignored

**Example**:
```
Input:  "int x = 10;"
Output: [INT, IDENTIFIER("x"), ASSIGN, NUMBER(10), SEMICOLON, EOF]
```

### 2. Parsing

**Location**: `compiler/parser/`

**Purpose**: Converts token stream into an Abstract Syntax Tree (AST).

**Components**:
- `ast_nodes.py`: Defines all AST node types (Program, Declaration, BinaryOp, etc.)
- `parser.py`: Recursive descent parser implementation

**Algorithm**:
The parser uses recursive descent with one function per grammar rule:

- `parse_program()`: Entry point, collects all statements
- `parse_statement()`: Dispatches to specific statement parsers
- `parse_declaration()`: Handles variable declarations
- `parse_assignment()`: Handles assignments
- `parse_print_statement()`: Handles print statements
- `parse_expression()`: Handles addition/subtraction (lower precedence)
- `parse_term()`: Handles multiplication/division/modulo (higher precedence)
- `parse_factor()`: Handles literals, identifiers, parenthesized expressions

**Precedence Implementation**:
Precedence is encoded in the grammar structure:
```
expression → term → factor
```
This creates a parse tree where higher precedence operators are deeper in the tree.

**Design Decisions**:
- Recursive descent for simplicity and clarity
- One lookahead token is sufficient
- Left-associativity achieved through iteration (while loops)
- Detailed error messages with source location

**Example**:
```
Input:  [INT, IDENTIFIER("x"), ASSIGN, NUMBER(10), SEMICOLON]
Output: Program([Declaration("int", "x", Number(10))])
```

### 3. Semantic Analysis

**Location**: `compiler/semantic/`

**Purpose**: Validates semantic correctness of the AST.

**Components**:
- `SymbolTable`: Manages variable declarations and their types
- `SemanticAnalyzer`: Visitor pattern implementation for AST traversal

**Checks Performed**:
1. **Undefined variables**: All referenced variables must be declared
2. **Redeclaration**: Variables cannot be declared twice
3. **Type checking**: Expression types must match declaration types
4. **Operator validation**: Operators must be used with compatible types

**Algorithm**:
1. Traverse AST using visitor pattern
2. For each declaration:
   - Check that variable isn't already declared
   - Infer type of initializer expression
   - Add to symbol table
3. For each assignment:
   - Check that variable is declared
   - Infer type of assigned expression
   - Verify type compatibility
4. For each expression:
   - Recursively infer types
   - Verify operand type compatibility

**Design Decisions**:
- Visitor pattern for clean separation of concerns
- Single-pass analysis (no need for multiple passes)
- Symbol table tracks only types (no scope nesting needed in Phase 1)
- Type inference from bottom-up during expression analysis

**Example**:
```
int x = y;  // ERROR: Undefined variable 'y'
int x = 10;
int x = 20; // ERROR: Variable 'x' already declared
```

### 4. Code Generation

**Location**: `compiler/codegen/`

**Purpose**: Converts validated AST into Python source code.

**Components**:
- `CodeGenerator`: AST visitor that emits Python code

**Algorithm**:
1. Traverse AST using visitor pattern
2. For each node, emit corresponding Python code:
   - **Declaration**: `name: type = expression`
   - **Assignment**: `name = expression`
   - **Print**: `print(expression)`
   - **BinaryOp**: `(left operator right)` with parentheses
   - **Number**: String representation of value
   - **Identifier**: Variable name as-is

**Design Decisions**:
- Always parenthesize binary operations for correctness
- Convert `/` to `//` for integer division
- Use Python type annotations for clarity
- Emit line-by-line to list, join at end

**Optimizations Not Implemented** (intentionally for clarity):
- Unnecessary parentheses removal
- Constant folding
- Dead code elimination

**Example**:
```
Input:  Program([Declaration("int", "x", BinaryOp(Number(10), "+", Number(20)))])
Output: "x: int = (10 + 20)"
```

## Data Structures

### Token
```python
@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
```

Represents a single lexical unit with source location.

### AST Nodes

All AST nodes inherit from `ASTNode` base class.

**Statement Nodes**:
- `Program`: Root node containing list of statements
- `Declaration`: Variable declaration with type
- `Assignment`: Variable assignment
- `PrintStatement`: Print statement

**Expression Nodes**:
- `BinaryOp`: Binary operation (left, operator, right)
- `Number`: Integer literal
- `Identifier`: Variable reference

### Symbol Table
```python
symbols: Dict[str, str]  # name -> type
```

Simple dictionary mapping variable names to types.

## Design Patterns

### Visitor Pattern

Used in both semantic analysis and code generation:
```python
def visit_declaration(self, node: Declaration) -> None:
    # Handle declaration
    pass

def visit_assignment(self, node: Assignment) -> None:
    # Handle assignment
    pass
```

Benefits:
- Separates AST structure from operations on AST
- Easy to add new operations without modifying AST nodes
- Clear, organized code

### Recursive Descent Parsing

Each grammar rule becomes a function:
```python
def parse_expression(self):
    left = self.parse_term()
    while current_token in ['+', '-']:
        op = advance()
        right = self.parse_term()
        left = BinaryOp(left, op, right)
    return left
```

Benefits:
- Direct mapping from grammar to code
- Easy to understand and debug
- Handles precedence naturally through call stack

## Error Handling Strategy

### Error Types

1. **LexerError**: Invalid characters or sequences
2. **ParserError**: Syntax errors (unexpected tokens)
3. **SemanticError**: Type errors, undefined variables, redeclarations

### Error Reporting

All errors include:
- Error type
- Descriptive message
- Line number
- Column number

Example:
```
Semantic error at 3:5: Undefined variable 'foo'
```

### Error Recovery

Currently: **Fail-fast** strategy
- Stop on first error
- Report error with location
- Exit compilation

Future: Could implement error recovery to report multiple errors.

## Type System

### Phase 1: Integer Only

- Single type: `int`
- All literals are integers
- All operators return integers
- Type checking is straightforward

### Future Extensions

Could add:
- Boolean type (`bool`)
- String type (`string`)
- Array types (`int[]`)
- User-defined types (`struct`)

Would require:
- Type inference improvements
- Operator overloading
- Subtyping/type compatibility rules

## Code Quality Principles

### 1. Simplicity Over Performance

The compiler prioritizes clarity over optimization:
- No complex algorithms or data structures
- Straightforward implementations
- Obvious code flow

### 2. Explicit Over Implicit

- Explicit type checking
- Explicit error messages
- Explicit AST node types

### 3. Testability

- Each phase independently testable
- Clear interfaces between phases
- Comprehensive test coverage

### 4. Extensibility

- Modular design
- Easy to add new features
- Clear extension points

## Testing Strategy

### Unit Tests

Each compiler phase has dedicated unit tests:
- **Lexer**: Token recognition, error handling, location tracking
- **Parser**: Grammar rules, precedence, error messages
- **Semantic**: Type checking, scope analysis, error detection
- **Codegen**: Code generation, correctness

### Integration Tests

Test full pipeline with various programs:
- Simple programs
- Complex expressions
- Error cases
- Edge cases

### End-to-End Tests

Test compiler CLI:
- File compilation
- Command-line options
- Generated code execution

### Test Coverage

84 tests covering:
- Happy paths
- Error conditions
- Edge cases
- All language features

## Performance Considerations

### Current Performance

For Phase 1 programs (small, simple):
- Compilation time: < 10ms
- Memory usage: Minimal
- No optimization needed

### Scalability

Current implementation scales linearly:
- O(n) lexing
- O(n) parsing
- O(n) semantic analysis
- O(n) code generation

For larger programs or language extensions, could add:
- Lazy evaluation
- Incremental compilation
- Parallel processing

## Future Architecture Changes

### For Phase 2+ Features

1. **Control Flow**:
   - Add basic blocks to AST
   - Control flow graph construction
   - More complex code generation

2. **Functions**:
   - Function symbol table
   - Call graph analysis
   - Stack frame management

3. **Type System**:
   - Type inference engine
   - Generic types support
   - Type checking algorithm improvements

4. **Optimization**:
   - Constant folding
   - Dead code elimination
   - Common subexpression elimination

5. **Better Error Handling**:
   - Error recovery
   - Multiple error reporting
   - Suggestions for fixes

## Conclusion

The SimpleLang compiler demonstrates a clean, educational implementation of compiler construction principles. The architecture is designed for clarity and extensibility, making it an excellent foundation for learning or for adding more sophisticated features.
