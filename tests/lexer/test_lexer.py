"""
Unit tests for SimpleLang lexer.
"""

import unittest
import sys
sys.path.insert(0, '/Users/arturokuang/sandbox')

from compiler.lexer import Lexer, LexerError, TokenType


class TestLexer(unittest.TestCase):
    """Test cases for the lexer."""

    def test_empty_source(self):
        """Test lexing empty source code."""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)

    def test_single_number(self):
        """Test lexing a single number."""
        lexer = Lexer("123")
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 2)  # NUMBER + EOF
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, 123)

    def test_identifier(self):
        """Test lexing an identifier."""
        lexer = Lexer("my_var")
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 2)  # IDENTIFIER + EOF
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].value, "my_var")

    def test_keywords(self):
        """Test lexing keywords."""
        lexer = Lexer("int print")
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 3)  # INT + PRINT + EOF
        self.assertEqual(tokens[0].type, TokenType.INT)
        self.assertEqual(tokens[1].type, TokenType.PRINT)

    def test_operators(self):
        """Test lexing operators."""
        lexer = Lexer("+ - * / % =")
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
            TokenType.MODULO,
            TokenType.ASSIGN,
            TokenType.EOF
        ]
        self.assertEqual(len(tokens), len(expected_types))
        for token, expected_type in zip(tokens, expected_types):
            self.assertEqual(token.type, expected_type)

    def test_delimiters(self):
        """Test lexing delimiters."""
        lexer = Lexer("( ) ;")
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.LPAREN,
            TokenType.RPAREN,
            TokenType.SEMICOLON,
            TokenType.EOF
        ]
        self.assertEqual(len(tokens), len(expected_types))
        for token, expected_type in zip(tokens, expected_types):
            self.assertEqual(token.type, expected_type)

    def test_simple_declaration(self):
        """Test lexing a simple variable declaration."""
        lexer = Lexer("int x = 42;")
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.INT,
            TokenType.IDENTIFIER,
            TokenType.ASSIGN,
            TokenType.NUMBER,
            TokenType.SEMICOLON,
            TokenType.EOF
        ]
        self.assertEqual(len(tokens), len(expected_types))
        for token, expected_type in zip(tokens, expected_types):
            self.assertEqual(token.type, expected_type)

    def test_expression(self):
        """Test lexing an arithmetic expression."""
        lexer = Lexer("x + y * 2")
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.IDENTIFIER,
            TokenType.PLUS,
            TokenType.IDENTIFIER,
            TokenType.MULTIPLY,
            TokenType.NUMBER,
            TokenType.EOF
        ]
        self.assertEqual(len(tokens), len(expected_types))
        for token, expected_type in zip(tokens, expected_types):
            self.assertEqual(token.type, expected_type)

    def test_print_statement(self):
        """Test lexing a print statement."""
        lexer = Lexer("print(result);")
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.PRINT,
            TokenType.LPAREN,
            TokenType.IDENTIFIER,
            TokenType.RPAREN,
            TokenType.SEMICOLON,
            TokenType.EOF
        ]
        self.assertEqual(len(tokens), len(expected_types))
        for token, expected_type in zip(tokens, expected_types):
            self.assertEqual(token.type, expected_type)

    def test_multiline_source(self):
        """Test lexing multiline source code."""
        source = """int x = 10;
int y = 20;
print(x + y);"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # Should have proper line numbers
        self.assertEqual(tokens[0].line, 1)  # int
        self.assertEqual(tokens[5].line, 2)  # second int
        self.assertEqual(tokens[10].line, 3)  # print

    def test_whitespace_handling(self):
        """Test that whitespace is properly ignored."""
        lexer1 = Lexer("int x=10;")
        lexer2 = Lexer("int    x   =   10  ;")
        tokens1 = lexer1.tokenize()
        tokens2 = lexer2.tokenize()

        # Should produce same token types
        self.assertEqual(len(tokens1), len(tokens2))
        for t1, t2 in zip(tokens1, tokens2):
            self.assertEqual(t1.type, t2.type)
            self.assertEqual(t1.value, t2.value)

    def test_invalid_character(self):
        """Test that invalid characters raise an error."""
        lexer = Lexer("int x = @;")
        with self.assertRaises(LexerError) as context:
            lexer.tokenize()
        self.assertIn("Unexpected character", str(context.exception))

    def test_column_tracking(self):
        """Test that column numbers are tracked correctly."""
        lexer = Lexer("int x = 10;")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].column, 1)   # int at column 1
        self.assertEqual(tokens[1].column, 5)   # x at column 5
        self.assertEqual(tokens[2].column, 7)   # = at column 7
        self.assertEqual(tokens[3].column, 9)   # 10 at column 9


if __name__ == '__main__':
    unittest.main()
