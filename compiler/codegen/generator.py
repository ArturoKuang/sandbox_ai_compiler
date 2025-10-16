"""
Code Generator for SimpleLang.

Converts AST to Python source code.
"""

from typing import List
from compiler.parser.ast_nodes import (
    ASTNode, Program, Statement, Declaration, Assignment, PrintStatement,
    IfStatement, WhileStatement,
    Expression, BinaryOp, UnaryOp, Number, Identifier, Boolean
)


class CodeGenerator:
    """Generates Python code from SimpleLang AST."""

    def __init__(self):
        self.output: List[str] = []
        self.indent_level = 0

    def generate(self, ast: Program) -> str:
        """Generates Python code from the AST."""
        self.output = []
        self.visit_program(ast)
        return '\n'.join(self.output)

    def emit(self, line: str) -> None:
        """Emits a line of code with proper indentation."""
        indent = '    ' * self.indent_level
        self.output.append(indent + line)

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

    def visit_declaration(self, node: Declaration) -> None:
        """
        Visits a declaration node.
        Generates: name: type = expression
        """
        expr_code = self.visit_expression(node.value)
        type_annotation = self.get_python_type(node.var_type)
        self.emit(f"{node.name}: {type_annotation} = {expr_code}")

    def visit_assignment(self, node: Assignment) -> None:
        """
        Visits an assignment node.
        Generates: name = expression
        """
        expr_code = self.visit_expression(node.value)
        self.emit(f"{node.name} = {expr_code}")

    def visit_print_statement(self, node: PrintStatement) -> None:
        """
        Visits a print statement node.
        Generates: print(expression)
        """
        expr_code = self.visit_expression(node.expression)
        self.emit(f"print({expr_code})")

    def visit_if_statement(self, node: IfStatement) -> None:
        """
        Visits an if statement node.
        Generates:
        if condition:
            statements
        else:
            statements
        """
        condition_code = self.visit_expression(node.condition)
        self.emit(f"if {condition_code}:")
        self.indent_level += 1
        for stmt in node.then_block:
            self.visit_statement(stmt)
        self.indent_level -= 1

        if node.else_block:
            self.emit("else:")
            self.indent_level += 1
            for stmt in node.else_block:
                self.visit_statement(stmt)
            self.indent_level -= 1

    def visit_while_statement(self, node: WhileStatement) -> None:
        """
        Visits a while statement node.
        Generates:
        while condition:
            statements
        """
        condition_code = self.visit_expression(node.condition)
        self.emit(f"while {condition_code}:")
        self.indent_level += 1
        for stmt in node.body:
            self.visit_statement(stmt)
        self.indent_level -= 1

    def visit_expression(self, node: Expression) -> str:
        """
        Visits an expression node and returns the generated code.
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
        return ""

    def visit_number(self, node: Number) -> str:
        """Visits a number node."""
        return str(node.value)

    def visit_boolean(self, node: Boolean) -> str:
        """Visits a boolean node."""
        return "True" if node.value else "False"

    def visit_identifier(self, node: Identifier) -> str:
        """Visits an identifier node."""
        return node.name

    def visit_unary_op(self, node: UnaryOp) -> str:
        """
        Visits a unary operation node.
        Generates: (operator operand)
        """
        operand_code = self.visit_expression(node.operand)

        # Convert SimpleLang operators to Python operators
        operator_map = {
            '!': 'not',
            '-': '-'
        }
        operator = operator_map.get(node.operator, node.operator)

        return f"({operator} {operand_code})"

    def visit_binary_op(self, node: BinaryOp) -> str:
        """
        Visits a binary operation node.
        Generates: (left operator right)
        Parentheses ensure correct precedence.
        """
        left_code = self.visit_expression(node.left)
        right_code = self.visit_expression(node.right)

        # Convert SimpleLang operators to Python operators
        operator_map = {
            '/': '//',   # Integer division
            '&&': 'and',
            '||': 'or',
        }
        operator = operator_map.get(node.operator, node.operator)

        # Add parentheses for clarity
        # For simple cases, we could optimize this, but for correctness we always add them
        return f"({left_code} {operator} {right_code})"

    def get_python_type(self, simplelang_type: str) -> str:
        """Converts SimpleLang type to Python type annotation."""
        type_map = {
            'int': 'int',
            'bool': 'bool',
        }
        return type_map.get(simplelang_type, simplelang_type)
