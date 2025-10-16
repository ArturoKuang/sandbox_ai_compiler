"""
Token definitions for SimpleLang lexer.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any


class TokenType(Enum):
    """Token types for SimpleLang."""

    # Keywords
    INT = auto()
    BOOL = auto()
    PRINT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    TRUE = auto()
    FALSE = auto()

    # Identifiers and literals
    IDENTIFIER = auto()
    NUMBER = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()

    # Comparison operators
    EQ = auto()          # ==
    NE = auto()          # !=
    LT = auto()          # <
    LE = auto()          # <=
    GT = auto()          # >
    GE = auto()          # >=

    # Logical operators
    AND = auto()         # &&
    OR = auto()          # ||
    NOT = auto()         # !

    # Delimiters
    SEMICOLON = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    COMMA = auto()       # ,

    # Special
    EOF = auto()


@dataclass
class Token:
    """Represents a single token in the source code."""

    type: TokenType
    value: Any
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"
