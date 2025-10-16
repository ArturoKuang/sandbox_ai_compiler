"""
Code Generator for SimpleLang.

Converts AST to Python source code.
"""

from typing import List
from compiler.parser.ast_nodes import (
    ASTNode, Program, Statement, Declaration, Assignment, PrintStatement,
    IfStatement, WhileStatement, ForStatement, FunctionDeclaration, ReturnStatement,
    Expression, BinaryOp, UnaryOp, Number, Identifier, Boolean,
    ArrayLiteral, ArrayAccess, FunctionCall
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
        elif isinstance(node, ForStatement):
            self.visit_for_statement(node)
        elif isinstance(node, FunctionDeclaration):
            self.visit_function_declaration(node)
        elif isinstance(node, ReturnStatement):
            self.visit_return_statement(node)

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

    def visit_for_statement(self, node: ForStatement) -> None:
        """
        Visits a for statement node.
        Converts C-style for loop to Python while loop.
        """
        # Emit init if present
        if node.init:
            self.visit_statement(node.init)

        # Convert to while loop
        condition_code = self.visit_expression(node.condition) if node.condition else "True"
        self.emit(f"while {condition_code}:")
        self.indent_level += 1

        # Emit body
        for stmt in node.body:
            self.visit_statement(stmt)

        # Emit update if present
        if node.update:
            self.visit_statement(node.update)

        self.indent_level -= 1

    def visit_function_declaration(self, node: FunctionDeclaration) -> None:
        """
        Visits a function declaration node.
        Generates: def name(params): body
        """
        # Build parameter list
        params_str = ", ".join([f"{name}: {self.get_python_type(ptype)}" for ptype, name in node.params])

        # Emit function signature
        return_type_annotation = f" -> {self.get_python_type(node.return_type)}" if node.return_type else ""
        self.emit(f"def {node.name}({params_str}){return_type_annotation}:")

        self.indent_level += 1

        # Emit body
        if node.body:
            for stmt in node.body:
                self.visit_statement(stmt)
        else:
            self.emit("pass")

        self.indent_level -= 1
        self.emit("")  # Empty line after function

    def visit_return_statement(self, node: ReturnStatement) -> None:
        """
        Visits a return statement node.
        Generates: return expression
        """
        if node.expression:
            expr_code = self.visit_expression(node.expression)
            self.emit(f"return {expr_code}")
        else:
            self.emit("return")

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
        elif isinstance(node, ArrayLiteral):
            return self.visit_array_literal(node)
        elif isinstance(node, ArrayAccess):
            return self.visit_array_access(node)
        elif isinstance(node, FunctionCall):
            return self.visit_function_call(node)
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

    def visit_array_literal(self, node: ArrayLiteral) -> str:
        """
        Visits an array literal node.
        Generates: [elem1, elem2, ...]
        """
        elements_code = [self.visit_expression(elem) for elem in node.elements]
        return "[" + ", ".join(elements_code) + "]"

    def visit_array_access(self, node: ArrayAccess) -> str:
        """
        Visits an array access node.
        Generates: array[index]
        """
        array_code = self.visit_expression(node.array)
        index_code = self.visit_expression(node.index)
        return f"{array_code}[{index_code}]"

    def visit_function_call(self, node: FunctionCall) -> str:
        """
        Visits a function call node.
        Generates: name(arg1, arg2, ...)
        """
        args_code = [self.visit_expression(arg) for arg in node.arguments]
        return f"{node.name}({', '.join(args_code)})"

    def get_python_type(self, simplelang_type: str) -> str:
        """Converts SimpleLang type to Python type annotation."""
        type_map = {
            'int': 'int',
            'bool': 'bool',
        }
        return type_map.get(simplelang_type, simplelang_type)
