from flask import Flask, request, jsonify
from flask_cors import CORS
import analizadorLexico
import analizadorSintactico
import analizadorSemantico

app = Flask(__name__)
CORS(app)

@app.route('/lexico', methods=['POST'])
def analisis_lexico():
    codigo = request.json.get('textarea_content', '')
    tokens = analizadorLexico.analizar_codigo(codigo)
    return jsonify({'tokens': tokens})

@app.route('/sintactico', methods=['POST'])
def analisis_sintactico():
    codigo = request.json.get('textarea_content', '')
    resultado_sintactico = analizadorSintactico.analizar_sintaxis(codigo)
    return jsonify(resultado_sintactico)

@app.route('/semantico', methods=['POST'])
def analisis_semantico():
    codigo = request.json.get('textarea_content', '')
    resultado_sintactico = analizadorSintactico.analizar_sintaxis(codigo)
    if 'errores' not in resultado_sintactico:
        resultado_semantico = analizadorSemantico.analizar_semantica_programa(resultado_sintactico)
        return jsonify(resultado_semantico)
    else:
        return jsonify(resultado_sintactico)

if __name__ == '__main__':
    app.run(debug=True)
