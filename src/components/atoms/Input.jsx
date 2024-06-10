import styled  from "styled-components";

const StyledInput = styled.input`
    color: #000000;
    background-color: #e7e7d5;
    font-family: Inter;
    font-size: 20px;
    font-style: normal;
    font-weight: 500;
    line-height: normal;
    cursor: pointer;
    border: 1px solid #e7e7d5;
    border-radius: 10px;
    height: 6em;
    width: 100%;
    padding: 0.5em 2em;

    &:hover {
        background-color: #f8f8f8;
        border-color: #e7e7d5;
    }
`;

const StyledDivButton = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
`;

function CustomInput({type, name, id, accept, handleChange}) {
    return ( 
        <StyledDivButton>
            <StyledInput type={type} name={name} id={id} accept={accept} onChange={handleChange} />
        </StyledDivButton>
    );
}

export default CustomInput;
