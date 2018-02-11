from lexer import *

@token(r'[a-zA-Z_]+[a-zA-Z_0-9]*')
def t_name(t):return {}

@token(r'[\!\@\#\$\%\^\&\*\>\<\~\+\-\=\\\/]+')
def t_op(t):return {}

@token('ignore in',' \n\t')
def t_ignore(t):return {}

@token(r'[0-9]+')
def t_int(t):return {}

@token(r'([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)')
def t_float(t):return {}

@token(r'\.')
def t_dot(t):return {}

@token('in','()')
def t_paren(t):return {}

@token(r',')
def t_comma(t):return {}

@token(r';')
def t_semicolon(t):return {}

mats = [
    t_name,
    t_op,
    t_ignore,
    t_float,
    t_int,
    t_paren,
    t_dot,
    t_comma,
    ]
def make(code):
    global mats
    return tokenize(mats,code)
