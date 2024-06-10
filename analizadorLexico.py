import ply.lex as lex

# Lista de tokens
tokens = (
    'ID', 'NUMBER', 'FLOAT', 'PLUS', 'EQUALS', 'LE', 'LESS', 'GE', 'GREATER', 'EQ', 'NEQ', 
    'PLUSPLUS', 'TYPE', 'FOR', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'DOT', 
    'TIMES'
)

# Palabras reservadas
reserved = {
    'for': 'FOR',
    'int': 'TYPE',
    'float': 'TYPE',
    'System': 'ID',
    'out': 'ID',
    'println': 'ID'
}

identifiers = []

# Definición de tokens
t_PLUS = r'\+'
t_EQUALS = r'='
t_LE = r'<='
t_LESS = r'<'
t_GE = r'>='
t_GREATER = r'>'
t_EQ = r'=='
t_NEQ = r'!='
t_PLUSPLUS = r'\+\+'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_DOT = r'\.'
t_TIMES = r'\*'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Chequea palabras reservadas
    if t.type == 'ID' and t.value not in identifiers:
        identifiers.append(t.value)  # Agregar identificador a la tabla de símbolos
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

def analizar_codigo(codigo):
    lexer.input(codigo)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append({
            'type': tok.type,
            'value': tok.value,
            'lineno': tok.lineno,
            'lexpos': tok.lexpos
        })
    return tokens
