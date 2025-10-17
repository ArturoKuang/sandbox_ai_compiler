#!/usr/bin/env python3
"""
SimpleLang Compiler - Main Driver

Compiles SimpleLang source code to Python.

Usage:
    python simplelang.py <source_file> [-o <output_file>] [--run]

Arguments:
    source_file     Path to SimpleLang source file
    -o, --output    Output Python file (default: same name with .py extension)
    --run           Run the generated Python code immediately
    --ast           Print the AST instead of generating code
    --tokens        Print tokens instead of compiling
"""

import sys
import argparse
from pathlib import Path

from compiler.lexer import Lexer, LexerError
from compiler.parser import Parser, ParserError
from compiler.semantic import SemanticAnalyzer, SemanticError
from compiler.codegen import CodeGenerator


class CompilerError(Exception):
    """Base class for all compiler errors."""
    pass


def compile_source(source_code: str, source_file: str = "<input>") -> str:
    """
    Compiles SimpleLang source code to Python.

    Args:
        source_code: The SimpleLang source code
        source_file: Name of the source file (for error messages)

    Returns:
        Generated Python code

    Raises:
        CompilerError: If compilation fails
    """
    try:
        # Lexical analysis
        lexer = Lexer(source_code)
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

        return python_code

    except (LexerError, ParserError, SemanticError) as e:
        raise CompilerError(f"Compilation failed: {e}") from e


def main():
    """Main entry point for the compiler."""
    parser = argparse.ArgumentParser(
        description="SimpleLang to Python Compiler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Compile to Python:
    python simplelang.py program.sl

  Compile and specify output file:
    python simplelang.py program.sl -o output.py

  Compile and run immediately:
    python simplelang.py program.sl --run

  Show tokens:
    python simplelang.py program.sl --tokens

  Show AST:
    python simplelang.py program.sl --ast
        """
    )

    parser.add_argument(
        'source_file',
        help='SimpleLang source file to compile'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output Python file (default: <source>.py)'
    )
    parser.add_argument(
        '--run',
        action='store_true',
        help='Run the generated Python code immediately'
    )
    parser.add_argument(
        '--tokens',
        action='store_true',
        help='Print tokens and exit (for debugging)'
    )
    parser.add_argument(
        '--ast',
        action='store_true',
        help='Print AST and exit (for debugging)'
    )

    args = parser.parse_args()

    # Read source file
    source_path = Path(args.source_file)
    if not source_path.exists():
        print(f"Error: File '{args.source_file}' not found", file=sys.stderr)
        sys.exit(1)

    try:
        source_code = source_path.read_text()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        # Tokenize
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        if args.tokens:
            print("Tokens:")
            for token in tokens:
                print(f"  {token}")
            return

        # Parse
        parser_obj = Parser(tokens)
        ast = parser_obj.parse()

        if args.ast:
            print("AST:")
            print(ast)
            return

        # Full compilation
        python_code = compile_source(source_code, str(source_path))

        # Determine output file
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = source_path.with_suffix('.py')

        # Write output
        output_path.write_text(python_code)
        print(f"Compiled {source_path} -> {output_path}")

        # Run if requested
        if args.run:
            print("\nRunning generated code:")
            print("-" * 40)
            # Create a namespace for exec to avoid scoping issues
            namespace = {}
            exec(python_code, namespace)

    except CompilerError as e:
        print(f"Compilation error: {e}", file=sys.stderr)
        sys.exit(1)
    except (LexerError, ParserError, SemanticError) as e:
        print(f"Compilation error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
