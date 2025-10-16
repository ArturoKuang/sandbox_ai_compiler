# SimpleLang Grammar Specification

## Phase 1 Grammar (Minimal Subset)

### Lexical Grammar (Tokens)

```
KEYWORD     : 'int' | 'print'
IDENTIFIER  : [a-zA-Z_][a-zA-Z0-9_]*
NUMBER      : [0-9]+
PLUS        : '+'
MINUS       : '-'
MULTIPLY    : '*'
DIVIDE      : '/'
MODULO      : '%'
ASSIGN      : '='
SEMICOLON   : ';'
LPAREN      : '('
RPAREN      : ')'
WHITESPACE  : [ \t\r\n]+ (ignored)
```

### Syntactic Grammar (CFG)

```
program         : statement_list

statement_list  : statement
                | statement_list statement

statement       : declaration
                | assignment
                | print_stmt

declaration     : type IDENTIFIER ASSIGN expression SEMICOLON

assignment      : IDENTIFIER ASSIGN expression SEMICOLON

print_stmt      : 'print' LPAREN expression RPAREN SEMICOLON

type            : 'int'

expression      : term
                | expression PLUS term
                | expression MINUS term

term            : factor
                | term MULTIPLY factor
                | term DIVIDE factor
                | term MODULO factor

factor          : NUMBER
                | IDENTIFIER
                | LPAREN expression RPAREN
```

### Operator Precedence (Highest to Lowest)

1. Parentheses `()`
2. Multiplication, Division, Modulo `*`, `/`, `%`
3. Addition, Subtraction `+`, `-`

### Operator Associativity

- All binary operators are left-associative

## Future Extensions (Phase 2+)

Will add:
- Boolean type and literals
- Comparison operators
- Logical operators
- If/else statements
- While loops
- Functions
- Arrays
- Strings
