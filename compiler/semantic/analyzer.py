"""
Semantic Analyzer for SimpleLang.

Performs type checking, scope analysis, and other semantic validations.
"""

from typing import Dict, Set, Optional
from compiler.parser.ast_nodes import (
    ASTNode, Program, Statement, Declaration, Assignment, PrintStatement,
    Expression, BinaryOp, Number, Identifier
)


class SemanticError(Exception):
    """Raised when semantic analysis detects an error."""

    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Semantic error at {line}:{column}: {message}")
        self.line = line
        self.column = column


class SymbolTable:
    """Manages variable declarations and their types."""

    def __init__(self):
        self.symbols: Dict[str, str] = {}  # name -> type

    def declare(self, name: str, var_type: str, line: int, column: int) -> None:
        """Declares a new variable."""
        if name in self.symbols:
            raise SemanticError(f"Variable '{name}' already declared", line, column)
        self.symbols[name] = var_type

    def lookup(self, name: str, line: int, column: int) -> str:
        """Looks up a variable's type."""
        if name not in self.symbols:
            raise SemanticError(f"Undefined variable '{name}'", line, column)
        return self.symbols[name]

    def is_defined(self, name: str) -> bool:
        """Checks if a variable is defined."""
        return name in self.symbols


class SemanticAnalyzer:
    """Performs semantic analysis on the AST."""

    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, ast: Program) -> None:
        """Analyzes the entire program."""
        self.visit_program(ast)

    def visit_program(self, node: Program) -> None:
        """Visits a program node."""
        for statement in node.statements:
            self.visit_statement(statement)

    def visit_statement(self, node: Statement) -> None:
        """Visits a statement node."""
        if isinstance(node, Declaration):
            self.visit_declaration(node)
        elif isinstance(node, Assignment):
            self.visit_assignment(node)
        elif isinstance(node, PrintStatement):
            self.visit_print_statement(node)
        else:
            raise SemanticError(
                f"Unknown statement type: {type(node).__name__}",
                0, 0
            )

    def visit_declaration(self, node: Declaration) -> None:
        """
        Visits a declaration node.
        Checks:
        - Variable is not already declared
        - Expression type matches declared type
        """
        # Check expression type
        expr_type = self.visit_expression(node.value)

        # Verify type compatibility
        if node.var_type != expr_type:
            raise SemanticError(
                f"Type mismatch: cannot assign {expr_type} to {node.var_type}",
                node.line,
                node.column
            )

        # Declare the variable
        self.symbol_table.declare(node.name, node.var_type, node.line, node.column)

    def visit_assignment(self, node: Assignment) -> None:
        """
        Visits an assignment node.
        Checks:
        - Variable is already declared
        - Expression type matches variable type
        """
        # Look up variable type
        var_type = self.symbol_table.lookup(node.name, node.line, node.column)

        # Check expression type
        expr_type = self.visit_expression(node.value)

        # Verify type compatibility
        if var_type != expr_type:
            raise SemanticError(
                f"Type mismatch: cannot assign {expr_type} to {var_type}",
                node.line,
                node.column
            )

    def visit_print_statement(self, node: PrintStatement) -> None:
        """
        Visits a print statement node.
        Checks that the expression is valid.
        """
        self.visit_expression(node.expression)

    def visit_expression(self, node: Expression) -> str:
        """
        Visits an expression node and returns its type.
        """
        if isinstance(node, Number):
            return self.visit_number(node)
        elif isinstance(node, Identifier):
            return self.visit_identifier(node)
        elif isinstance(node, BinaryOp):
            return self.visit_binary_op(node)
        else:
            raise SemanticError(
                f"Unknown expression type: {type(node).__name__}",
                0, 0
            )

    def visit_number(self, node: Number) -> str:
        """Visits a number node. Numbers are always type 'int'."""
        return "int"

    def visit_identifier(self, node: Identifier) -> str:
        """Visits an identifier node. Returns the variable's type."""
        return self.symbol_table.lookup(node.name, node.line, node.column)

    def visit_binary_op(self, node: BinaryOp) -> str:
        """
        Visits a binary operation node.
        Checks:
        - Both operands have the same type
        - Operators are valid for the operand types
        Returns the result type.
        """
        left_type = self.visit_expression(node.left)
        right_type = self.visit_expression(node.right)

        # For Phase 1, we only support int operations
        if left_type != "int" or right_type != "int":
            raise SemanticError(
                f"Binary operation '{node.operator}' requires int operands",
                node.line,
                node.column
            )

        # All arithmetic operators on ints return int
        if node.operator in ('+', '-', '*', '/', '%'):
            return "int"

        raise SemanticError(
            f"Unknown binary operator: {node.operator}",
            node.line,
            node.column
        )
