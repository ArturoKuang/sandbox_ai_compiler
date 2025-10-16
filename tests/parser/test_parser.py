"""
Unit tests for SimpleLang parser.
"""

import unittest
import sys
sys.path.insert(0, '/Users/arturokuang/sandbox')

from compiler.lexer import Lexer
from compiler.parser import (
    Parser, ParserError,
    Program, Declaration, Assignment, PrintStatement,
    BinaryOp, Number, Identifier
)


class TestParser(unittest.TestCase):
    """Test cases for the parser."""

    def parse_source(self, source: str) -> Program:
        """Helper to lex and parse source code."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()

    def test_empty_program(self):
        """Test parsing an empty program."""
        ast = self.parse_source("")
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 0)

    def test_simple_declaration(self):
        """Test parsing a simple variable declaration."""
        ast = self.parse_source("int x = 42;")
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, Declaration)
        self.assertEqual(stmt.var_type, "int")
        self.assertEqual(stmt.name, "x")
        self.assertIsInstance(stmt.value, Number)
        self.assertEqual(stmt.value.value, 42)

    def test_declaration_with_expression(self):
        """Test parsing a declaration with an arithmetic expression."""
        ast = self.parse_source("int result = 10 + 20;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, Declaration)
        self.assertEqual(stmt.name, "result")
        self.assertIsInstance(stmt.value, BinaryOp)
        self.assertEqual(stmt.value.operator, "+")
        self.assertIsInstance(stmt.value.left, Number)
        self.assertEqual(stmt.value.left.value, 10)
        self.assertIsInstance(stmt.value.right, Number)
        self.assertEqual(stmt.value.right.value, 20)

    def test_assignment(self):
        """Test parsing an assignment statement."""
        ast = self.parse_source("x = 100;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, Assignment)
        self.assertEqual(stmt.name, "x")
        self.assertIsInstance(stmt.value, Number)
        self.assertEqual(stmt.value.value, 100)

    def test_print_statement(self):
        """Test parsing a print statement."""
        ast = self.parse_source("print(42);")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, PrintStatement)
        self.assertIsInstance(stmt.expression, Number)
        self.assertEqual(stmt.expression.value, 42)

    def test_print_identifier(self):
        """Test parsing print with an identifier."""
        ast = self.parse_source("print(result);")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, PrintStatement)
        self.assertIsInstance(stmt.expression, Identifier)
        self.assertEqual(stmt.expression.name, "result")

    def test_arithmetic_operators(self):
        """Test parsing all arithmetic operators."""
        # Addition
        ast = self.parse_source("int a = 1 + 2;")
        self.assertEqual(ast.statements[0].value.operator, "+")

        # Subtraction
        ast = self.parse_source("int b = 5 - 3;")
        self.assertEqual(ast.statements[0].value.operator, "-")

        # Multiplication
        ast = self.parse_source("int c = 4 * 5;")
        self.assertEqual(ast.statements[0].value.operator, "*")

        # Division
        ast = self.parse_source("int d = 10 / 2;")
        self.assertEqual(ast.statements[0].value.operator, "/")

        # Modulo
        ast = self.parse_source("int e = 10 % 3;")
        self.assertEqual(ast.statements[0].value.operator, "%")

    def test_operator_precedence(self):
        """Test that operator precedence is correctly handled."""
        # Multiplication has higher precedence than addition
        ast = self.parse_source("int x = 2 + 3 * 4;")
        stmt = ast.statements[0]
        # Should parse as: 2 + (3 * 4)
        self.assertIsInstance(stmt.value, BinaryOp)
        self.assertEqual(stmt.value.operator, "+")
        self.assertIsInstance(stmt.value.left, Number)
        self.assertEqual(stmt.value.left.value, 2)
        self.assertIsInstance(stmt.value.right, BinaryOp)
        self.assertEqual(stmt.value.right.operator, "*")

    def test_left_associativity(self):
        """Test that operators are left-associative."""
        # Should parse as: (10 - 5) - 2
        ast = self.parse_source("int x = 10 - 5 - 2;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt.value, BinaryOp)
        self.assertEqual(stmt.value.operator, "-")
        self.assertIsInstance(stmt.value.left, BinaryOp)
        self.assertEqual(stmt.value.left.operator, "-")
        self.assertIsInstance(stmt.value.right, Number)
        self.assertEqual(stmt.value.right.value, 2)

    def test_parenthesized_expression(self):
        """Test parsing expressions with parentheses."""
        ast = self.parse_source("int x = (2 + 3) * 4;")
        stmt = ast.statements[0]
        # Should parse as: (2 + 3) * 4
        self.assertIsInstance(stmt.value, BinaryOp)
        self.assertEqual(stmt.value.operator, "*")
        self.assertIsInstance(stmt.value.left, BinaryOp)
        self.assertEqual(stmt.value.left.operator, "+")

    def test_complex_expression(self):
        """Test parsing a complex arithmetic expression."""
        ast = self.parse_source("int result = (10 + 20) * 3 - 5 / 2;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, Declaration)
        self.assertIsInstance(stmt.value, BinaryOp)

    def test_multiple_statements(self):
        """Test parsing multiple statements."""
        source = """
        int x = 10;
        int y = 20;
        int sum = x + y;
        print(sum);
        """
        ast = self.parse_source(source)
        self.assertEqual(len(ast.statements), 4)
        self.assertIsInstance(ast.statements[0], Declaration)
        self.assertIsInstance(ast.statements[1], Declaration)
        self.assertIsInstance(ast.statements[2], Declaration)
        self.assertIsInstance(ast.statements[3], PrintStatement)

    def test_variable_in_expression(self):
        """Test parsing expressions with variables."""
        ast = self.parse_source("int result = x + y * 2;")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt.value, BinaryOp)
        self.assertEqual(stmt.value.operator, "+")
        self.assertIsInstance(stmt.value.left, Identifier)
        self.assertEqual(stmt.value.left.name, "x")

    def test_missing_semicolon(self):
        """Test that missing semicolon raises an error."""
        with self.assertRaises(ParserError) as context:
            self.parse_source("int x = 10")
        self.assertIn("Expected SEMICOLON", str(context.exception))

    def test_invalid_statement(self):
        """Test that invalid statements raise an error."""
        with self.assertRaises(ParserError) as context:
            self.parse_source("42;")
        self.assertIn("expected statement", str(context.exception))

    def test_missing_parenthesis(self):
        """Test that missing parentheses raise an error."""
        with self.assertRaises(ParserError) as context:
            self.parse_source("print(x;")
        self.assertIn("Expected RPAREN", str(context.exception))

    def test_unexpected_token_in_expression(self):
        """Test that unexpected tokens in expressions raise an error."""
        with self.assertRaises(ParserError) as context:
            self.parse_source("int x = ;")
        self.assertIn("expected expression", str(context.exception))


if __name__ == '__main__':
    unittest.main()
