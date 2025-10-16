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
    PRINT = auto()

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

    # Delimiters
    SEMICOLON = auto()
    LPAREN = auto()
    RPAREN = auto()

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
