"""
Recursive Descent Parser for SimpleLang.

Parses a stream of tokens into an Abstract Syntax Tree (AST).
"""

from typing import List, Optional
from compiler.lexer import Token, TokenType
from .ast_nodes import (
    Program, Statement, Declaration, Assignment, PrintStatement,
    Expression, BinaryOp, Number, Identifier
)


class ParserError(Exception):
    """Raised when parser encounters a syntax error."""

    def __init__(self, message: str, token: Token):
        super().__init__(f"Parser error at {token.line}:{token.column}: {message}")
        self.token = token


class Parser:
    """Recursive descent parser for SimpleLang."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        """Returns the current token."""
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.pos]

    def peek_token(self, offset: int = 1) -> Token:
        """Peeks ahead at a token without consuming it."""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[pos]

    def advance(self) -> Token:
        """Consumes and returns the current token."""
        token = self.current_token()
        if self.pos < len(self.tokens) - 1:  # Don't advance past EOF
            self.pos += 1
        return token

    def expect(self, token_type: TokenType) -> Token:
        """Consumes a token of the expected type or raises an error."""
        token = self.current_token()
        if token.type != token_type:
            raise ParserError(
                f"Expected {token_type.name}, got {token.type.name}",
                token
            )
        return self.advance()

    def parse(self) -> Program:
        """Parses the entire program."""
        return self.parse_program()

    def parse_program(self) -> Program:
        """
        program : statement_list
        """
        statements = []
        while self.current_token().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self) -> Statement:
        """
        statement : declaration
                  | assignment
                  | print_stmt
        """
        token = self.current_token()

        # Check for declaration (starts with type keyword)
        if token.type == TokenType.INT:
            return self.parse_declaration()

        # Check for print statement
        elif token.type == TokenType.PRINT:
            return self.parse_print_statement()

        # Check for assignment (starts with identifier)
        elif token.type == TokenType.IDENTIFIER:
            return self.parse_assignment()

        else:
            raise ParserError(
                f"Unexpected token {token.type.name}, expected statement",
                token
            )

    def parse_declaration(self) -> Declaration:
        """
        declaration : type IDENTIFIER ASSIGN expression SEMICOLON
        """
        type_token = self.expect(TokenType.INT)
        var_type = type_token.value

        id_token = self.expect(TokenType.IDENTIFIER)
        name = id_token.value

        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        return Declaration(var_type, name, value, type_token.line, type_token.column)

    def parse_assignment(self) -> Assignment:
        """
        assignment : IDENTIFIER ASSIGN expression SEMICOLON
        """
        id_token = self.expect(TokenType.IDENTIFIER)
        name = id_token.value

        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        return Assignment(name, value, id_token.line, id_token.column)

    def parse_print_statement(self) -> PrintStatement:
        """
        print_stmt : PRINT LPAREN expression RPAREN SEMICOLON
        """
        print_token = self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        expr = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)

        return PrintStatement(expr, print_token.line, print_token.column)

    def parse_expression(self) -> Expression:
        """
        expression : term ((PLUS | MINUS) term)*

        This implements left-associative addition and subtraction.
        """
        left = self.parse_term()

        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self.advance()
            operator = op_token.value
            right = self.parse_term()
            left = BinaryOp(left, operator, right, op_token.line, op_token.column)

        return left

    def parse_term(self) -> Expression:
        """
        term : factor ((MULTIPLY | DIVIDE | MODULO) factor)*

        This implements left-associative multiplication, division, and modulo.
        """
        left = self.parse_factor()

        while self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op_token = self.advance()
            operator = op_token.value
            right = self.parse_factor()
            left = BinaryOp(left, operator, right, op_token.line, op_token.column)

        return left

    def parse_factor(self) -> Expression:
        """
        factor : NUMBER
               | IDENTIFIER
               | LPAREN expression RPAREN
        """
        token = self.current_token()

        # Number literal
        if token.type == TokenType.NUMBER:
            self.advance()
            return Number(token.value, token.line, token.column)

        # Identifier (variable reference)
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(token.value, token.line, token.column)

        # Parenthesized expression
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr

        else:
            raise ParserError(
                f"Unexpected token {token.type.name}, expected expression",
                token
            )
