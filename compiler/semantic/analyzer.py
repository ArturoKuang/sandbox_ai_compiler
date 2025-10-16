"""
Semantic Analyzer for SimpleLang.

Performs type checking, scope analysis, and other semantic validations.
"""

from typing import Dict, Set, Optional
from compiler.parser.ast_nodes import (
    ASTNode, Program, Statement, Declaration, Assignment, PrintStatement,
    IfStatement, WhileStatement,
    Expression, BinaryOp, UnaryOp, Number, Identifier, Boolean
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
        elif isinstance(node, IfStatement):
            self.visit_if_statement(node)
        elif isinstance(node, WhileStatement):
            self.visit_while_statement(node)
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

    def visit_if_statement(self, node: IfStatement) -> None:
        """
        Visits an if statement node.
        Checks:
        - Condition is a boolean expression
        - All statements in blocks are valid
        """
        # Check condition type
        condition_type = self.visit_expression(node.condition)
        if condition_type != "bool":
            raise SemanticError(
                f"If condition must be bool, got {condition_type}",
                node.line,
                node.column
            )

        # Visit then block
        for stmt in node.then_block:
            self.visit_statement(stmt)

        # Visit else block if present
        if node.else_block:
            for stmt in node.else_block:
                self.visit_statement(stmt)

    def visit_while_statement(self, node: WhileStatement) -> None:
        """
        Visits a while statement node.
        Checks:
        - Condition is a boolean expression
        - All statements in body are valid
        """
        # Check condition type
        condition_type = self.visit_expression(node.condition)
        if condition_type != "bool":
            raise SemanticError(
                f"While condition must be bool, got {condition_type}",
                node.line,
                node.column
            )

        # Visit body
        for stmt in node.body:
            self.visit_statement(stmt)

    def visit_expression(self, node: Expression) -> str:
        """
        Visits an expression node and returns its type.
        """
        if isinstance(node, Number):
            return self.visit_number(node)
        elif isinstance(node, Boolean):
            return self.visit_boolean(node)
        elif isinstance(node, Identifier):
            return self.visit_identifier(node)
        elif isinstance(node, BinaryOp):
            return self.visit_binary_op(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unary_op(node)
        else:
            raise SemanticError(
                f"Unknown expression type: {type(node).__name__}",
                0, 0
            )

    def visit_number(self, node: Number) -> str:
        """Visits a number node. Numbers are always type 'int'."""
        return "int"

    def visit_boolean(self, node: Boolean) -> str:
        """Visits a boolean node. Booleans are always type 'bool'."""
        return "bool"

    def visit_identifier(self, node: Identifier) -> str:
        """Visits an identifier node. Returns the variable's type."""
        return self.symbol_table.lookup(node.name, node.line, node.column)

    def visit_unary_op(self, node: UnaryOp) -> str:
        """
        Visits a unary operation node.
        Checks:
        - Operator is valid for the operand type
        Returns the result type.
        """
        operand_type = self.visit_expression(node.operand)

        # NOT operator requires bool operand
        if node.operator == '!':
            if operand_type != "bool":
                raise SemanticError(
                    f"Unary operator '!' requires bool operand, got {operand_type}",
                    node.line,
                    node.column
                )
            return "bool"

        # Unary minus requires int operand
        if node.operator == '-':
            if operand_type != "int":
                raise SemanticError(
                    f"Unary operator '-' requires int operand, got {operand_type}",
                    node.line,
                    node.column
                )
            return "int"

        raise SemanticError(
            f"Unknown unary operator: {node.operator}",
            node.line,
            node.column
        )

    def visit_binary_op(self, node: BinaryOp) -> str:
        """
        Visits a binary operation node.
        Checks:
        - Operands have appropriate types for the operator
        - Operators are valid for the operand types
        Returns the result type.
        """
        left_type = self.visit_expression(node.left)
        right_type = self.visit_expression(node.right)

        # Arithmetic operators: require int operands, return int
        if node.operator in ('+', '-', '*', '/', '%'):
            if left_type != "int" or right_type != "int":
                raise SemanticError(
                    f"Arithmetic operator '{node.operator}' requires int operands",
                    node.line,
                    node.column
                )
            return "int"

        # Comparison operators: require int operands, return bool
        if node.operator in ('<', '<=', '>', '>='):
            if left_type != "int" or right_type != "int":
                raise SemanticError(
                    f"Comparison operator '{node.operator}' requires int operands",
                    node.line,
                    node.column
                )
            return "bool"

        # Equality operators: require same types, return bool
        if node.operator in ('==', '!='):
            if left_type != right_type:
                raise SemanticError(
                    f"Equality operator '{node.operator}' requires operands of same type",
                    node.line,
                    node.column
                )
            return "bool"

        # Logical operators: require bool operands, return bool
        if node.operator in ('&&', '||'):
            if left_type != "bool" or right_type != "bool":
                raise SemanticError(
                    f"Logical operator '{node.operator}' requires bool operands",
                    node.line,
                    node.column
                )
            return "bool"

        raise SemanticError(
            f"Unknown binary operator: {node.operator}",
            node.line,
            node.column
        )
