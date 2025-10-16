"""
Integration tests for the full compiler pipeline.

Tests the complete flow from source code to generated Python code.
"""

import unittest
import sys
sys.path.insert(0, '/Users/arturokuang/sandbox')

from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.semantic import SemanticAnalyzer
from compiler.codegen import CodeGenerator


class TestFullPipeline(unittest.TestCase):
    """Test the complete compilation pipeline."""

    def compile_and_execute(self, source: str) -> str:
        """
        Compiles SimpleLang source and executes it, returning output.
        """
        # Lexical analysis
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()

        # Semantic analysis
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)

        # Code generation
        generator = CodeGenerator()
        python_code = generator.generate(ast)

        # Execute and capture output
        import io
        import contextlib

        output_buffer = io.StringIO()
        with contextlib.redirect_stdout(output_buffer):
            exec(python_code)

        return output_buffer.getvalue().strip()

    def test_simple_program(self):
        """Test compiling and running a simple program."""
        source = """
        int x = 42;
        print(x);
        """
        output = self.compile_and_execute(source)
        self.assertEqual(output, "42")

    def test_arithmetic_program(self):
        """Test compiling and running arithmetic operations."""
        source = """
        int x = 10;
        int y = 5;
        int sum = x + y;
        int diff = x - y;
        int prod = x * y;
        print(sum);
        print(diff);
        print(prod);
        """
        output = self.compile_and_execute(source)
        lines = output.split('\n')
        self.assertEqual(lines[0], "15")
        self.assertEqual(lines[1], "5")
        self.assertEqual(lines[2], "50")

    def test_complex_expressions(self):
        """Test compiling and running complex expressions."""
        source = """
        int a = 5;
        int b = 10;
        int c = 2;
        int result = (a + b) * c - 5;
        print(result);
        """
        output = self.compile_and_execute(source)
        self.assertEqual(output, "25")  # (5 + 10) * 2 - 5 = 25

    def test_operator_precedence(self):
        """Test that operator precedence is correct."""
        source = """
        int result = 2 + 3 * 4;
        print(result);
        """
        output = self.compile_and_execute(source)
        self.assertEqual(output, "14")  # 2 + (3 * 4) = 14

    def test_parentheses_override_precedence(self):
        """Test that parentheses override precedence."""
        source = """
        int result = (2 + 3) * 4;
        print(result);
        """
        output = self.compile_and_execute(source)
        self.assertEqual(output, "20")  # (2 + 3) * 4 = 20

    def test_integer_division(self):
        """Test that division produces integer results."""
        source = """
        int result = 15 / 2;
        print(result);
        """
        output = self.compile_and_execute(source)
        self.assertEqual(output, "7")  # Integer division

    def test_modulo_operation(self):
        """Test modulo operation."""
        source = """
        int result = 17 % 5;
        print(result);
        """
        output = self.compile_and_execute(source)
        self.assertEqual(output, "2")

    def test_variable_reassignment(self):
        """Test variable reassignment."""
        source = """
        int x = 10;
        print(x);
        x = 20;
        print(x);
        x = x + 5;
        print(x);
        """
        output = self.compile_and_execute(source)
        lines = output.split('\n')
        self.assertEqual(lines[0], "10")
        self.assertEqual(lines[1], "20")
        self.assertEqual(lines[2], "25")

    def test_multiple_variables(self):
        """Test programs with multiple variables."""
        source = """
        int a = 1;
        int b = 2;
        int c = 3;
        int d = 4;
        int e = 5;
        int sum = a + b + c + d + e;
        print(sum);
        """
        output = self.compile_and_execute(source)
        self.assertEqual(output, "15")

    def test_nested_expressions(self):
        """Test deeply nested expressions."""
        source = """
        int result = ((10 + 5) * 2 - 3) / 3;
        print(result);
        """
        output = self.compile_and_execute(source)
        self.assertEqual(output, "9")  # ((10 + 5) * 2 - 3) / 3 = (15 * 2 - 3) / 3 = 27 / 3 = 9

    def test_left_associativity(self):
        """Test that operators are left-associative."""
        source = """
        int result = 20 - 10 - 5;
        print(result);
        """
        output = self.compile_and_execute(source)
        self.assertEqual(output, "5")  # (20 - 10) - 5 = 5

    def test_all_operators_together(self):
        """Test using all operators in one program."""
        source = """
        int a = 100;
        int b = 10;
        int add = a + b;
        int sub = a - b;
        int mul = a * b;
        int div = a / b;
        int mod = a % b;
        print(add);
        print(sub);
        print(mul);
        print(div);
        print(mod);
        """
        output = self.compile_and_execute(source)
        lines = output.split('\n')
        self.assertEqual(lines[0], "110")
        self.assertEqual(lines[1], "90")
        self.assertEqual(lines[2], "1000")
        self.assertEqual(lines[3], "10")
        self.assertEqual(lines[4], "0")


if __name__ == '__main__':
    unittest.main()
