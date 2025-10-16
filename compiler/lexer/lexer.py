"""
Lexer (Tokenizer) for SimpleLang.

Converts source code into a stream of tokens.
"""

from typing import List, Optional
from .token import Token, TokenType


class LexerError(Exception):
    """Raised when lexer encounters an invalid character or sequence."""

    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Lexer error at {line}:{column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    """Tokenizes SimpleLang source code."""

    # Keyword mapping
    KEYWORDS = {
        'int': TokenType.INT,
        'bool': TokenType.BOOL,
        'print': TokenType.PRINT,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'return': TokenType.RETURN,
        'function': TokenType.FUNCTION,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
    }

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def current_char(self) -> Optional[str]:
        """Returns the current character or None if at end."""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peeks ahead at a character without consuming it."""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]

    def advance(self) -> None:
        """Advances to the next character."""
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1

    def skip_whitespace(self) -> None:
        """Skips whitespace characters."""
        while self.current_char() and self.current_char() in ' \t\r\n':
            self.advance()

    def read_number(self) -> Token:
        """Reads a number token."""
        start_line = self.line
        start_column = self.column
        num_str = ''

        while self.current_char() and self.current_char().isdigit():
            num_str += self.current_char()
            self.advance()

        return Token(TokenType.NUMBER, int(num_str), start_line, start_column)

    def read_identifier_or_keyword(self) -> Token:
        """Reads an identifier or keyword token."""
        start_line = self.line
        start_column = self.column
        id_str = ''

        # First character must be letter or underscore
        if self.current_char() and (self.current_char().isalpha() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()

        # Subsequent characters can be alphanumeric or underscore
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()

        # Check if it's a keyword
        token_type = self.KEYWORDS.get(id_str, TokenType.IDENTIFIER)
        return Token(token_type, id_str, start_line, start_column)

    def tokenize(self) -> List[Token]:
        """Tokenizes the entire source code."""
        while self.current_char() is not None:
            self.skip_whitespace()

            if self.current_char() is None:
                break

            char = self.current_char()
            line = self.line
            column = self.column

            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())

            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier_or_keyword())

            # Operators and delimiters
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, char, line, column))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, char, line, column))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, char, line, column))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, char, line, column))
                self.advance()
            elif char == '%':
                self.tokens.append(Token(TokenType.MODULO, char, line, column))
                self.advance()
            elif char == '=':
                # Check for ==
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.EQ, '==', line, column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, char, line, column))
                    self.advance()
            elif char == '!':
                # Check for !=
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.NE, '!=', line, column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.NOT, char, line, column))
                    self.advance()
            elif char == '<':
                # Check for <=
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.LE, '<=', line, column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.LT, char, line, column))
                    self.advance()
            elif char == '>':
                # Check for >=
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.GE, '>=', line, column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.GT, char, line, column))
                    self.advance()
            elif char == '&':
                # Check for &&
                if self.peek_char() == '&':
                    self.tokens.append(Token(TokenType.AND, '&&', line, column))
                    self.advance()
                    self.advance()
                else:
                    raise LexerError(f"Unexpected character '{char}' (did you mean '&&'?)", line, column)
            elif char == '|':
                # Check for ||
                if self.peek_char() == '|':
                    self.tokens.append(Token(TokenType.OR, '||', line, column))
                    self.advance()
                    self.advance()
                else:
                    raise LexerError(f"Unexpected character '{char}' (did you mean '||'?)", line, column)
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, char, line, column))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, char, line, column))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, char, line, column))
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, char, line, column))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, char, line, column))
                self.advance()
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, char, line, column))
                self.advance()
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, char, line, column))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, char, line, column))
                self.advance()
            else:
                raise LexerError(f"Unexpected character '{char}'", line, column)

        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
