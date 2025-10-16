"""
End-to-end tests using the example programs.

Tests the compiler by compiling and running actual example files.
"""

import unittest
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, '/Users/arturokuang/sandbox')


class TestExamples(unittest.TestCase):
    """Test the compiler with example programs."""

    def setUp(self):
        """Set up test environment."""
        self.examples_dir = Path('/Users/arturokuang/sandbox/examples')
        self.compiler = Path('/Users/arturokuang/sandbox/simplelang.py')

    def compile_and_run(self, example_file: str) -> str:
        """
        Compiles and runs an example file, returning output.
        """
        source_path = self.examples_dir / example_file

        # Compile and run using the compiler
        result = subprocess.run(
            [sys.executable, str(self.compiler), str(source_path), '--run'],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            self.fail(f"Compilation failed: {result.stderr}")

        # Extract just the program output (after the separator line)
        output_lines = result.stdout.split('\n')
        separator_index = -1
        for i, line in enumerate(output_lines):
            if '---' in line:
                separator_index = i
                break

        if separator_index >= 0:
            program_output = '\n'.join(output_lines[separator_index + 1:])
            return program_output.strip()
        return ""

    def test_hello_example(self):
        """Test the hello.sl example."""
        output = self.compile_and_run('hello.sl')
        self.assertEqual(output, "42")

    def test_arithmetic_example(self):
        """Test the arithmetic.sl example."""
        output = self.compile_and_run('arithmetic.sl')
        lines = output.split('\n')
        self.assertEqual(lines[0], "30")   # sum
        self.assertEqual(lines[1], "-10")  # diff
        self.assertEqual(lines[2], "200")  # product
        self.assertEqual(lines[3], "2")    # quotient
        self.assertEqual(lines[4], "0")    # remainder

    def test_complex_example(self):
        """Test the complex.sl example."""
        output = self.compile_and_run('complex.sl')
        lines = output.split('\n')
        self.assertEqual(lines[0], "225")  # (5 + 10) * 15
        self.assertEqual(lines[1], "155")  # 5 + 10 * 15
        self.assertEqual(lines[2], "150")  # (5 + 10) * (15 - 5)
        self.assertEqual(lines[3], "50")   # 100 + 50 = 150, 150 / 3 = 50

    def test_generated_python_files(self):
        """Test that generated Python files are valid."""
        examples = ['hello.sl', 'arithmetic.sl', 'complex.sl']

        for example in examples:
            source_path = self.examples_dir / example
            python_path = source_path.with_suffix('.py')

            # Ensure the .py file exists
            self.assertTrue(
                python_path.exists(),
                f"Generated Python file {python_path} should exist"
            )

            # Verify it's valid Python by running it
            result = subprocess.run(
                [sys.executable, str(python_path)],
                capture_output=True,
                text=True
            )

            self.assertEqual(
                result.returncode, 0,
                f"Generated Python file {python_path} should execute without errors"
            )


class TestCompilerCLI(unittest.TestCase):
    """Test the compiler's command-line interface."""

    def setUp(self):
        """Set up test environment."""
        self.examples_dir = Path('/Users/arturokuang/sandbox/examples')
        self.compiler = Path('/Users/arturokuang/sandbox/simplelang.py')

    def test_tokens_flag(self):
        """Test the --tokens flag."""
        source_path = self.examples_dir / 'hello.sl'

        result = subprocess.run(
            [sys.executable, str(self.compiler), str(source_path), '--tokens'],
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Tokens:", result.stdout)
        self.assertIn("INT", result.stdout)
        self.assertIn("IDENTIFIER", result.stdout)

    def test_ast_flag(self):
        """Test the --ast flag."""
        source_path = self.examples_dir / 'hello.sl'

        result = subprocess.run(
            [sys.executable, str(self.compiler), str(source_path), '--ast'],
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("AST:", result.stdout)
        self.assertIn("Program", result.stdout)

    def test_custom_output_file(self):
        """Test specifying a custom output file."""
        source_path = self.examples_dir / 'hello.sl'
        output_path = self.examples_dir / 'custom_output.py'

        # Clean up if exists
        if output_path.exists():
            output_path.unlink()

        result = subprocess.run(
            [sys.executable, str(self.compiler), str(source_path), '-o', str(output_path)],
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)
        self.assertTrue(output_path.exists())

        # Clean up
        output_path.unlink()


if __name__ == '__main__':
    unittest.main()
