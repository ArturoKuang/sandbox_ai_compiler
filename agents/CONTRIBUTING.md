# Contributing to SimpleLang Compiler

This guide explains how to extend the SimpleLang compiler with new features.

## Adding New Language Features

### 1. Adding a New Operator

Example: Adding the power operator `**`

#### Step 1: Update the Lexer

Add token type in `compiler/lexer/token.py`:
```python
class TokenType(Enum):
    # ... existing tokens ...
    POWER = auto()  # Add this
```

Add recognition in `compiler/lexer/lexer.py`:
```python
elif char == '*':
    if self.peek_char() == '*':
        self.advance()  # Skip second *
        self.tokens.append(Token(TokenType.POWER, '**', line, column))
        self.advance()
    else:
        self.tokens.append(Token(TokenType.MULTIPLY, char, line, column))
        self.advance()
```

#### Step 2: Update the Parser

Add to grammar (in appropriate precedence level):
```python
def parse_factor(self) -> Expression:
    # ... existing code ...
    left = self.parse_primary()

    # Handle power operator (right-associative)
    if self.current_token().type == TokenType.POWER:
        op_token = self.advance()
        right = self.parse_factor()  # Right-associative
        return BinaryOp(left, '**', right, op_token.line, op_token.column)

    return left
```

#### Step 3: Update the Semantic Analyzer

Add operator to validation in `compiler/semantic/analyzer.py`:
```python
def visit_binary_op(self, node: BinaryOp) -> str:
    # ... existing code ...

    if node.operator in ('+', '-', '*', '/', '%', '**'):  # Add '**'
        return "int"
```

#### Step 4: Update the Code Generator

Power operator works in Python as-is, so no changes needed in `compiler/codegen/generator.py`.

#### Step 5: Add Tests

Add tests in all relevant test files:
```python
def test_power_operator(self):
    """Test power operator."""
    source = "int x = 2 ** 3;"
    ast = self.parse_source(source)
    # ... assertions ...
```

### 2. Adding a New Data Type

Example: Adding boolean type

#### Step 1: Update the Lexer

Add keywords:
```python
KEYWORDS = {
    'int': TokenType.INT,
    'bool': TokenType.BOOL,     # Add this
    'true': TokenType.TRUE,     # Add this
    'false': TokenType.FALSE,   # Add this
    'print': TokenType.PRINT,
}
```

#### Step 2: Update the Parser

Add AST nodes in `compiler/parser/ast_nodes.py`:
```python
@dataclass
class Boolean(Expression):
    """Boolean literal."""
    value: bool
    line: int
    column: int
```

Update parser to handle boolean literals:
```python
def parse_factor(self) -> Expression:
    token = self.current_token()

    # ... existing cases ...

    elif token.type in (TokenType.TRUE, TokenType.FALSE):
        self.advance()
        value = token.type == TokenType.TRUE
        return Boolean(value, token.line, token.column)
```

#### Step 3: Update the Semantic Analyzer

Add type checking:
```python
def visit_boolean(self, node: Boolean) -> str:
    return "bool"

def visit_declaration(self, node: Declaration) -> None:
    # ... existing code ...
    # Now handles both 'int' and 'bool' types
```

#### Step 4: Update the Code Generator

Add code generation:
```python
def visit_boolean(self, node: Boolean) -> str:
    return "True" if node.value else "False"

def get_python_type(self, simplelang_type: str) -> str:
    type_map = {
        'int': 'int',
        'bool': 'bool',  # Add this
    }
    return type_map.get(simplelang_type, simplelang_type)
```

#### Step 5: Add Tests

Test in all phases.

### 3. Adding Control Flow (if/else)

#### Step 1: Update the Lexer

Add keywords:
```python
TokenType.IF = auto()
TokenType.ELSE = auto()
TokenType.LBRACE = auto()  # {
TokenType.RBRACE = auto()  # }
```

#### Step 2: Update the Grammar

Add to grammar specification:
```
if_stmt : 'if' '(' expression ')' '{' statement_list '}'
          ('else' '{' statement_list '}')?
```

#### Step 3: Update the Parser

Add AST nodes:
```python
@dataclass
class IfStatement(Statement):
    condition: Expression
    then_body: List[Statement]
    else_body: Optional[List[Statement]]
    line: int
    column: int
```

Add parsing function:
```python
def parse_if_statement(self) -> IfStatement:
    if_token = self.expect(TokenType.IF)
    self.expect(TokenType.LPAREN)
    condition = self.parse_expression()
    self.expect(TokenType.RPAREN)
    self.expect(TokenType.LBRACE)

    then_body = []
    while self.current_token().type != TokenType.RBRACE:
        then_body.append(self.parse_statement())
    self.expect(TokenType.RBRACE)

    else_body = None
    if self.current_token().type == TokenType.ELSE:
        self.advance()
        self.expect(TokenType.LBRACE)
        else_body = []
        while self.current_token().type != TokenType.RBRACE:
            else_body.append(self.parse_statement())
        self.expect(TokenType.RBRACE)

    return IfStatement(condition, then_body, else_body, if_token.line, if_token.column)
```

