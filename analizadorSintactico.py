import ply.yacc as yacc
from analizadorLexico import tokens

# Tabla de símbolos
tabla_de_simbolos = {}

# Definición de la gramática
def p_program(p):
    '''program : statement_list'''
    print("program -> statement_list")
    p[0] = ("program", p[1])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        print("statement_list -> statement_list statement")
        p[0] = p[1] + [p[2]]
    else:
        print("statement_list -> statement")
        p[0] = [p[1]]

def p_statement(p):
    '''statement : expression_statement
                 | compound_statement
                 | declaration_statement
                 | for_statement
                 | method_call_statement'''
    print("statement -> ", p.slice[1].type)
    p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON'''
    print("expression_statement -> expression SEMICOLON")
    p[0] = ("expression_statement", p[1])

def p_declaration_statement(p):
    '''declaration_statement : TYPE ID SEMICOLON
                             | TYPE ID EQUALS expression SEMICOLON'''
    if len(p) == 4:
        print("declaration_statement -> TYPE ID SEMICOLON")
        tabla_de_simbolos[p[2]] = p[1]
        p[0] = ("declaration_statement", p[1], p[2])
    else:
        print("declaration_statement -> TYPE ID EQUALS expression SEMICOLON")
        tabla_de_simbolos[p[2]] = p[1]
        p[0] = ("declaration_statement", p[1], p[2], p[4])

def p_compound_statement(p):
    '''compound_statement : LBRACE statement_list RBRACE'''
    print("compound_statement -> LBRACE statement_list RBRACE")
    p[0] = ("compound_statement", p[2])

def p_for_statement(p):
    '''for_statement : FOR LPAREN assignment_expression SEMICOLON expression SEMICOLON assignment_expression RPAREN compound_statement'''
    print("for_statement -> FOR LPAREN assignment_expression SEMICOLON expression SEMICOLON assignment_expression RPAREN compound_statement")

    p[0] = ("for_statement", p[3], p[5], p[7], p[9])

    print("Sintaxis FOR Correcta")
    p.parser.sintaxis_for_correcta = True



def p_expression(p):
    '''expression : assignment_expression
                  | additive_expression
                  | relational_expression'''
    print("expression -> ", p.slice[1].type)
    p[0] = p[1]

def p_assignment_expression(p):
    '''assignment_expression : ID EQUALS expression
                             | ID PLUSPLUS'''
    if len(p) == 4:
        print("assignment_expression -> ID EQUALS expression")
        validar_variable(p[1])
        p[0] = ("assignment_expression", p[1], p[3])
    else:
        print("assignment_expression -> ID PLUSPLUS")
        validar_variable(p[1])
        p[0] = ("increment_expression", p[1])

def p_relational_expression(p):
    '''relational_expression : expression LE expression
                             | expression LESS expression
                             | expression GE expression
                             | expression GREATER expression
                             | expression EQ expression
                             | expression NEQ expression'''
    print(f"relational_expression -> {p[2]}")
    p[0] = ("relational_expression", p[1], p[2], p[3])

def p_additive_expression(p):
    '''additive_expression : additive_expression PLUS multiplicative_expression
                           | multiplicative_expression'''
    if len(p) == 4:
        print("additive_expression -> additive_expression PLUS multiplicative_expression")
        p[0] = ("additive_expression", p[1], p[3])
    else:
        print("additive_expression -> multiplicative_expression")
        p[0] = p[1]

def p_multiplicative_expression(p):
    '''multiplicative_expression : multiplicative_expression TIMES primary_expression
                                 | primary_expression'''
    if len(p) == 4:
        print("multiplicative_expression -> multiplicative_expression TIMES primary_expression")
        p[0] = ("multiplicative_expression", p[1], p[3])
    else:
        print("multiplicative_expression -> primary_expression")
        p[0] = p[1]

def p_primary_expression(p):
    '''primary_expression : ID
                          | NUMBER
                          | FLOAT
                          | LPAREN expression RPAREN
                          | method_call'''
    if len(p) == 2:
        print("primary_expression -> ", p.slice[1].type)
        if p[1] in tabla_de_simbolos or p.slice[1].type in ['NUMBER', 'FLOAT']:
            p[0] = ("primary_expression", p[1])
        else:
            raise Exception(f"Error: Variable '{p[1]}' no declarada antes de usarla")
    else:
        print("primary_expression -> LPAREN expression RPAREN")
        p[0] = p[2]

def p_method_call(p):
    '''method_call : ID DOT ID DOT ID LPAREN RPAREN
                   | ID DOT ID DOT ID LPAREN expression RPAREN'''
    if len(p) == 8:
        print("method_call -> ID DOT ID DOT ID LPAREN RPAREN")
        p[0] = ("method_call", p[1], p[3], p[5])
    else:
        print("method_call -> ID DOT ID DOT ID LPAREN expression RPAREN")
        p[0] = ("method_call", p[1], p[3], p[5], p[7])

def p_method_call_statement(p):
    '''method_call_statement : method_call SEMICOLON'''
    print("method_call_statement -> method_call SEMICOLON")
    p[0] = ("method_call_statement", p[1])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' en la línea {p.lineno}")
    else:
        print("Syntax error at EOF")

# Construcción del parser
parser = yacc.yacc()

# Funciones auxiliares para la validación de variables
def validar_variable(variable):
    if variable not in tabla_de_simbolos:
        raise Exception(f"Error: Variable '{variable}' no declarada antes de usarla")

def extraer_variables(expresion):
    # Función auxiliar para extraer todas las variables de una expresión
    variables = []
    if isinstance(expresion, tuple):
        if expresion[0] == 'primary_expression' and isinstance(expresion[1], str):
            variables.append(expresion[1])
        else:
            for elemento in expresion:
                variables.extend(extraer_variables(elemento))
    return variables

def validar_asignacion(asignacion):
    if asignacion[0] == 'assignment_expression':
        if asignacion[2] == 'EQUALS':
            validar_variable(asignacion[1])
        elif asignacion[2] == 'PLUSPLUS':
            validar_variable(asignacion[1])
        else:
            raise Exception(f"Error: Asignación no reconocida en la estructura FOR")

def validar_expresion(expresion):
    if expresion[0] == 'relational_expression':
        for var in extraer_variables(expresion):
            validar_variable(var)

def validar_cuerpo_compuesto(compound):
    if compound[0] == 'compound_statement':
        for stmt in compound[1]:
            if stmt[0] == 'expression_statement':
                for var in extraer_variables(stmt[1]):
                    validar_variable(var)
            elif stmt[0] == 'declaration_statement':
                tabla_de_simbolos[stmt[2]] = stmt[1]

def analizar_sintaxis(codigo):
    resultado = None
    errores = []
    parser.sintaxis_for_correcta = False

    try:
        resultado = parser.parse(codigo, tracking=True)
    except Exception as e:
        errores.append(str(e))

    return {
        'sintactico': {
            'resultado': resultado,
            'errores': errores,
            'mensaje': "Sintaxis FOR Correcta" if not errores else "Sintaxis FOR Incorrecta"
        },
        'sintaxis_for_correcta': parser.sintaxis_for_correcta
    }

