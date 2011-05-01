import ply.lex

tokens = ('LPAREN', 'RPAREN', 'SYMBOL', 'INTEGER', 'BOOLEAN', 'FLOATING_POINT', 'COMMENT', 'CHARACTER', 'STRING')

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SYMBOL = r'[a-zA-Z*+/!?=<>.-]+' # TODO: check against R5RS docs

def t_STRING(t):
    r'"(\\"|[a-zA-Z*+/!?=<>. -])*"'
    # strip leading and trailing doublequote from input
    t.value = t.value[1:-1]

    t.value = t.value.replace('\\"', '"')
    return t

def t_FLOATING_POINT(t):
    r"([0-9]*\.[0-9]+)|([0-9]+\.[0-9]*)"
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_BOOLEAN(t):
    r'\#t|\#f'
    if t.value == "#t":
        t.value = True
    else:
        t.value = False

    return t

def t_CHARACTER(t):
    r'\#\\(space|newline|.)'
    # throw away leading #\
    t.value = t.value[2:]

    if t.value == 'space':
        t.value = ' '
    elif t.value == 'newline':
        t.value = '\n'

    return t

def t_COMMENT(t):
    r";[^\n]*"
    # throw away all comments during lexing
    pass

t_ignore = ' \t\n'

lexer = ply.lex.lex()

