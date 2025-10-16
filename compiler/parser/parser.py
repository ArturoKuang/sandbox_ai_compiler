"""
Recursive Descent Parser for SimpleLang.

Parses a stream of tokens into an Abstract Syntax Tree (AST).
"""

from typing import List, Optional
from compiler.lexer import Token, TokenType
from .ast_nodes import (
    Program, Statement, Declaration, Assignment, PrintStatement,
    IfStatement, WhileStatement, ForStatement, FunctionDeclaration, ReturnStatement,
    Expression, BinaryOp, UnaryOp, Number, Identifier, Boolean,
    ArrayLiteral, ArrayAccess, FunctionCall
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
                  | for_stmt
                  | function_decl
                  | return_stmt
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

        # Check for for statement
        elif token.type == TokenType.FOR:
            return self.parse_for_statement()

        # Check for function declaration
        elif token.type == TokenType.FUNCTION:
            return self.parse_function_declaration()

        # Check for return statement
        elif token.type == TokenType.RETURN:
            return self.parse_return_statement()

        # Check for assignment (starts with identifier)
        elif token.type == TokenType.IDENTIFIER:
            # Could be assignment or array assignment
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
        assignment : IDENTIFIER (LBRACKET expression RBRACKET)? ASSIGN expression SEMICOLON

        Note: Array element assignment is handled by treating arr[i] = value as a special form
        """
        id_token = self.expect(TokenType.IDENTIFIER)
        name = id_token.value

        # Check for array element assignment
        if self.current_token().type == TokenType.LBRACKET:
            self.advance()
            index = self.parse_expression()
            self.expect(TokenType.RBRACKET)
            self.expect(TokenType.ASSIGN)
            value = self.parse_expression()
            self.expect(TokenType.SEMICOLON)

            # Create a special identifier name for array element assignment
            # We'll handle this in codegen by detecting the pattern
            # For now, store the array access node as a special assignment target
            # We need to extend Assignment node, but for now use a workaround
            # Store name as "name[index_expr]" - will need special handling in codegen
            return Assignment(name + "[INDEX]", value, id_token.line, id_token.column)

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

    def parse_for_statement(self) -> ForStatement:
        """
        for_stmt : FOR LPAREN (declaration | assignment)? SEMICOLON expression? SEMICOLON (assignment)? RPAREN LBRACE statement* RBRACE
        """
        for_token = self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)

        # Parse init (optional)
        init = None
        if self.current_token().type != TokenType.SEMICOLON:
            if self.current_token().type in (TokenType.INT, TokenType.BOOL):
                init = self.parse_declaration()
                # Declaration already consumes the semicolon, so we skip expecting it
            else:
                init = self.parse_assignment()
                # Assignment already consumes the semicolon
        else:
            self.advance()  # skip semicolon

        # Parse condition (optional)
        condition = None
        if self.current_token().type != TokenType.SEMICOLON:
            condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        # Parse update (optional)
        update = None
        if self.current_token().type != TokenType.RPAREN:
            # For update, we parse as assignment but without semicolon
            id_token = self.expect(TokenType.IDENTIFIER)
            name = id_token.value
            self.expect(TokenType.ASSIGN)
            value = self.parse_expression()
            update = Assignment(name, value, id_token.line, id_token.column)

        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)

        # Parse body
        body = []
        while self.current_token().type != TokenType.RBRACE:
            body.append(self.parse_statement())
        self.expect(TokenType.RBRACE)

        return ForStatement(init, condition, update, body, for_token.line, for_token.column)

    def parse_function_declaration(self) -> FunctionDeclaration:
        """
        function_decl : FUNCTION IDENTIFIER LPAREN params RPAREN LBRACE statement* RBRACE
        params : (type IDENTIFIER (COMMA type IDENTIFIER)*)?
        """
        func_token = self.expect(TokenType.FUNCTION)
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value

        self.expect(TokenType.LPAREN)

        # Parse parameters
        params = []
        if self.current_token().type in (TokenType.INT, TokenType.BOOL):
            # First parameter
            param_type_token = self.current_token()
            if param_type_token.type not in (TokenType.INT, TokenType.BOOL):
                raise ParserError(f"Expected type, got {param_type_token.type.name}", param_type_token)
            self.advance()
            param_type = param_type_token.value

            param_name_token = self.expect(TokenType.IDENTIFIER)
            param_name = param_name_token.value
            params.append((param_type, param_name))

            # Remaining parameters
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                param_type_token = self.current_token()
                if param_type_token.type not in (TokenType.INT, TokenType.BOOL):
                    raise ParserError(f"Expected type, got {param_type_token.type.name}", param_type_token)
                self.advance()
                param_type = param_type_token.value

                param_name_token = self.expect(TokenType.IDENTIFIER)
                param_name = param_name_token.value
                params.append((param_type, param_name))

        self.expect(TokenType.RPAREN)

        # For simplicity, assume return type is int (we can enhance this later)
        return_type = "int"

        self.expect(TokenType.LBRACE)

        # Parse body
        body = []
        while self.current_token().type != TokenType.RBRACE:
            body.append(self.parse_statement())
        self.expect(TokenType.RBRACE)

        return FunctionDeclaration(name, params, return_type, body, func_token.line, func_token.column)

    def parse_return_statement(self) -> ReturnStatement:
        """
        return_stmt : RETURN expression? SEMICOLON
        """
        return_token = self.expect(TokenType.RETURN)

        expression = None
        if self.current_token().type != TokenType.SEMICOLON:
            expression = self.parse_expression()

        self.expect(TokenType.SEMICOLON)

        return ReturnStatement(expression, return_token.line, return_token.column)

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
               | IDENTIFIER (LBRACKET expression RBRACKET | LPAREN args RPAREN)?
               | LBRACKET array_elements RBRACKET
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

        # Identifier (variable reference, array access, or function call)
        elif token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()

            # Check for array access
            if self.current_token().type == TokenType.LBRACKET:
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                return ArrayAccess(Identifier(name, token.line, token.column), index, token.line, token.column)

            # Check for function call
            elif self.current_token().type == TokenType.LPAREN:
                self.advance()
                arguments = []
                if self.current_token().type != TokenType.RPAREN:
                    arguments.append(self.parse_expression())
                    while self.current_token().type == TokenType.COMMA:
                        self.advance()
                        arguments.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
                return FunctionCall(name, arguments, token.line, token.column)

            # Just an identifier
            else:
                return Identifier(name, token.line, token.column)

        # Array literal
        elif token.type == TokenType.LBRACKET:
            self.advance()
            elements = []
            if self.current_token().type != TokenType.RBRACKET:
                elements.append(self.parse_expression())
                while self.current_token().type == TokenType.COMMA:
                    self.advance()
                    elements.append(self.parse_expression())
            self.expect(TokenType.RBRACKET)
            return ArrayLiteral(elements, token.line, token.column)

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
