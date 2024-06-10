def analizar_semantica_programa(resultado_sintactico):
    if not resultado_sintactico or 'errores' in resultado_sintactico:
        return {'errores': 'Errores sintácticos encontrados'}

    ast = resultado_sintactico.get('resultado')

    # Tabla de símbolos para almacenar variables declaradas
    tabla_de_simbolos = {}

    def procesar_statement(statement, tabla_de_simbolos):
        if statement[0] == 'for_statement':
            # Obtener las partes del bucle for
            _, asignacion, condicion, incremento, cuerpo = statement
            # Realizar análisis semántico en la asignación
            validar_asignacion(asignacion, tabla_de_simbolos)
            # Realizar análisis semántico en la condición
            validar_expresion(condicion, tabla_de_simbolos)
            # Realizar análisis semántico en el incremento
            validar_asignacion(incremento, tabla_de_simbolos)
            # Realizar análisis semántico en el cuerpo del bucle
            validar_cuerpo_compuesto(cuerpo, tabla_de_simbolos)

    if ast and ast[0] == 'program':
        # Obtener los elementos relevantes del AST
        statement_list = ast[1]

        # Realizar análisis semántico
        for statement in statement_list:
            procesar_statement(statement, tabla_de_simbolos)

    # Verificar si la variable 'i' está en la tabla de símbolos
    if 'i' in tabla_de_simbolos:
        print("La variable 'i' está presente en la tabla de símbolos.")
    else:
        print("La variable 'i' no está presente en la tabla de símbolos.")

    # Si no se encontraron errores, devolver un mensaje de éxito
    return {'resultado': 'Análisis semántico exitoso'}

# Funciones auxiliares para el análisis semántico
def validar_asignacion(asignacion, tabla_de_simbolos):
    if asignacion[0] == 'assignment_expression':
        # Verificar si la variable está declarada
        variable = asignacion[1]
        if variable not in tabla_de_simbolos:
            raise Exception(f"Error: Variable '{variable}' no declarada antes de usarla")

def validar_expresion(expresion, tabla_de_simbolos):
    # Validar variables utilizadas en la expresión
    for var in extraer_variables(expresion):
        if var not in tabla_de_simbolos:
            raise Exception(f"Error: Variable '{var}' no declarada antes de usarla")

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

def validar_cuerpo_compuesto(compound, tabla_de_simbolos):
    if compound[0] == 'compound_statement':
        for stmt in compound[1]:
            if stmt[0] == 'declaration_statement':
                # Agregar las variables declaradas a la tabla de símbolos
                tabla_de_simbolos[stmt[2]] = stmt[1]
            elif stmt[0] == 'expression_statement':
                # Validar variables utilizadas en expresiones
                for var in extraer_variables(stmt[1]):
                    if var not in tabla_de_simbolos:
                        raise Exception(f"Error: Variable '{var}' no declarada antes de usarla")
