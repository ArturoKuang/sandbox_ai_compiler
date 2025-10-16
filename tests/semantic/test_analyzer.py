"""
Unit tests for SimpleLang semantic analyzer.
"""

import unittest
import sys
sys.path.insert(0, '/Users/arturokuang/sandbox')

from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.semantic import SemanticAnalyzer, SemanticError


class TestSemanticAnalyzer(unittest.TestCase):
    """Test cases for the semantic analyzer."""

    def analyze_source(self, source: str) -> None:
        """Helper to lex, parse, and analyze source code."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)

    def test_simple_declaration(self):
        """Test analyzing a simple variable declaration."""
        self.analyze_source("int x = 42;")
        # Should not raise any errors

    def test_declaration_with_expression(self):
        """Test analyzing a declaration with an expression."""
        self.analyze_source("int result = 10 + 20;")
        # Should not raise any errors

    def test_multiple_declarations(self):
        """Test analyzing multiple variable declarations."""
        source = """
        int x = 10;
        int y = 20;
        int z = 30;
        """
        self.analyze_source(source)
        # Should not raise any errors

    def test_assignment_to_declared_variable(self):
        """Test analyzing assignment to a declared variable."""
        source = """
        int x = 10;
        x = 20;
        """
        self.analyze_source(source)
        # Should not raise any errors

    def test_variable_in_expression(self):
        """Test analyzing expressions with variables."""
        source = """
        int x = 10;
        int y = 20;
        int sum = x + y;
        """
        self.analyze_source(source)
        # Should not raise any errors

    def test_complex_expression(self):
        """Test analyzing a complex expression."""
        source = """
        int a = 5;
        int b = 10;
        int c = 15;
        int result = (a + b) * c - 20 / 4;
        """
        self.analyze_source(source)
        # Should not raise any errors

    def test_print_literal(self):
        """Test analyzing print with a literal."""
        self.analyze_source("print(42);")
        # Should not raise any errors

    def test_print_variable(self):
        """Test analyzing print with a variable."""
        source = """
        int x = 100;
        print(x);
        """
        self.analyze_source(source)
        # Should not raise any errors

    def test_print_expression(self):
        """Test analyzing print with an expression."""
        source = """
        int x = 10;
        int y = 20;
        print(x + y * 2);
        """
        self.analyze_source(source)
        # Should not raise any errors

    def test_undefined_variable_in_declaration(self):
        """Test that using undefined variable in declaration raises error."""
        source = "int x = y + 10;"
        with self.assertRaises(SemanticError) as context:
            self.analyze_source(source)
        self.assertIn("Undefined variable 'y'", str(context.exception))

    def test_undefined_variable_in_assignment(self):
        """Test that assigning to undefined variable raises error."""
        source = "x = 10;"
        with self.assertRaises(SemanticError) as context:
            self.analyze_source(source)
        self.assertIn("Undefined variable 'x'", str(context.exception))

    def test_undefined_variable_in_expression(self):
        """Test that undefined variable in expression raises error."""
        source = """
        int x = 10;
        int result = x + undefined_var;
        """
        with self.assertRaises(SemanticError) as context:
            self.analyze_source(source)
        self.assertIn("Undefined variable 'undefined_var'", str(context.exception))

    def test_undefined_variable_in_print(self):
        """Test that undefined variable in print raises error."""
        source = "print(undefined_var);"
        with self.assertRaises(SemanticError) as context:
            self.analyze_source(source)
        self.assertIn("Undefined variable 'undefined_var'", str(context.exception))

    def test_redeclaration_error(self):
        """Test that redeclaring a variable raises error."""
        source = """
        int x = 10;
        int x = 20;
        """
        with self.assertRaises(SemanticError) as context:
            self.analyze_source(source)
        self.assertIn("Variable 'x' already declared", str(context.exception))

    def test_all_operators(self):
        """Test that all arithmetic operators work correctly."""
        source = """
        int a = 10 + 5;
        int b = 10 - 5;
        int c = 10 * 5;
        int d = 10 / 5;
        int e = 10 % 5;
        """
        self.analyze_source(source)
        # Should not raise any errors

    def test_nested_expressions(self):
        """Test analyzing deeply nested expressions."""
        source = """
        int x = 1;
        int y = 2;
        int z = 3;
        int result = ((x + y) * (z - x)) / (y + 1);
        """
        self.analyze_source(source)
        # Should not raise any errors

    def test_variable_order(self):
        """Test that variables must be declared before use."""
        source = """
        int result = x + y;
        int x = 10;
        int y = 20;
        """
        with self.assertRaises(SemanticError) as context:
            self.analyze_source(source)
        self.assertIn("Undefined variable", str(context.exception))

    def test_assignment_type_compatibility(self):
        """Test that assignment maintains type compatibility."""
        source = """
        int x = 10;
        int y = x;
        x = y + 5;
        """
        self.analyze_source(source)
        # Should not raise any errors


if __name__ == '__main__':
    unittest.main()
