import styled  from "styled-components";

const StyledButton = styled.button`
    color: #000000;
    background-color: #f4efed;
    font-family: Inter;
    font-size: 20px;
    font-style: normal;
    font-weight: 500;
    line-height: normal;
    cursor: pointer;
    border: 1px solid #f4efed;
    border-radius: 10px;
    width: 11em;
    height: 3.5em;

    &:hover {
        background-color: #e9d9b2;
        border-color: #e9d9b2;
    }
`;

const StyledDivButton = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
`;

function Button({type, value, handlerClick}) {
    return ( 
        <StyledDivButton>
            <StyledButton type={type} onClick={handlerClick}>{value}</StyledButton>
        </StyledDivButton>
    );
}

export default Button;
