import styled  from "styled-components";

const StyledTittle = styled.h1`
    color: #000000;
    font-family: Inter;
    font-size: 3rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
`;

function Tittle({des}) {
    return ( 
        <StyledTittle>{des}</StyledTittle>
    );
}

export default Tittle;
