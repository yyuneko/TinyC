import os

import ply.yacc as yacc

import classes
import lexer
import node
from lexer import Lexer
from CMFile.read import read_file_as_str

precedence = (
    ('left', 'LOR'),
    ('right', 'LAND'),
    ('left', 'PLUS', 'MINUS'),
    ('right', 'TIMES', 'DIVIDE'),
    ('left', 'MODULO')
)


# def p_test(p):
#     """
#     TEST : NUM
#     """
#     p[0] = {"value": p[1]}
#     print(p[0])


def p_PROGRAM(p):
    """
    MAIN : PROGRAM ID LBRACE VARIABLEDECLARATION STATEMENTS RBRACE
    """
    p[0] = [classes.Function()]


def p_VARIABLEDECLARATION(p):
    """
    VARIABLEDECLARATION : TYPE NULLSIGN VARIABLES SEMI VARIABLEDECLARATION
                        |
    """


def p_TYPE(p):
    """
    TYPE : INT
         | FLOAT
    """


def p_NULLSIGN(p):
    """
    NULLSIGN : TERNARY
             |
    """


def p_ARRAY(p):
    """
    ARRAY : LBRACKET EXPRESSION RBRACKET ARRAY
          |
    """


def p_VARIABLE(p):
    """
    VARIABLE : ID ARRAY
    """


def p_VARIABLES(p):
    """
    VARIABLES : VARIABLE COMMA VARIABLES
              | VARIABLE
    """


def p_STATEMENTS(p):
    """
    STATEMENTS : STATEMENT STATEMENTS
               |
    """


def p_STATEMENT(p):
    """
    STATEMENT : ASSIGNMENT SEMI
              | BLOCK
              | IFSTATEMENT
              | FORSTATEMENT
    """


def p_ASSIGNMENT(p):
    """
    ASSIGNMENT : VARIABLE EQUALS EXPRESSION
    """


def p_BLOCK(p):
    """
    BLOCK : LBRACE  STATEMENTS  RBRACE
    """


def p_EXPRESSION(p):
    """
    EXPRESSION : EXPRESSION PLUS EXPRESSION
               | EXPRESSION MINUS EXPRESSION
               | EXPRESSION TIMES EXPRESSION
               | EXPRESSION DIVIDE EXPRESSION
               | EXPRESSION MODULO EXPRESSION
               | FACTOR
    """
    if len(p) == 4:
        p[0] = classes.ExpressionArithmetic(p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = p[1]


def p_FACTOR_ID(p):
    """
        FACTOR : ID
    """
    p[0] = classes.Identifier(p[1])


def p_FACTOR_NUM(p):
    """
        FACTOR : NUM
    """
    p[0] = classes.Num(p[1])


def p_FACTOR_REAL(p):
    """
        FACTOR : REAL
    """
    p[0] = classes.Real(p[1])


def p_FACTOR(p):
    """
    FACTOR : LPAREN EXPRESSION RPAREN
           | ID LBRACKET EXPRESSION RBRACKET ARRAY
    """
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 6:
        if p:
            pass
        else:
            # todo
            pass


def p_CONDITION(p):
    """
    CONDITION : CONDITION LAND CONDITION
              | EXPRESSION RELATIONALOPERATOR EXPRESSION
              | CONDITION LOR CONDITION
    """


def p_IFSTATEMENT(p):
    """
    IFSTATEMENT : IF LPAREN  CONDITION RPAREN   STATEMENT  ELSE  STATEMENT
    """


def p_RELATIONALOPERATOR(p):
    """
    RELATIONALOPERATOR : GT
                       | LT
                       | EQ
                       | NE
                       | GE
                       | LE
    """


def p_FORSTATEMENT(p):
    """
    FORSTATEMENT : FOR LPAREN  ID IN NUM DPERIOD NUM RPAREN  STATEMENT
    """


def p_error(p):
    if p:
        pass
    else:
        print("Syntax error in input!")


tokens = lexer.tokens
parser = yacc.yacc(debug=1, method='SLR')


# lexer = Lexer(read_file_as_str(os.path.realpath("./test/test_lexer.in")))
# tokens = lexer.get_tokens()


class Parser:
    def __init__(self, input):
        self.input = input
        # self.lexer = Lexer(self.input).lexer
        self.out = parser.parse(input)
        self.generator = node.Node(self.out)

    def gen_code_3d(self):
        pass


p = Parser(read_file_as_str(os.path.realpath("./test/test_lexer.in")))
print(p.out)
