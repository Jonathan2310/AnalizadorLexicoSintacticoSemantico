import Title from "../components/atoms/Tittle";
import styled from "styled-components";
import Button from "../components/atoms/Button";
import { useState } from "react";

function Home() {
    const [texto, setTexto] = useState("");
    const [analisisLexico, setAnalisisLexico] = useState("");
    const [analisisSintactico, setAnalisisSintactico] = useState("");
    const [analisisSemantico, setAnalisisSemantico] = useState("");
    const [error, setError] = useState("");
    const [tablaTokens, setTablaTokens] = useState([]);

    const handleBorrarAnalisisLexico = () => {
        setTexto("");
        setAnalisisLexico("");
        setError("");
        setTablaTokens([]);
    };

    const handleBorrarAnalisisSintactico = () => {
        setTexto("");
        setAnalisisSintactico("");
        setError("");
    };

    const handleBorrarAnalisisSemantico = () => {
        setTexto("");
        setAnalisisSemantico("");
        setError("");
    };

    const handleAnalisisLexico = async () => {
        try {
            const response = await fetch("http://localhost:5000/lexico", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ textarea_content: texto }),
            });
    
            const data = await response.json();
            if (data.error) {
                setError(data.error);
            } else {
                setAnalisisLexico(formatAnalisisLexico(data.tokens));
                setTablaTokens(createTablaTokens(data.tokens));
                setError("");
            }
        } catch (error) {
            setError("Error de conexión con el servidor");
        }
    };

    const handleAnalisisSintactico = async () => {
        try {
            const response = await fetch("http://localhost:5000/sintactico", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ textarea_content: texto }),
            });
    
            const data = await response.json();
            if (data.errores) {
                setError(data.errores);
            } else {
                setAnalisisSintactico(data.sintactico.mensaje); // Establecer el mensaje del análisis sintáctico
                setError("");
            }
        } catch (error) {
            setError("Error de conexión con el servidor");
        }
    };
    

    const handleAnalisisSemantico = async () => {
        try {
            const response = await fetch("http://localhost:5000/semantico", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ textarea_content: texto }),
            });
    
            const data = await response.json();
            if (data.errores) {
                setError(data.errores);
            } else {
                if (data.resultado) {
                    // Extraer el valor de la variable i del objeto JSON
                    const valorI = data.resultado;
                    console.log("Valor de i:", valorI);
                    setAnalisisSemantico(valorI); // Establecer el resultado del análisis semántico
                } else {
                    setAnalisisSemantico("Análisis semántico exitoso");
                }
                setError("");
            }
        } catch (error) {
            setError("Error de conexión con el servidor");
        }
    };

    const formatAnalisisLexico = (tokens) => {
        return tokens.map(token => `Línea ${token.lineno}: Tipo ${token.type}, Valor '${token.value}'`).join("\n");
    };

    const createTablaTokens = (tokens) => {
        const tabla = tokens.map(token => ({
            valor: token.value,
            tipo: token.type,
            reservada: token.type === 'FOR' ? 'X' : '',
            id: token.type === 'ID' ? 'X' : '',
            numero: token.type === 'NUMBER' || token.type === 'FLOAT' ? 'X' : '',
            simbolo: ['EQUALS', 'LE', 'SEMICOLON', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'DOT'].includes(token.type) ? 'X' : '',
            error: ''
        }));

        const totales = {
            valor: 'Total',
            tipo: '',
            reservada: tabla.filter(token => token.reservada).length,
            id: tabla.filter(token => token.id).length,
            numero: tabla.filter(token => token.numero).length,
            simbolo: tabla.filter(token => token.simbolo).length,
            error: ''
        };

        return [...tabla, totales];
    };

    return (
        <StyledDivHome>
            <StyledDivHome2>
                <Title des="Inserta Código a Analizar"></Title>
                <StyledTextarea 
                    name="Texto" 
                    id="Texto" 
                    rows="10" 
                    cols="50" 
                    value={texto}
                    onChange={(e) => setTexto(e.target.value)} 
                />
            </StyledDivHome2>
            <StyledContainerAnalisis>
                <StyledContainerAnalisis2>
                    <StyledItem1>
                        <Button type="button" value="Análisis Léxico" handlerClick={handleAnalisisLexico} />
                        <Button type="button" value="Borrar" handlerClick={handleBorrarAnalisisLexico} />
                    </StyledItem1>
                    <StyledItem2>
                        <StyledTextarea 
                            name="AnalisisLexico" 
                            id="AnalisisLexico" 
                            rows="10" 
                            cols="50" 
                            value={analisisLexico} 
                            readOnly
                        />
                    </StyledItem2>
                </StyledContainerAnalisis2>
                <StyledContainerAnalisis2>
                    <StyledItem1>
                        <Button type="button" value="Análisis Sintáctico" handlerClick={handleAnalisisSintactico} />
                        <Button type="button" value="Borrar" handlerClick={handleBorrarAnalisisSintactico} /> 
                    </StyledItem1>
                    <StyledItem2>
                        <StyledTextarea 
                            name="AnalisisSintactico" 
                            id="AnalisisSintactico" 
                            rows="10" 
                            cols="50" 
                            value={analisisSintactico} 
                            readOnly
                        />
                    </StyledItem2>
                </StyledContainerAnalisis2>
                <StyledContainerAnalisis2>
                    <StyledItem1>
                        <Button type="button" value="Análisis Semántico" handlerClick={handleAnalisisSemantico} />
                        <Button type="button" value="Borrar" handlerClick={handleBorrarAnalisisSemantico} /> 
                    </StyledItem1>
                    <StyledItem2>
                        <StyledTextarea 
                            name="AnalisisSemantico" 
                            id="AnalisisSemantico" 
                            rows="10" 
                            cols="50" 
                            value={analisisSemantico} 
                            readOnly
                        />
                    </StyledItem2>
                </StyledContainerAnalisis2>
            </StyledContainerAnalisis>
            {error && <Error>{error}</Error>}
                {tablaTokens.length > 0 && (
                    <StyledTable>
                        <thead>
                            <tr>
                                <th>Valor</th>
                                <th>Reservada</th>
                                <th>ID</th>
                                <th>Número</th>
                                <th>Símbolo</th>
                                <th>Error</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tablaTokens.map((token, index) => (
                                <tr key={index}>
                                    <td>{token.valor}</td>
                                    <td>{token.reservada}</td>
                                    <td>{token.id}</td>
                                    <td>{token.numero}</td>
                                    <td>{token.simbolo}</td>
                                    <td>{token.error}</td>
                                </tr>
                            ))}
                        </tbody>
                    </StyledTable>
                )}
        </StyledDivHome>
    );
}

