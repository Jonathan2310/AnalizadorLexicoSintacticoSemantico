import Title from "../components/atoms/Tittle";
import styled from "styled-components";

function NotFound() {
    return ( 
        <StyledDiv>
            <Title des="Error: 404. Página no encontrada"></Title>
        </StyledDiv>
        
    );
}

const StyledDiv=styled.div`
    height: 100vh;
    width: 100%;
    background-color: #b0a17c;
    display: flex;
    align-items: center;
    justify-content: center;
    
`

export default NotFound;
