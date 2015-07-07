import ply.lex as lex

tokens = (
    #Punctuation
    'COMMENT',
    'OPCODE',
    'CONDITION',
    'COMMA',
    'DOT',
    'COLON',
    'NEWLINE',
    
    #Operands
    'REGISTER',
    'LABEL',
    'LITERAL',
    
    #Separators
    'LBRACKET',
    'RBRACKET',
    'LPAREN',
    'RPAREN'
)

t_ignore = ' \t'

t_COMMA = r','

t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore_COMMENT = r';.*'

def t_REGISTER(t):
    r'r\d{0,2}'
    t.value = int(t.value[1:])
    return t
    
def t_LABEL(t):
    r'\$[a-zA-Z][a-zA-Z0-9]+'
    t.value = t.value[1:]
    return t
    
def t_LITERAL(t):
    r'\#\d+'
    t.value = int(t.value[1:])
    return t

def t_OPCODE(t):
    r'[a-zA-Z]+(?=[\s\.])'
    t.value = t.value.lower()
    return t
    
def t_CONDITION(t):
    r'\.[a-zA-Z]+(?=\s)'
    #Ignore the preceding dot
    t.value = t.value[1:].lower()
    return t
    
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += len(t.value)
    return t
    
def t_error(t):
    print("Illegal character: {0}".format(t.value))
    t.lexer.skip(1)
    
lexer = lex.lex()

#data = """add.eq r1, r3
#sub r2, [$mem]
#add r2, #3"""

#lexer.input(data)

#for tok in lexer:
#    print(tok)
    
