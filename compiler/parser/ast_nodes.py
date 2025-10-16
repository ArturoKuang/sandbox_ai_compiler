"""
Abstract Syntax Tree (AST) node definitions for SimpleLang.
"""

from dataclasses import dataclass
from typing import List, Any
from abc import ABC, abstractmethod


class ASTNode(ABC):
    """Base class for all AST nodes."""

    @abstractmethod
    def __repr__(self) -> str:
        pass


# Program and Statements

@dataclass
class Program(ASTNode):
    """Root node representing the entire program."""
    statements: List['Statement']

    def __repr__(self) -> str:
        return f"Program({self.statements})"


class Statement(ASTNode):
    """Base class for all statements."""
    pass


@dataclass
class Declaration(Statement):
    """Variable declaration statement: type name = expr;"""
    var_type: str
    name: str
    value: 'Expression'
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Declaration({self.var_type}, {self.name}, {self.value})"


@dataclass
class Assignment(Statement):
    """Variable assignment statement: name = expr;"""
    name: str
    value: 'Expression'
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Assignment({self.name}, {self.value})"


@dataclass
class PrintStatement(Statement):
    """Print statement: print(expr);"""
    expression: 'Expression'
    line: int
    column: int

    def __repr__(self) -> str:
        return f"PrintStatement({self.expression})"


# Expressions

class Expression(ASTNode):
    """Base class for all expressions."""
    pass


@dataclass
class BinaryOp(Expression):
    """Binary operation: left op right"""
    left: Expression
    operator: str
    right: Expression
    line: int
    column: int

    def __repr__(self) -> str:
        return f"BinaryOp({self.left}, {self.operator}, {self.right})"


@dataclass
class Number(Expression):
    """Integer literal."""
    value: int
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Number({self.value})"


@dataclass
class Identifier(Expression):
    """Variable reference."""
    name: str
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Identifier({self.name})"
