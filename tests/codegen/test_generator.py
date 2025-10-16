"""
Unit tests for SimpleLang code generator.
"""

import unittest
import sys
sys.path.insert(0, '/Users/arturokuang/sandbox')

from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.codegen import CodeGenerator


class TestCodeGenerator(unittest.TestCase):
    """Test cases for the code generator."""

    def generate_code(self, source: str) -> str:
        """Helper to lex, parse, and generate code."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        generator = CodeGenerator()
        return generator.generate(ast)

    def test_simple_declaration(self):
        """Test generating code for a simple declaration."""
        source = "int x = 42;"
        expected = "x: int = 42"
        result = self.generate_code(source)
        self.assertEqual(result, expected)

    def test_declaration_with_expression(self):
        """Test generating code for declaration with expression."""
        source = "int result = 10 + 20;"
        result = self.generate_code(source)
        self.assertIn("result: int = ", result)
        self.assertIn("10", result)
        self.assertIn("20", result)
        self.assertIn("+", result)

    def test_multiple_declarations(self):
        """Test generating code for multiple declarations."""
        source = """
        int x = 10;
        int y = 20;
        """
        result = self.generate_code(source)
        self.assertIn("x: int = 10", result)
        self.assertIn("y: int = 20", result)

    def test_assignment(self):
        """Test generating code for assignment."""
        source = """
        int x = 10;
        x = 20;
        """
        result = self.generate_code(source)
        lines = result.split('\n')
        self.assertEqual(lines[0], "x: int = 10")
        self.assertEqual(lines[1], "x = 20")

    def test_print_literal(self):
        """Test generating code for print with literal."""
        source = "print(42);"
        expected = "print(42)"
        result = self.generate_code(source)
        self.assertEqual(result, expected)

    def test_print_identifier(self):
        """Test generating code for print with identifier."""
        source = """
        int x = 100;
        print(x);
        """
        result = self.generate_code(source)
        lines = result.split('\n')
        self.assertEqual(lines[0], "x: int = 100")
        self.assertEqual(lines[1], "print(x)")

    def test_arithmetic_operators(self):
        """Test generating code for all arithmetic operators."""
        test_cases = [
            ("int a = 1 + 2;", "+"),
            ("int b = 5 - 3;", "-"),
            ("int c = 4 * 5;", "*"),
            ("int d = 10 / 2;", "/"),
            ("int e = 10 % 3;", "%"),
        ]
        for source, operator in test_cases:
            result = self.generate_code(source)
            self.assertIn(operator, result)

    def test_complex_expression(self):
        """Test generating code for complex expression."""
        source = "int result = (10 + 20) * 3;"
        result = self.generate_code(source)
        self.assertIn("result: int = ", result)
        # Should contain parentheses and operators
        self.assertIn("10", result)
        self.assertIn("20", result)
        self.assertIn("3", result)

    def test_variable_in_expression(self):
        """Test generating code for expression with variables."""
        source = """
        int x = 10;
        int y = 20;
        int sum = x + y;
        """
        result = self.generate_code(source)
        lines = result.split('\n')
        self.assertEqual(lines[0], "x: int = 10")
        self.assertEqual(lines[1], "y: int = 20")
        self.assertIn("sum: int = ", lines[2])
        self.assertIn("x", lines[2])
        self.assertIn("y", lines[2])

    def test_print_expression(self):
        """Test generating code for print with expression."""
        source = """
        int x = 10;
        int y = 20;
        print(x + y);
        """
        result = self.generate_code(source)
        lines = result.split('\n')
        self.assertIn("print(", lines[2])
        self.assertIn("x", lines[2])
        self.assertIn("y", lines[2])

    def test_complete_program(self):
        """Test generating code for a complete program."""
        source = """
        int x = 10;
        int y = 20;
        int result = x + y * 2;
        print(result);
        """
        result = self.generate_code(source)
        lines = result.split('\n')

        # Should have 4 lines
        self.assertEqual(len(lines), 4)

        # Check each line
        self.assertIn("x: int = 10", lines[0])
        self.assertIn("y: int = 20", lines[1])
        self.assertIn("result: int = ", lines[2])
        self.assertIn("print(result)", lines[3])

    def test_parenthesized_expression(self):
        """Test that parentheses are preserved in expressions."""
        source = "int x = (2 + 3) * 4;"
        result = self.generate_code(source)
        # Generated code should maintain proper precedence
        self.assertIn("x: int = ", result)


class TestGeneratedCodeExecution(unittest.TestCase):
    """Test that generated Python code actually executes correctly."""

    def execute_generated_code(self, source: str) -> str:
        """Generates code and executes it, returning output."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        generator = CodeGenerator()
        python_code = generator.generate(ast)

        # Capture print output
        import io
        import contextlib

        output_buffer = io.StringIO()
        with contextlib.redirect_stdout(output_buffer):
            exec(python_code)

        return output_buffer.getvalue().strip()

    def test_execute_simple_print(self):
        """Test executing generated code for simple print."""
        source = "print(42);"
        output = self.execute_generated_code(source)
        self.assertEqual(output, "42")

    def test_execute_arithmetic(self):
        """Test executing generated code with arithmetic."""
        source = """
        int x = 10;
        int y = 20;
        print(x + y);
        """
        output = self.execute_generated_code(source)
        self.assertEqual(output, "30")

    def test_execute_complex_expression(self):
        """Test executing generated code with complex expression."""
        source = """
        int x = 10;
        int y = 20;
        int result = x + y * 2;
        print(result);
        """
        output = self.execute_generated_code(source)
        self.assertEqual(output, "50")  # 10 + (20 * 2) = 50

    def test_execute_all_operators(self):
        """Test executing generated code with all operators."""
        source = """
        int a = 15 + 5;
        print(a);
        int b = 15 - 5;
        print(b);
        int c = 15 * 2;
        print(c);
        int d = 15 / 3;
        print(d);
        int e = 15 % 4;
        print(e);
        """
        output = self.execute_generated_code(source)
        lines = output.split('\n')
        self.assertEqual(lines[0], "20")  # 15 + 5
        self.assertEqual(lines[1], "10")  # 15 - 5
        self.assertEqual(lines[2], "30")  # 15 * 2
        self.assertEqual(lines[3], "5")   # 15 / 3
        self.assertEqual(lines[4], "3")   # 15 % 4

    def test_execute_variable_reassignment(self):
        """Test executing generated code with variable reassignment."""
        source = """
        int x = 10;
        print(x);
        x = 20;
        print(x);
        """
        output = self.execute_generated_code(source)
        lines = output.split('\n')
        self.assertEqual(lines[0], "10")
        self.assertEqual(lines[1], "20")


if __name__ == '__main__':
    unittest.main()