#### Step 4: Update the Semantic Analyzer

Add validation:
```python
def visit_if_statement(self, node: IfStatement) -> None:
    # Condition must be boolean
    cond_type = self.visit_expression(node.condition)
    if cond_type != 'bool':
        raise SemanticError(f"If condition must be bool, got {cond_type}", ...)

    for stmt in node.then_body:
        self.visit_statement(stmt)

    if node.else_body:
        for stmt in node.else_body:
            self.visit_statement(stmt)
```

#### Step 5: Update the Code Generator

Add code generation:
```python
def visit_if_statement(self, node: IfStatement) -> None:
    cond_code = self.visit_expression(node.condition)
    self.emit(f"if {cond_code}:")

    self.indent_level += 1
    for stmt in node.then_body:
        self.visit_statement(stmt)
    self.indent_level -= 1

    if node.else_body:
        self.emit("else:")
        self.indent_level += 1
        for stmt in node.else_body:
            self.visit_statement(stmt)
        self.indent_level -= 1
```

### 4. Adding Functions

This is more complex and requires:
- Function declarations with parameters
- Function calls with arguments
- Return statements
- Function symbol table
- Parameter type checking
- Return type checking

See `.agent/PROJECT_PLAN.md` for planned Phase 3 features.

## Testing Guidelines

### Test-Driven Development

1. Write tests first
2. Run tests (they should fail)
3. Implement feature
4. Run tests (they should pass)
5. Refactor if needed

### Test Coverage

Ensure new features have tests at all levels:
- **Unit tests**: Each compiler phase
- **Integration tests**: Full pipeline
- **E2E tests**: CLI and examples

### Test Organization

```
tests/
  lexer/test_lexer.py          # Add lexer tests here
  parser/test_parser.py         # Add parser tests here
  semantic/test_analyzer.py     # Add semantic tests here
  codegen/test_generator.py     # Add codegen tests here
  integration/test_full_pipeline.py  # Add integration tests here
  e2e/test_examples.py          # Add E2E tests here
```

## Code Style

### Python Style

- Follow PEP 8
- Use type hints
- Write docstrings for all functions
- Use meaningful variable names

### Documentation

- Update README.md with new features
- Update grammar specification if grammar changes
- Add examples for new features
- Update ARCHITECTURE.md for significant changes

## Commit Guidelines

### Commit Messages

Format:
```
<type>: <description>

<body>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `test`: Adding tests
- `docs`: Documentation changes

### Commit Frequency

Commit after each significant change:
- After implementing each phase of a feature
- After fixing a bug
- After adding tests

## Development Workflow

### 1. Plan

- Define the feature clearly
- Update PROJECT_PLAN.md
- Sketch out changes needed in each phase

### 2. Implement

- Update lexer (if needed)
- Update parser (if needed)
- Update semantic analyzer (if needed)
- Update code generator (if needed)

### 3. Test

- Write comprehensive tests
- Run all tests to ensure nothing broke
- Fix any failing tests

### 4. Document

- Update README.md
- Update GRAMMAR.md
- Add example programs
- Update ARCHITECTURE.md

### 5. Commit and Push

- Make clear, descriptive commits
- Push after each file edit as per project guidelines

## Common Patterns

### Adding a Statement Type

1. Add token types in lexer (if new keywords)
2. Create AST node class
3. Add parsing function
4. Add semantic analysis visitor method
5. Add code generation visitor method
6. Add tests

### Adding an Expression Type

1. Add token types in lexer (if needed)
2. Create AST node class
3. Update expression parsing
4. Add type inference in semantic analyzer
5. Add code generation
6. Add tests

### Adding an Operator

1. Add token type
2. Add to lexer recognition
3. Update grammar and parser
4. Add to semantic operator validation
5. Update code generator (if Python equivalent differs)
6. Add tests

## Debugging Tips

### Use Debug Flags

```bash
# See tokens
python simplelang.py program.sl --tokens

# See AST
python simplelang.py program.sl --ast
```

### Add Print Statements

Temporarily add print statements in compiler phases to see what's happening.

### Test Incrementally

Test each phase independently:
```python
# Test just lexer
lexer = Lexer(source)
print(lexer.tokenize())

# Test lexer + parser
lexer = Lexer(source)
parser = Parser(lexer.tokenize())
print(parser.parse())
```

## Resources

### Understanding Compilers

- Dragon Book: "Compilers: Principles, Techniques, and Tools"
- "Crafting Interpreters" by Robert Nystrom
- "Writing a Compiler in Go" by Thorsten Ball

### Python Resources

- Python documentation
- Type hints guide
- unittest documentation

## Questions?

Check existing code for examples:
- Look at how current features are implemented
- Read ARCHITECTURE.md for design patterns
- Run tests to see expected behavior

## Summary

1. Plan your feature
2. Implement across all compiler phases
3. Write comprehensive tests
4. Document your changes
5. Commit and push frequently

Happy coding!