const StyledDivHome = styled.div`
    height: 100vh;
    width: 100%;
    background-color: #b0a17c;
    display: grid;
    align-items: center;
    justify-content: center;
`;

const StyledDivHome2 = styled.div`
    display: grid;
    align-items: center;
    justify-content: center;
`;

const StyledTextarea = styled.textarea`
    background-color: #dfdacd;
    resize: none;
    color: #000000;
    font-family: Inter;
    font-size: 1rem;
    height: 15em;
    margin-top: 10px;
    font-style: normal;
    font-weight: 500;
    line-height: normal;
`;

const StyledContainerAnalisis = styled.div`
    display: grid;
    grid-template-columns: auto auto;
    gap: 50px;
    padding: 10px;
`;

const StyledContainerAnalisis2 = styled.div`
    display: grid;
`;

const StyledItem1 = styled.div`
    display: grid;
    grid-template-columns: auto auto;
`;

const StyledItem2 = styled.div`
    display: grid;
    grid-template-rows: auto;
`;

const Error = styled.div`
    color: red;
`;

const StyledTable = styled.table`
    border-collapse: collapse;
    width: 100%;
    margin-top: 20px;
    font-family: Arial, sans-serif;

    th, td {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }

    th {
        background-color: #f2f2f2;
    }
`;

export default Home;
