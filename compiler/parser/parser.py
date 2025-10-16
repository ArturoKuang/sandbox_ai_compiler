"""
Recursive Descent Parser for SimpleLang.

Parses a stream of tokens into an Abstract Syntax Tree (AST).
"""

from typing import List, Optional
from compiler.lexer import Token, TokenType
from .ast_nodes import (
    Program, Statement, Declaration, Assignment, PrintStatement,
    IfStatement, WhileStatement,
    Expression, BinaryOp, UnaryOp, Number, Identifier, Boolean
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
                  | if_stmt
                  | while_stmt
        """
        token = self.current_token()

        # Check for declaration (starts with type keyword)
        if token.type in (TokenType.INT, TokenType.BOOL):
            return self.parse_declaration()

        # Check for print statement
        elif token.type == TokenType.PRINT:
            return self.parse_print_statement()

        # Check for if statement
        elif token.type == TokenType.IF:
            return self.parse_if_statement()

        # Check for while statement
        elif token.type == TokenType.WHILE:
            return self.parse_while_statement()

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
        # Accept either INT or BOOL type
        type_token = self.current_token()
        if type_token.type not in (TokenType.INT, TokenType.BOOL):
            raise ParserError(f"Expected type, got {type_token.type.name}", type_token)
        self.advance()
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

    def parse_if_statement(self) -> IfStatement:
        """
        if_stmt : IF LPAREN expression RPAREN LBRACE statement* RBRACE (ELSE LBRACE statement* RBRACE)?
        """
        if_token = self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)

        # Parse then block
        then_block = []
        while self.current_token().type != TokenType.RBRACE:
            then_block.append(self.parse_statement())
        self.expect(TokenType.RBRACE)

        # Parse optional else block
        else_block = None
        if self.current_token().type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.LBRACE)
            else_block = []
            while self.current_token().type != TokenType.RBRACE:
                else_block.append(self.parse_statement())
            self.expect(TokenType.RBRACE)

        return IfStatement(condition, then_block, else_block, if_token.line, if_token.column)

    def parse_while_statement(self) -> WhileStatement:
        """
        while_stmt : WHILE LPAREN expression RPAREN LBRACE statement* RBRACE
        """
        while_token = self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)

        # Parse body
        body = []
        while self.current_token().type != TokenType.RBRACE:
            body.append(self.parse_statement())
        self.expect(TokenType.RBRACE)

        return WhileStatement(condition, body, while_token.line, while_token.column)

    def parse_expression(self) -> Expression:
        """
        expression : logical_or

        Entry point for expression parsing
        """
        return self.parse_logical_or()

    def parse_logical_or(self) -> Expression:
        """
        logical_or : logical_and (OR logical_and)*
        """
        left = self.parse_logical_and()

        while self.current_token().type == TokenType.OR:
            op_token = self.advance()
            operator = op_token.value
            right = self.parse_logical_and()
            left = BinaryOp(left, operator, right, op_token.line, op_token.column)

        return left

    def parse_logical_and(self) -> Expression:
        """
        logical_and : comparison (AND comparison)*
        """
        left = self.parse_comparison()

        while self.current_token().type == TokenType.AND:
            op_token = self.advance()
            operator = op_token.value
            right = self.parse_comparison()
            left = BinaryOp(left, operator, right, op_token.line, op_token.column)

        return left

    def parse_comparison(self) -> Expression:
        """
        comparison : arithmetic ((EQ | NE | LT | LE | GT | GE) arithmetic)*
        """
        left = self.parse_arithmetic()

        while self.current_token().type in (TokenType.EQ, TokenType.NE, TokenType.LT,
                                             TokenType.LE, TokenType.GT, TokenType.GE):
            op_token = self.advance()
            operator = op_token.value
            right = self.parse_arithmetic()
            left = BinaryOp(left, operator, right, op_token.line, op_token.column)

        return left

    def parse_arithmetic(self) -> Expression:
        """
        arithmetic : term ((PLUS | MINUS) term)*

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
        term : unary ((MULTIPLY | DIVIDE | MODULO) unary)*

        This implements left-associative multiplication, division, and modulo.
        """
        left = self.parse_unary()

        while self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op_token = self.advance()
            operator = op_token.value
            right = self.parse_unary()
            left = BinaryOp(left, operator, right, op_token.line, op_token.column)

        return left

    def parse_unary(self) -> Expression:
        """
        unary : (NOT | MINUS) unary
              | factor
        """
        token = self.current_token()

        if token.type in (TokenType.NOT, TokenType.MINUS):
            op_token = self.advance()
            operator = op_token.value
            operand = self.parse_unary()
            return UnaryOp(operator, operand, op_token.line, op_token.column)

        return self.parse_factor()

    def parse_factor(self) -> Expression:
        """
        factor : NUMBER
               | TRUE
               | FALSE
               | IDENTIFIER
               | LPAREN expression RPAREN
        """
        token = self.current_token()

        # Number literal
        if token.type == TokenType.NUMBER:
            self.advance()
            return Number(token.value, token.line, token.column)

        # Boolean literals
        elif token.type == TokenType.TRUE:
            self.advance()
            return Boolean(True, token.line, token.column)

        elif token.type == TokenType.FALSE:
            self.advance()
            return Boolean(False, token.line, token.column)

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
