import ply.lex
import ply.lex as lex
import CMFile as cmf
import CMFile.read


class Style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


tokens = (
    # Program
    'PROGRAM',
    # Literals (identifier, integer=<NUM> , float=<REAL> constant, string constant, char const)
    'ID', 'NUM', 'NUM_OCT', 'NUM_HEX', 'REAL',

    # Operators (+,-,*,/,%,|,&,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
    'LOR', 'LAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

    # Assignment (=, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |= , :=)
    'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
    'LSHIFTEQUAL', 'RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL', 'COLONEQUAL',

    # Increment/decrement (++,--)
    'INCREMENT', 'DECREMENT',

    # Delimeters ( ) [ ] { } , .. ; :
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'DPERIOD', 'SEMI',

    # Ellipsis (...)
    'ELLIPSIS',

    # Ternary operator (?)
    'TERNARY',

    'IGNORE',
)

keywords = {
    # 'program':'PROGRAM',
    'int': 'INT',
    'float': 'FLOAT',
    'for': 'FOR',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'in': 'IN'
}

tokens += tuple(keywords.values())


def t_PROGRAM(t):
    r'[Pp][Rr][Oo][Gg][Rr][Aa][Mm]'
    return t


def t_INT(t):
    r'[Ii][Nn][Tt]'
    return t


def t_FLOAT(t):
    r'[Ff][Ll][Oo][Aa][Tt]'
    return t


def t_FOR(t):
    r'[Ff][Oo][Rr]'
    return t


def t_IF(t):
    r'[iI][fF]'
    return t


def t_ELSE(t):
    r'[Ee][Ll][Ss][Ee]'
    return t


def t_WHILE(t):
    r'[wW][hH][iI][lL][eE]'
    return t


def t_IN(t):
    r'[iI][nN]'
    return t


# Identifiers

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    # if t.value in keywords:
    #     t.type = t.value
    return t


def t_NUM_OCT(t):
    r'(0)(\d+)'

    if len(t.value) > 15:
        return t_error(t)
    t.type = "NUM"
    t.value = int(t.value, 8)
    return t


def t_NUM_HEX(t):
    r'(0x)(\d+)'
    if len(t.value) > 15:
        return t_error(t)
    t.value = int(t.value, 16)
    t.type = "NUM"
    return t


def t_REAL(t):
    r'\d+\.\d+'
    if len(t.value) > 15:
        return t_error(t)
    return t


def t_NUM(t):
    r'(\d+)'
    if len(t.value) > 15:
        return t_error(t)
    return t


t_ignore = r' '
t_ignore_IGNORE = r'\t'

# Delimeters
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_DPERIOD = r'\.\.'
t_SEMI = r';'
t_ELLIPSIS = r'\.\.\.'

t_TERNARY = r'\?'

# Assignment operators

t_EQUALS = r'='
t_TIMESEQUAL = r'\*='
t_DIVEQUAL = r'/='
t_MODEQUAL = r'%='
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'-='
t_LSHIFTEQUAL = r'<<='
t_RSHIFTEQUAL = r'>>='
t_ANDEQUAL = r'&='
t_OREQUAL = r'\|='
t_XOREQUAL = r'\^='
t_COLONEQUAL = r'\:='
# Increment/decrement
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'


def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)


def t_CPPCOMMENT(t):
    r'(//.*)(\n)'
    t.lexer.lineno += 1
    t.value = t.value.strip()
    return t


def t_error(t):
    if t.type == "error":
        print(Style.GREEN + "TOKEN ERROR:\n" + "\tIllegal character {0} ,Line {1} Error ".format(t.value[0], t.lineno))
        # import linecache
        # linecache = linecache.getline(file, t.lineno).strip()
        # if lineFirsTok.lineno != t.lineno:
        #     lineFirsTok.lineno = t.lineno
        #     lineFirsTok.lexpos = t.lexpos
        # pos = t.lexpos - lineFirsTok.lexpos
        # print(Style.YELLOW + linecache[0:pos] + Style.RED + linecache[pos] + Style.YELLOW + linecache[pos + 1:])

    if t.type == "NUM":
        print(Style.GREEN + "NUM ERROR:\n" + "\tIllegal initial \"{0}\" ,Line {1} Error ".format(t.value, t.lineno))
        # import linecache
        # linecache = linecache.getline(file, t.lineno).strip()
        # pos = t.lexpos - lineFirsTok.lexpos
        # print(
        #     Style.YELLOW + linecache[0:pos] + Style.RED + linecache[pos: pos + len(t.value)] + Style.YELLOW + linecache[
        #                                                                                                       pos + len(
        #                                                                                                           t.value) + 1:])

    if t.type == "REAL":
        print(Style.GREEN + "NUM ERROR:\n" + "\tIllegal initial \"{0}\" ,Line {1} Error ".format(t.value, t.lineno))
        # import linecache
        # linecache = linecache.getline(file, t.lineno).strip()
        # pos = t.lexpos - lineFirsTok.lexpos
        # print(
        #     Style.YELLOW + linecache[0:pos] + Style.RED + linecache[pos: pos + len(t.value)] + Style.YELLOW + linecache[
        #                                                                                                       pos + len(
        #                                                                                                           t.value) + 1:])
    t.lexer.skip(1)


# Operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_OR = r'\|'
t_AND = r'&'
t_NOT = r'~'
t_XOR = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_LOR = r'\|\|'
t_LAND = r'&&'
t_LNOT = r'!'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

lexer=lex.lex()
class Lexer:
    def __init__(self, input):
        self.input = input
        self.lexer = lex.lex()
        self.line_first_token = None
        # self.lexer.input(self.input)

    def token(self):
        tok = self.lexer.token()
        return tok

    def get_tokens(self):
        toks = []
        tok = self.line_first_token = self.lexer.token()
        toks.append(tok)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            toks.append(tok)
        return toks
